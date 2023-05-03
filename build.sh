#!/bin/env bash

work_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

mkdir -p ${work_dir}/binaries &
. "${work_dir}/map/build.sh" &
wait
