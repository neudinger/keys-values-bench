#!/usr/bin/env bash

work_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Choose the value type stored as key  
export MAP_TYPES_KEY="int64_t"

# Choose the container type  
# export MAP_BUILD='["LLVM", "LLVM_MAP_VECTOR"]'
export MAP_BUILD='["STD","LLVM","BOOST","LLVM_MAP_VECTOR"]'

# Choose the value type stored as value  
# export LIST_TYPES='["int32_t"]'
export LIST_TYPES='["int32_t","int64_t","std::string"]'

# Choose the the recursion key value
# export RECURSIONS='[1,2]'
export RECURSIONS='[1,2,3]'

# Can use every file type compatible with plotly
export FILE_TYPES='["eps", "png", "svg"]' # "eps", "png", "svg",

eval "$(conda shell.bash hook)" && \
conda activate bench-env

python3 $PWD/read_results.py "map"
