cmake_minimum_required(VERSION 3.21)

set(TARGET "mapping")
project(${TARGET} VERSION 0.1)

set(WORKDIR ${CMAKE_CURRENT_LIST_DIR})
message(STATUS "WORKDIR in: ${WORKDIR}")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

get_filename_component(LIBDIR ${PROJECT_SOURCE_DIR} PATH)
set(LIBDIR ${LIBDIR}/libs)

set(LIKWID_INCLUDE_DIR ${LIBDIR}/likwid-5.2.0)
include_directories(${LIBDIR}/boost_1_77_0)
include_directories(${LIBDIR}/clang+llvm-13.0.0-x86_64-linux-gnu-ubuntu-20.04/include)


if(STD)
  add_compile_definitions(STD=True)
elseif(LLVM)
  add_compile_definitions(LLVM=True)
elseif(LLVM_MAP_VECTOR)
  add_compile_definitions(LLVM_MAP_VECTOR=True)
elseif(BOOST)
  add_compile_definitions(BOOST=True)
else()
  message(STATUS " PLEASE USE build.sh")
  RETURN()
endif()

if(MAP_VALUE AND KEYNAMES AND TYPES AND LIST_TYPE AND RECURSION)
else()
  message(STATUS "MAP_VALUE, KEYNAMES, TYPES, LIST_TYPE NOT SPECIFIED")
  RETURN()
endif()

if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  find_package(likwid REQUIRED)

# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mllvm -polly -Rpass-analysis=polly")
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mllvm -polly-parallel")
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mllvm -polly-vectorizer=stripmine")
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mllvm -polly-optimizer=pluto")
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  # using GCC
  find_package(likwid REQUIRED COMPONENTS marker OPTIONAL_COMPONENTS nvmarker)

# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fipa-matrix-reorg")
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "Intel")
# using Intel C++
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  # using Visual Studio C++
endif()

if(NOT EXISTS "${WORKDIR}/src/main.cc")
  add_custom_command(
    OUTPUT main

    COMMAND c++
    -DKEYNAMES=${KEYNAMES}
    -DTYPES=${TYPES}
    -DLIST_TYPE=${LIST_TYPE}
    -DRECURSION=${RECURSION}
    -DMAP_VALUE="${MAP_VALUE}"
    -std=c++2a -E
    ${WORKDIR}/src/make_main.in.cxx > ${WORKDIR}/src/main.cc

    COMMENT "generating main"
  )
  add_custom_command(
    OUTPUT ${WORKDIR}/src/main.cc
    DEPENDS main
    COMMAND sed -i "1i#include \\\"mapping.hpp\\\"" ${WORKDIR}/src/main.cc
    COMMENT "add main dependencies"
  )
endif(NOT EXISTS "${WORKDIR}/src/main.cc")

file(GLOB SRC
  "${WORKDIR}/src/*.hpp"
  "${WORKDIR}/src/*.cpp"
)

# file(WRITE ${WORKDIR}/src/version.cc
# "const char* getVersion() { return \"${${TARGET}_VERSION}\"; }"
# )
file(GLOB LLVM_LIBS
  "${LIBDIR}/clang+llvm-13.0.0-x86_64-linux-gnu-ubuntu-20.04/lib/*.so"
)

list(REMOVE_ITEM LLVM_LIBS "${LIBDIR}/clang+llvm-13.0.0-x86_64-linux-gnu-ubuntu-20.04/lib/LLVMPolly.so")
# https://cmake.org/cmake/help/v3.6/command/string.html#regex-specification
# list(FILTER lib_srcs EXCLUDE REGEX ".*LLVMPolly\\.so$")

add_executable(${TARGET} ${SRC} ${WORKDIR}/src/main.cc)
set_property(TARGET ${TARGET} PROPERTY CXX_STANDARD ${CMAKE_CXX_STANDARD})
set_property(TARGET ${TARGET} PROPERTY RULE_LAUNCH_COMPILE "${CMAKE_COMMAND} -E time")
set_property(TARGET ${TARGET} PROPERTY RULE_LAUNCH_LINK "${CMAKE_COMMAND} -E time")

# target_compile_options(${TARGET} PRIVATE -O3 -g)
target_compile_features(${TARGET} PRIVATE cxx_std_${CMAKE_CXX_STANDARD})
target_compile_options(${TARGET} PRIVATE -march=native -mtune=native)
target_include_directories(${TARGET} SYSTEM PRIVATE ${LIBDIR}/clang+llvm-13.0.0-x86_64-linux-gnu-ubuntu-20.04/)
target_link_libraries(${TARGET}
  PUBLIC
  likwid::likwid
  ${LLVM_LIBS}
)

unset(MAP_VALUE CACHE)
unset(KEYNAMES CACHE)
unset(TYPES CACHE)
unset(LIST_TYPE CACHE)
unset(RECURSION CACHE)

unset(STD CACHE)
unset(LLVM CACHE)
unset(LLVM_MAP_VECTOR CACHE)
unset(BOOST CACHE)
