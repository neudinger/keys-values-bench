# Benchmark of keys values containers with likwid

![](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

![C++](https://img.shields.io/badge/c++17-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white) ![](https://img.shields.io/badge/Python_3-FFD43B?style=for-the-badge&logo=python&logoColor=blue) ![](https://img.shields.io/badge/Shell_Script-121011?style=for-the-badge&logo=gnu-bash&logoColor=white)

![](https://img.shields.io/badge/CMake-064F8C?style=for-the-badge&logo=cmake&logoColor=white) ![](https://img.shields.io/badge/conda_env-342B029.svg?&style=for-the-badge&logo=anaconda&logoColor=white)


![](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white) ![](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white) ![](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)

![](https://llvm.org/img/LLVM-Logo-Derivative-1.png) ![](https://hpc.fau.de/files/2017/10/ll2-285x200.png) ![](https://upload.wikimedia.org/wikipedia/commons/c/cd/Boost.png) ![](https://mamba.readthedocs.io/en/latest/_static/logo.png)

This project require C++ 17 due to the usage of [structured bindings](https://en.cppreference.com/w/cpp/language/structured_binding)

## Install commands

Required

- C++ Compiler gnu g++ or LLVM clang++ 
- [micromamba](https://mamba.readthedocs.io/en/latest/installation.html#micromamba)



```bash
mamba env create -f environment.yml
conda activate bench-env

export C_INCLUDE_PATH=${CONDA_PREFIX}/include
export CPLUS_INCLUDE_PATH=${CONDA_PREFIX}/include
```

```bash
# Sometime this is required for the compiler to find include and the libraries
# export C_INCLUDE_PATH=${C_INCLUDE_PATH}:${PWD}/libs/clang+llvm-13.0.0-x86_64-linux-gnu-ubuntu-20.04/include
# export CPLUS_INCLUDE_PATH=${CPLUS_INCLUDE_PATH}:${PWD}/libs/clang+llvm-13.0.0-x86_64-linux-gnu-ubuntu-20.04/include
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${PWD}/libs/clang+llvm-13.0.0-x86_64-linux-gnu-ubuntu-20.04/lib
# export LIBRARY_PATH=$LIBRARY_PATH:${PWD}/libs/clang+llvm-13.0.0-x86_64-linux-gnu-ubuntu-20.04/lib
```

- Download and install the required dependencies 
  ```bash
  ./dl_lib.sh
  ```

- Build every binary
  ```bash
  ./build.sh
  ```

- Run every binary in ./binaries directory with likwid monitoring and write csv result in ./results/csv/
  ```bash
  ./run.sh
  ```

- Read csv to convert in eps, png, svg image performance chart
  ```
  ./read_results.sh
  ```


## Likwid simple usage

- Please use the `./run.sh`

```sh
# https://rrze-hpc.github.io/likwid/Doxygen/likwid-perfctr.html
likwid-perfctr -O -m -C S0:0 -g MEM_DP ./binaries/stencil_EIGEN_1D 10 1000 > EIGEN_1D.csv

likwid-perfctr -O -m -C S0:0 -g MEM_DP ./binaries/map_STD-3RK\=int64_t-MAP_VALUE\=k1 10 > map_STD\=int64_t-MAP_VALUE\=k1.csv
```

## MAP
Bench between most popular Key Value library

See some result [result](./result.md)

- [x] std::map
- [x] LLVM::map
- [x] LLVM::map_vector
- [x] boost::container::map
- [ ] [parallel-hashmap](https://github.com/greg7mdp/parallel-hashmap) (incoming)
- [ ] [sparsepp](https://github.com/greg7mdp/sparsepp) (incoming)





