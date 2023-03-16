#! /bin/bash

set -e -x

if [ X"${1}" = X"primary" ]; then
    exec /app/bootstrap.sh
else
    exec "$@"
fi
