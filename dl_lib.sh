#!/bin/env bash

declare DEV_WORKDIR=${PWD}
declare libdir=${PWD}/libs

declare ALL_LIBS=(
    https://boostorg.jfrog.io/artifactory/main/release/1.77.0/source/boost_1_77_0.tar.bz2
    https://github.com/llvm/llvm-project/releases/download/llvmorg-13.0.0/clang+llvm-13.0.0-x86_64-linux-gnu-ubuntu-20.04.tar.xz
)

mkdir -p ${libdir};

for lib in ${ALL_LIBS[@]};
do
    curl --progress-bar -L ${lib} -o lib.tar.gz && \
    tar -xvf lib.tar.gz -C ${libdir} && \
    rm lib.tar.gz
done

# Remove LLVMPolly.so due to linker error
# rm ${libdir}/clang+llvm-13.0.0-x86_64-linux-gnu-ubuntu-20.04/lib/LLVMPolly.so

# # ====BUILD LIB====
export PREFIX=${CONDA_PREFIX}
export CMAKE_INSTALL_PREFIX=${CONDA_PREFIX}

# Install boost
cd ${libdir}/boost_1_77_0/
./bootstrap.sh
./b2


# Install LIKWID
cd ${DEV_WORKDIR};
# sed in file because with sudo make install PREFIX env disappear
wget https://github.com/RRZE-HPC/likwid/archive/refs/tags/v5.2.0.tar.gz && \
tar -xvf v5.2.0.tar.gz -C ${libdir} && rm v5.2.0.tar.gz && \
sed -i "s|\/usr\/local|$CONDA_PREFIX|" ${libdir}/likwid-5.2.0/config.mk && \
cd ${libdir}/likwid-5.2.0 && make && sudo make install

cd ${DEV_WORKDIR};
