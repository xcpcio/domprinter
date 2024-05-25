import os
import json
import time
import typst
import requests
import constants
import subprocess
from multiprocessing import Process, Queue
from utils.tools import Logger

logger = Logger()

HEADERS = {'content-type': 'application/json'}

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_PATH = os.path.join(CUR_DIR, "output")

PRINT_HEADER = """2024 Jiangxi Provincial Collegiate Programming Contest - TechGroup
座位：{}
队伍：{}
提交时间：{}
"""

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

class TaskProcessor(Process):
    def __init__(self, queue, config):
        super().__init__()
        self.queue = queue
        self.base_url = self.make_base_url(config)
        self.location_filter_list = config.get("filter_list", [])
        ensure_dir(OUTPUT_PATH)
        logger.info("TaskProcessor has been initialized.")
    
    @classmethod
    def make_base_url(cls, config):
        return "http://{}:{}@{}:{}/print-task".format(
            config['auth_name'],
            config['auth_passwd'],
            config['service_host'],
            config['service_port']
        )
    
    def fetch_task(self):
        local_url = self.base_url + "?TaskState=1&LimitTaskNum=32"
        resp = requests.get(local_url, headers=HEADERS, verify=False, timeout=10)
        if resp.status_code != 200:
            logger.warning("fetch error. [status_code={}]".format(resp.status_code))
        return json.loads(resp.text)
    
    def process_task(self, task):
        try:
            self.queue.put(('NEW', task))
            submit_time = task["SubmitTime"]
            user_name = task["UserName"]
            team_name = task["TeamName"]
            team_id = task["TeamID"]
            location = task["Location"]
            if location not in self.location_filter_list:
                logger.info("Location {} is not in the filter list, skip.".format(location))
            language = task["Language"]
            # language = "plaintext"
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

            header = PRINT_HEADER.format(location, team_name, submit_time)

            with open(typst_path, "w") as f:
                f.write(constants.TYPST_CONFIG %
                        (print_task_id, team_name, location, filename, language, code_file_name, header))

            typst.compile(typst_path, output=pdf_path)

            cmd = "lp -o charset=UTF-8 -o print-quality=5 -P 1-16 {}".format(pdf_path)
            subprocess.run(cmd, shell=True)
            # logger.critical("SIMULATE PRINTING: {}".format(cmd))

            self.done_task(print_task_id)
            self.queue.put(('DONE', task))
        except Exception as e:
            logger.error("handle print task error. [error={}]".format(e))
        
    def done_task(self, task_id):
        resp = requests.patch(
        self.base_url, {"TaskState": 2, "PrintTaskIDList": [task_id]}, verify=False)

        if resp.status_code != 200:
            logger.error("done error. [task_id={}] [status_code={}]".format(task_id, resp.status_code))

        return resp
    
    def run(self):
        self.queue.put(('INIT', 'INIT'))
        logger.info("Start pulling the task list...")
        while True:
            try:
                r = self.fetch_task()
                r = r["PrintTaskList"]
                if len(r) == 0:
                    logger.info("Empty task list, request again in 1 second...")
                for task in r:
                    logger.info("Received tasks, processing...")
                    self.process_task(task)
            except Exception as e:
                logger.error("Error: {}".format(e))
            finally:
                time.sleep(5)
    
