import os
import time
import requests
import json
import typst
import subprocess

import constants

HEADERS = {'content-type': 'application/json'}

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_PATH = os.path.join(CUR_DIR, "output")

BASE_URL = os.getenv(
    "BASE_URL", "http://username:password@localhost:8080/print-task")


def fetch():
    local_url = BASE_URL + "?TaskState=1&LimitTaskNum=32"
    resp = requests.get(local_url, headers=HEADERS, verify=False, timeout=10)

    if resp.status_code != 200:
        raise Exception(
            "fetch error. [status_code={}]".format(resp.status_code))

    return json.loads(resp.text)


def done(task_id):
    resp = requests.patch(
        BASE_URL, {"TaskState": 2, "PrintTaskIDList": [task_id]}, verify=False)

    if resp.status_code != 200:
        raise Exception(
            "done error. [task_id={}] [status_code={}]".format(task_id, resp.status_code))

    return resp


def ensure_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


def handle_print_task(task):
    try:
        submit_time = task["SubmitTime"]
        user_name = task["UserName"]
        team_name = task["TeamName"]
        team_id = task["TeamID"]
        location = task["Location"]
        language = task["Language"]
        filename = task["FileName"]
        source_code = task["SourceCode"]
        print_task_id = task["PrintTaskID"]
        task_state = task["TaskState"]

        if len(team_name) == 0:
            team_name = "无"

        if len(location) == 0:
            location = "无"

        print("handle print task. [print_task_id={}] [task_state={}] [submit_time={}] [user_name={}] [team_name={}] [team_id={}] [location={}] [language={}] [filename={}]".format(
            print_task_id, task_state, submit_time, user_name, team_name, team_id, location, language, filename))

        build_dir = os.path.join(OUTPUT_PATH, str(print_task_id))
        ensure_dir(build_dir)

        typst_path = os.path.join(build_dir, "main.typst")
        pdf_path = os.path.join(build_dir, "main.pdf")
        code_file_name = "main.{}".format(language)
        code_file_path = os.path.join(build_dir, code_file_name)
        with open(code_file_path, "w") as f:
            f.write(source_code)

        header = """座位：{}
队伍：{}
提交时间：{}

""".format(location, team_name, submit_time)

        with open(typst_path, "w") as f:
            f.write(constants.TYPST_CONFIG %
                    (print_task_id, team_name, location, filename, language, code_file_name, header))

        typst.compile(typst_path, output=pdf_path)

        cmd = "lp -o charset=UTF-8 -o print-quality=5 -P 1-10 {}".format(
            pdf_path)
        subprocess.run(cmd, shell=True)

        done(print_task_id)
    except Exception as e:
        print("handle print task error. [error={}]".format(e))


def init():
    ensure_dir(OUTPUT_PATH)


def main():
    init()

    while True:
        try:
            r = fetch()
            r = r["PrintTaskList"]
            for task in r:
                handle_print_task(task)
        except Exception as e:
            print(e)
        finally:
            time.sleep(1)


if __name__ == "__main__":
    main()
