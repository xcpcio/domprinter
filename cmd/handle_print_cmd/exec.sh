#! /bin/bash

CUR_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

FILE="${1}"
ORIGINAL="${2}"
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

RES_MESSAGE=$(
    python3 <<EOF
import json
import urllib.request

body = {}
body["PrintTask"] = {}
p = body["PrintTask"]

p["SubmitTime"] = "${SUBMIT_TIME}"
p["UserName"] = "${USER_NAME}"
p["TeamName"] = "${TEAM_NAME}"
p["TeamID"] = "${TEAM_ID}"
p["LOCATION"] = "${LOCATION}"
p["Language"] = "${LANGUAGE}"
p["FileName"] = "${ORIGINAL}"
p["SourceCode"] = '''
//    FILE_NAME=${FILE_NAME}
//    LANGUAGE=${LANGUAGE}
//    TEAM_NAME=${TEAM_NAME}
//    LOCATION=${LOCATION}

${SOURCE_CODE}
'''

url = "http://${DOMPRINTER_HOSTNAME:-127.0.0.1}:${DOMPRINTER_PORT:-8888}/print-task"
payload = json.dumps(body)
headers = {'Content-Type': 'application/json'}

req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers=headers)
response = urllib.request.urlopen(req)
code = response.status
res = json.loads(response.read().decode('utf-8'))

def main():
    if code == 200:
        print("{}. [TEAM_NAME={}] [LOCATION={}] [FILE={}] [LANGUAGE={}]".format(res["BaseResp"]["RespMessage"], "${TEAM_NAME}", "${LOCATION}", "${ORIGINAL}", "${LANGUAGE}"))
        return
    else:
        print("Submit PrintTask Failed. [CODE={}]".format(code))

    print(res)

main()
EOF
)

echo "${RES_MESSAGE}"
echo "[FILE=${FILE}] [ORIGINAL=${ORIGINAL}] [LANGUAGE=${LANGUAGE}] [USER_NAME=${USER_NAME}] [TEAM_NAME=${TEAM_NAME}] [TEAM_ID=${TEAM_ID}] [LOCATION=${LOCATION}] [RES=${RES_MESSAGE}]" >>"${CUR_DIR}/handle_print_cmd.log"

# test command
# ./cmd/handle_print_cmd/exec.sh /tmp/abcdefg a.cpp cpp Dup4 Dup4 Dup4 test

# configure print command
# /handle_print_cmd/exec.sh [file] [original] [language] [username] [teamname] [teamid] [location] 2>&1
