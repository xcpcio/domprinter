#! /bin/bash

set -e -x

if [[ -n "${HANDLE_PRINT_CMD_PATH}" ]]; then
    cp "/app/handle_print_cmd/exec.sh" "${HANDLE_PRINT_CMD_PATH}"
    chmod 755 "${HANDLE_PRINT_CMD_PATH}/exec.sh"
    touch "${HANDLE_PRINT_CMD_PATH}/handle_print_cmd.log"
    chmod 777 "${HANDLE_PRINT_CMD_PATH}/handle_print_cmd.log"
fi

if [ X"${1}" = X"primary" ]; then
    exec /app/bootstrap.sh
else
    exec "$@"
fi
