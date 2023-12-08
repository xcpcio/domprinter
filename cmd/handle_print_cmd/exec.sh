#! /bin/bash

CUR_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

FILE="${1}"
ORIGINAL_FILE="${2}"
LANGUAGE="${3}"
USER_NAME="${4}"
TEAM_NAME="${5}"
TEAM_ID="${6}"
LOCATION="${7}"

if [[ -n "${SUBMIT_FILE_LIMIT}" ]]; then
    if [[ -s "${FILE}" && $(stat -c%s "${FILE}") -gt "${SUBMIT_FILE_LIMIT}" ]]; then
        echo "File size exceeding the limit."
        exit 0
    fi
fi

SOURCE_CODE="$(cat "${FILE}")"
# SOURCE_CODE="$(cat -n "${FILE}" | sed 's/\\n/\\\\n/g' | sed 's/\\r/\\\\r/g')"

if [[ "$(uname -a | grep -c "MacBookPro")" -ge 1 ]]; then
    SUBMIT_TIME="2023-03-16T11:30:49.799+08:00"
else
    SUBMIT_TIME="$(date --rfc-3339=ns | sed 's/ /T/; s/\(\....\).*\([+-]\)/\1\2/g')"
fi

RES_MESSAGE=$(
    python3 <<EOF
import json
import urllib.request
import base64

body = {}
body["PrintTask"] = {}
p = body["PrintTask"]

p["SubmitTime"] = r"${SUBMIT_TIME}"
p["UserName"] = r"${USER_NAME}"
p["TeamName"] = r"${TEAM_NAME}"
p["TeamID"] = r"${TEAM_ID}"
p["LOCATION"] = r"${LOCATION}"
p["Language"] = r"${LANGUAGE}"
p["FileName"] = r"${ORIGINAL_FILE}"
p["SourceCode"] = r'''${SOURCE_CODE}'''

url = "http://${DOMPRINTER_HOSTNAME:-127.0.0.1}:${DOMPRINTER_PORT:-8888}/print-task"
payload = json.dumps(body)
headers = {'Content-Type': 'application/json'}

def main():
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers=headers)

    auth_base64_string = base64.b64encode("{}:{}".format("${AUTH_USERNAME}", "${AUTH_PASSWORD}").encode()).decode()
    req.add_header("Authorization", "Basic {}".format(auth_base64_string))

    response = urllib.request.urlopen(req)
    code = response.status
    res = json.loads(response.read().decode('utf-8'))
    request_id = response.info().get("X-Request-Id")

    if code == 200:
        message = res["BaseResp"]["RespMessage"]
        print_task_id = res["PrintTaskID"]
        print("{}.\n[PrintTaskID={}]\n[RequestID={}]\n[SubmitTime={}]\n[FILE_NAME={}]\n[LANGUAGE={}]\n[TEAM_NAME={}]\n[LOCATION={}]".format(message, print_task_id, request_id, r"${SUBMIT_TIME}", r"${ORIGINAL_FILE}", r"${LANGUAGE}", r"${TEAM_NAME}", r"${LOCATION}"))
    else:
        print("Submit PrintTask Failed. Please try again or contact the administrator. [CODE={}] [RequestID={}]".format(code, request_id))

main()
EOF
)

echo "${RES_MESSAGE}"
echo "[FILE=${FILE}] [ORIGINAL_FILE=${ORIGINAL_FILE}] [LANGUAGE=${LANGUAGE}] [USER_NAME=${USER_NAME}] [TEAM_NAME=${TEAM_NAME}] [TEAM_ID=${TEAM_ID}] [LOCATION=${LOCATION}] [RES=${RES_MESSAGE}]" >>"${CUR_DIR}/handle_print_cmd.log"

# test command
# AUTH_USERNAME=domprinter AUTH_PASSWORD=domprinter DOMPRINTER_HOSTNAME=devbox ./cmd/handle_print_cmd/exec.sh /tmp/abcdefg a.cpp cpp Dup4 Dup4 Dup4 test

# configure print command
# AUTH_USERNAME=domprinter AUTH_PASSWORD=domprinter DOMPRINTER_HOSTNAME=domprinter /handle_print_cmd/exec.sh [file] [original] [language] [username] [teamname] [teamid] [location] 2>&1
