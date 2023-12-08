import os
import time
import requests
import json

headers = {'content-type': 'application/json'}

BASE_URL = os.getenv(
    "BASE_URL", "http://username:password@localhost:8080/print-task")


def fetch():
    local_url = BASE_URL + "?TaskState=1&LimitTaskNum=32"
    resp = requests.get(local_url, headers=headers, verify=False, timeout=10)

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

        print("handle print task. [print_task_id={}] [task_state={}] [submit_time={}] [user_name={}] [team_name={}] [team_id={}] [location={}] [language={}] [filename={}]".format(
            print_task_id, task_state, submit_time, user_name, team_name, team_id, location, language, filename))

        print(source_code)

        done(print_task_id)
    except Exception as e:
        print("handle print task error. [error={}]".format(e))


def main():
    while True:
        try:
            r = fetch()
            r = r["PrintTaskList"]
            for task in r:
                handle_print_task(task)
            time.sleep(1)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
