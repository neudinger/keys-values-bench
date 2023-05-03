#!/bin/env bash
work_dir=${PWD}
build_dir=${work_dir}/builds/map
here=${work_dir}/map

declare ALL_BUILD=(
    STD
    LLVM
    LLVM_MAP_VECTOR
    BOOST
)

declare LIST_TYPES=(
    int32_t
    int64_t
    std::string
)

declare MAP_TYPES_KEY=int64_t
declare RECURSIONS=(
    1
    2
    3
)

for RECURSION in ${RECURSIONS[@]};
do
    unset KEYNAMES
    for i in $(seq 1 ${RECURSION});
    do
        KEYNAMES=${KEYNAMES},k${i};
    done
    KEYNAMES=${KEYNAMES: 1}
    for LIST_TYPE in ${LIST_TYPES[@]};
    do
        unset TYPES
        if [[ "${LIST_TYPE}" == "std::string" ]];
        then
            MAP_VALUE="std::to_string(std::bind(uid,re)())";
        else
            MAP_VALUE=k1
        fi
        for i in $(seq 1 ${RECURSION});
        do
            TYPES=${TYPES}${MAP_TYPES_KEY},;
        done
        TYPES=${TYPES}${LIST_TYPES}
        for build in ${ALL_BUILD[@]};
        do
            #Release OR MinSizeRel OR RelWithDebInfo
            cmake -S ${here} \
            -DMAP_VALUE="${MAP_VALUE}" \
            -DKEYNAMES=${KEYNAMES} \
            -DTYPES=${TYPES} \
            -DLIST_TYPE=${LIST_TYPE} \
            -DRECURSION=${RECURSION} \
            -DCMAKE_BUILD_TYPE=RelWithDebInfo \
            -D${build}:BOOL=ON  \
            -B ${build_dir} \
            && cmake --build ${build_dir} && \
            mv ${build_dir}/mapping ${work_dir}/binaries/map_${build}-${RECURSION}-${MAP_TYPES_KEY}-${LIST_TYPE};
        done
    done
    rm -f ${here}/src/main.cc;
    # Debug
    # mv ${here}/src/main.cc ${here}/src/main.cxx
done

