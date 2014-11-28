#!/bin/bash

BASEDIR=$( cd $( dirname ${BASH_SOURCE[0]} ) && pwd )
GOAT_PROMPT="baaa> "

function usage {
echo <<EOF
usage: $script <user-id>

Starts a REPL for goat tower using the user-id passed in
EOF
}
if [ -z "$1" ]; then usage; exit 1; fi

pushd "$BASEDIR"/.. > /dev/null
function cleanup {
    popd > /dev/null
    echo    
}
trap cleanup EXIT

user=$1
while read -p "$GOAT_PROMPT" input; do
    python cli.py $user $input
done
