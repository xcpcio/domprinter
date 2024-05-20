import os
import time
import requests
import json
import typst
import subprocess
import chardet

# 配置信息
CONFIG = {
    "HEADERS": {'content-type': 'application/json'},
    "BASE_URL": "",# 更改为你的打印服务器的实际路径，例如http://admin:admin@127.0.0.1:8080/print-task
    "SUMATRA_PATH": "",  # 更改为SumatraPDF的实际路径，例如D:\SumatraPDF.exe
    "PRINTER_NAME": "" # 更改为你想使用的打印机名称，例如HP LaserJet Professional
}

# Typst 配置
TYPST_CONFIG = """
#let print(
    task_id: "",
    team: "",
    location: "",
    filename: "",
    lang: "",
    filepath: "",
    header: "",
    body
) = {
    set document(author: (team), title: filename)
    set text(font: "ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace", lang: "zh")
    set page(
        paper: "a4",
        header: [
            filename: #filename
            #h(1fr)
            id: #task_id
            #h(1fr)
            Page #counter(page).display("1 of 1", both: true)
        ],
        margin: (
            top: 48pt,
            bottom: 28pt,
            left: 24pt,
            right: 32pt,
        )
    )

    header
    raw(read(filepath), lang: lang)
    body
}

#show raw.line: it => {
    box(stack(
        dir: ltr,
        box(width: 24pt)[#it.number],
        it.body,
    ))
}

#show: print.with(
    task_id: "%s",
    team: "%s",
    location: "%s",
    filename: "%s",
    lang: "%s",
    filepath: "%s",
    header: "%s",
)
"""

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_PATH = os.path.join(CUR_DIR, "output")

def fetch():
    local_url = CONFIG["BASE_URL"] + "?TaskState=1&LimitTaskNum=32"
    resp = requests.get(local_url, headers=CONFIG["HEADERS"], verify=False, timeout=10)

    if resp.status_code != 200:
        raise Exception(
            "fetch error. [status_code={}]".format(resp.status_code))

    return json.loads(resp.text)

def done(task_id):
    resp = requests.patch(
        CONFIG["BASE_URL"], {"TaskState": 2, "PrintTaskIDList": [task_id]}, verify=False)

    if resp.status_code != 200:
        raise Exception(
            "done error. [task_id={}] [status_code={}]".format(task_id, resp.status_code))

    return resp

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def detect_encoding(data):
    result = chardet.detect(data)
    return result['encoding']

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
        
        # Detect encoding and convert to UTF-8
        source_code_bytes = source_code.encode('latin1')  
        encoding = detect_encoding(source_code_bytes)
        source_code = source_code_bytes.decode(encoding).encode('utf-8').decode('utf-8')
        
        with open(code_file_path, "w", encoding="utf-8") as f:
            f.write(source_code)

        header = """座位：{}
队伍：{}
提交时间：{}

""".format(location, team_name, submit_time)

        with open(typst_path, "w", encoding="utf-8") as f:
            f.write(TYPST_CONFIG %
                    (print_task_id, team_name, location, filename, language, code_file_name, header))

        typst.compile(typst_path, output=pdf_path)

        cmd = '"{}" -print-to "{}" "{}"'.format(CONFIG["SUMATRA_PATH"], CONFIG["PRINTER_NAME"], pdf_path)
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
            print("running...")

if __name__ == "__main__":
    main()
