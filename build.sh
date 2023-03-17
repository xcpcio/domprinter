#! /bin/bash

CUR_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

BINARY_NAME=domprinter
OUTPUT_DIR="${CUR_DIR}/output"

if [[ -d "${OUTPUT_DIR}" ]]; then
    rm -rf "${OUTPUT_DIR}"
fi

mkdir -p "${OUTPUT_DIR}/"{bin,handle_print_cmd}

cp "${CUR_DIR}/script"/* "${OUTPUT_DIR}"/ 2>/dev/null
chmod +x "${OUTPUT_DIR}/bootstrap.sh"

go build -o "${OUTPUT_DIR}/bin/${BINARY_NAME}"
go build -o "${OUTPUT_DIR}/bin/health_check" ./cmd/health_check

cp -a "${CUR_DIR}/cmd/handle_print_cmd/exec.sh" "${OUTPUT_DIR}"/handle_print_cmd/exec.sh
