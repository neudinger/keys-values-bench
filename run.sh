#!/bin/env bash

declare work_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
declare binaries_dir=${PWD}/binaries
declare bench_result=${PWD}/results/csv;
mkdir -p ${bench_result};

export OMP_NUM_THREADS=`nproc`

declare GROUP_NAME=(
    MEM_DP
    # L2CACHE
    # L3CACHE
    # L2
    # L3
)

declare maps=$(find -path './binaries/*' -prune -name "map_*");
declare stencils=$(find -path './binaries/*' -prune -name "stencil_*");

declare SIZES=(
    200
    400
    600
)

declare MAX_IT=420

cmd="likwid-perfctr -O -C S0"

set -x;

for group_name in ${GROUP_NAME[@]};
do
    for map in ${maps[@]};
    do
        for SIZE in ${SIZES[@]};
        do
            echo ${group_name} ${map##*/}" "${SIZE}
            $cmd -m -g ${group_name} ${map} ${SIZE} >> ${bench_result}/${map##*/}.csv
        done
    done
done
