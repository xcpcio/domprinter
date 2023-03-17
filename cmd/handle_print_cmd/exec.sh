#! /bin/bash

CUR_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

FILE="${1}"
ORIGINAL_FILE="${2}"
LANGUAGE="${3}"
USER_NAME="${4}"
TEAM_NAME="${5}"
TEAM_ID="${6}"
LOCATION="${7}"

SOURCE_CODE="$(cat "${FILE}")"

if [[ "$(uname -a | grep -c "MacBookPro")" -ge 1 ]]; then
    SUBMIT_TIME="2023-03-16T11:30:49.799+08:00"
else
    SUBMIT_TIME="$(date -u --rfc-3339=ns | sed 's/ /T/; s/\(\....\).*\([+-]\)/\1\2/g')"
fi

COMMENT_CHAR="//"
if [[ "${LANGUAGE}" == "py" ]] || [[ "${LANGUAGE}" == "py2" ]] || [[ "${LANGUAGE}" == "py3" ]]; then
    COMMENT_CHAR="#"
fi

RES_MESSAGE=$(
    python3 <<EOF
import json
import urllib.request
import base64

body = {}
body["PrintTask"] = {}
p = body["PrintTask"]

p["SubmitTime"] = "${SUBMIT_TIME}"
p["UserName"] = "${USER_NAME}"
p["TeamName"] = "${TEAM_NAME}"
p["TeamID"] = "${TEAM_ID}"
p["LOCATION"] = "${LOCATION}"
p["Language"] = "${LANGUAGE}"
p["FileName"] = "${ORIGINAL_FILE}"
p["SourceCode"] = '''
${COMMENT_CHAR}    FILE_NAME=${ORIGINAL_FILE}
${COMMENT_CHAR}    LANGUAGE=${LANGUAGE}
${COMMENT_CHAR}    TEAM_NAME=${TEAM_NAME}
${COMMENT_CHAR}    LOCATION=${LOCATION}

${SOURCE_CODE}
'''

url = "http://${AUTH_STRING}${DOMPRINTER_HOSTNAME:-127.0.0.1}:${DOMPRINTER_PORT:-8888}/print-task"
payload = json.dumps(body)
headers = {'Content-Type': 'application/json'}

def main():
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers=headers)

    auth_base64_string = base64.b64encode("{}:{}".format("${AUTH_USERNAME}", "${AUTH_PASSWORD}").encode()).decode()
    req.add_header("Authorization", "Basic {}".format(auth_base64_string))

    response = urllib.request.urlopen(req)
    code = response.status
    res = json.loads(response.read().decode('utf-8'))

    if code == 200:
        print("{}. [PrintTaskID={}] [FILE_NAME={}] [LANGUAGE={}] [TEAM_NAME={}] [LOCATION={}]".format(res["BaseResp"]["RespMessage"], res["PrintTaskID"], "${ORIGINAL_FILE}", "${LANGUAGE}", "${TEAM_NAME}", "${LOCATION}"))
    else:
        print("Submit PrintTask Failed. Please try again or contact the administrator. [CODE={}]".format(code))

main()
EOF
)

echo "${RES_MESSAGE}"
echo "[FILE=${FILE}] [ORIGINAL_FILE=${ORIGINAL_FILE}] [LANGUAGE=${LANGUAGE}] [USER_NAME=${USER_NAME}] [TEAM_NAME=${TEAM_NAME}] [TEAM_ID=${TEAM_ID}] [LOCATION=${LOCATION}] [RES=${RES_MESSAGE}]" >>"${CUR_DIR}/handle_print_cmd.log"

# test command
# DOMPRINTER_HOSTNAME=devbox ./cmd/handle_print_cmd/exec.sh /tmp/abcdefg a.cpp cpp Dup4 Dup4 Dup4 test

# configure print command
# DOMPRINTER_HOSTNAME=domprinter /handle_print_cmd/exec.sh [file] [original] [language] [username] [teamname] [teamid] [location] 2>&1
