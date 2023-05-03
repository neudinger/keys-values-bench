#!/usr/bin/env python3

# %%
import itertools
import os
import json
import pandas
import plotly
import numpy
import sys
import pathlib

MAP_TYPES_KEY = "int64_t"
MAP_BUILD = (
    "STD",
    "LLVM",
    "BOOST",
    "LLVM_MAP_VECTOR",
)
LIST_TYPES = (
    "int32_t",
    "int64_t",
    "std::string",
)
RECURSIONS = (
    1,
    2,
    3,
)
STENCILS_BUILD = (
    "BLAZE",
    "ARRAY_2D",
    "EIGEN_2D",
    "ARMADILLO",
    "XTENSOR_2D",
    "BOOST_UBLAS",
    "STD_VECTOR_2D",
)
FILE_TYPES: list[str] = ["png"]

file_types = os.getenv("FILE_TYPES")
file_types = json.loads(file_types) if file_types else FILE_TYPES
stencils_build = os.getenv("STENCILS_BUILD")
stencils_build: list[str] = json.loads(
    stencils_build) if stencils_build else STENCILS_BUILD
map_types_key = os.getenv("MAP_TYPES_KEY", MAP_TYPES_KEY)
list_types = os.getenv("LIST_TYPES")
list_types = json.loads(list_types) if list_types else LIST_TYPES
recursions = os.getenv("RECURSIONS")
recursions = json.loads(recursions) if recursions else RECURSIONS
map_build = os.getenv("MAP_BUILD")
map_build = json.loads(map_build) if map_build else MAP_BUILD
setup_benchs = dict(
    MEM_DP=dict(
        positions={
            "Energy [J]": 1,
            "Power [W]": 1,
            "DP [MFLOP/s]": 1,
            "DRAM_READS": 2,
            "DRAM_WRITES": 2,
            "PWR_PKG_ENERGY": 2,
            "PWR_DRAM_ENERGY": 2,
            "Memory load data volume [GBytes]": 1,
            "Memory evict data volume [GBytes]": 1,
            "Energy DRAM [J]": 1,
            "Power DRAM [W]": 1,
            "Memory data volume [GBytes]": 1,
            "Runtime (RDTSC) [s]": 1,
            "Operational intensity": 1,
        }),
    L2=dict(
        positions={
            "L2D load data volume [GBytes]": 1,
            "L2 data volume [GBytes]": 1,
        },
    ),
    L3=dict(
        positions={
            "L3 load data volume [GBytes]": 1,
            "L3 data volume [GBytes]": 1,
        }
    ),
    L2CACHE=dict(
        positions={
            "L2 request rate": 1,
            "L2 miss rate": 1,
            "L2 miss ratio": 1,
        }),
    L3CACHE=dict(
        positions={
            "L3 request rate": 1,
            "L3 miss rate": 1,
            "L3 miss ratio": 1,
        }),
)

color_style = itertools.cycle(["mediumblue",
                               "mediumorchid",
                               "mediumpurple",
                               "mediumseagreen",
                               "mediumslateblue",
                               "mediumspringgreen",
                               "mediumturquoise",
                               ])

dash_style = itertools.cycle(["solid",
                              "dash",
                              "longdash",
                              "solid",
                              "dashdot",
                              "dot",
                              "longdashdot"])

symbol_style = itertools.cycle(["circle",
                                "square",
                                "diamond",
                                "cross",
                                "x",
                                "triangle-up",
                                "triangle-down",
                                "pentagon",
                                "hexagon",
                                "star"])


def get_size_of_elements_by_marker(dataframe: pandas.DataFrame) -> tuple:
    likwid_markers = list({_.split()[1]  # Get size from LIKWID_MARKER markername
                           # Region
                           for _ in
                           # Get LIKWID_MARKER markername
                           dataframe.loc[dataframe.iloc[:, 0]
                                         == "TABLE"][1].to_numpy()})
    likwid_markers: map = map(lambda val: (
        val.split('-')[0], int(val.split('-')[1])), likwid_markers)
    dict_merged: dict = {}
    for marker in likwid_markers:
        if marker[0] in dict_merged.keys():
            dict_merged[marker[0]].append(marker[1])
        else:
            dict_merged[marker[0]] = [marker[1]]
    return (list(dict_merged.keys())[::-1], sorted(list(dict_merged.values())[0]))


def read_bench_file(file_path: str, bench_params: dict) -> dict:
    dataframe: pandas.DataFrame = pandas.read_csv(file_path,
                                                  names=list(range(6)))
    bench_results: dict = {}
    size_of_elements: tuple = get_size_of_elements_by_marker(
        dataframe=dataframe)
    likwid_marker_nbr: int = len(size_of_elements[0])
    for name, position in bench_params["positions"].items():
        likwid_marker_result: pandas.Series = dataframe.loc[
            dataframe.iloc[:, 0] == name][position].replace('nil', '0').to_numpy(dtype=numpy.float64)
        for idx in range(likwid_marker_nbr):
            result = likwid_marker_result[idx::likwid_marker_nbr]
            if size_of_elements[0][idx] in bench_results.keys():
                bench_results[size_of_elements[0][idx]].append(
                    [name, zip(size_of_elements[1], result)])
            else:
                bench_results[size_of_elements[0][idx]] = [
                    [name, zip(size_of_elements[1], result)]]
    return bench_results


def plotting(bench_results_areas: list = [], extra_name: str = "") -> list:
    data_traces: dict = dict()
    for file_bench in bench_results_areas:
        for function_bench, data in file_bench.items():
            for spec_name, spec in data:
                data_spec: dict = dict(spec)
                color_data: str = color_style.__next__()
                scatter = plotly.graph_objs.Scatter(
                    x=list(data_spec.keys()),
                    y=list(data_spec.values()),
                    name=function_bench,
                    line=dict(
                        dash=dash_style.__next__(),
                        color=color_data,
                        width=3
                    ),
                    marker=dict(
                        symbol=symbol_style.__next__(),
                        color=color_data,
                        size=10
                    ))
                if spec_name in data_traces.keys():
                    data_traces[spec_name].append(scatter)
                else:
                    data_traces[spec_name] = [scatter]
    perf_scatters: list = list()
    for perf_monitor_name, perf_monitors in data_traces.items():
        layout = plotly.graph_objs.Layout(
            title=perf_monitor_name + extra_name,
            xaxis=dict(title='Size of container on first dimension'),
            # type = log OR linear
            # https://github.com/d3/d3-format/blob/main/README.md#locale_format
            yaxis=dict(title=perf_monitor_name.split('_')[0],
                       exponentformat="e",
                       type='log'),
        )
        perf_scatters.append(plotly.graph_objs.Figure(
            data=perf_monitors, layout=layout))
    return perf_scatters


PATH_CSV = pathlib.Path('.') / "results" / "csv"
PATH_SAVE = pathlib.Path('.') / "results"

if not PATH_CSV.exists():
    raise FileNotFoundError(f"\"{PATH_CSV.absolute()}\"", "do not exist")


def read_stencil_bench() -> list:
    bench_results_areas: list = []
    for build in stencils_build:
        for _, setups in setup_benchs.items():
            print(f"Reading {PATH_CSV.absolute()}/stencil_{build}.csv")
            result = read_bench_file(
                f"{PATH_CSV.absolute()}/stencil_{build}.csv", setups)
            bench_results_areas.append(result)
    return bench_results_areas


def read_map_bench() -> list:
    mylist: list = []
    for recursion in recursions:
        for list_type in list_types:
            for build in map_build:
                print(f"Reading {build}-{recursion}-{map_types_key}-{list_type}")
                mylist.append(
                    f"{build}-{recursion}-{map_types_key}-{list_type}")
    groups = [list(i) for _, i in itertools.groupby(mylist,
                                                    lambda a: a.split('-')[1])]
    grouped = map(lambda X: [list(i)
                             for _, i in itertools.groupby(X, lambda a: a.split('-')[3])], groups)

    bench_results_areas_group: list = []
    for recursive_groups in grouped:
        for value_types in recursive_groups:
            for parameters in value_types:
                params = parameters.split('-')
                for _, setups in setup_benchs.items():
                    bench_results_areas: dict = read_bench_file(
                        f"{PATH_CSV.absolute()}/map_{parameters}.csv", setups)
                    for key, vals in bench_results_areas.items():
                        for bench_type in vals:
                            bench_type[0] += f"_{key}-{params[1]}-{params[3]}"
                        bench_results_areas_group.append({parameters: vals})
    return bench_results_areas_group


def save(results: list, path: pathlib.Path, file_type: str) -> None:
    if not path.exists():
        path.mkdir(parents=True)
    plotted = plotting(results)
    for perf_scatter in plotted:
        image_name: str = perf_scatter.layout.title.text
        perf_scatter.layout.title.text = None
        for char in [' ', '/']:
            if char in image_name:
                image_name = image_name.replace(char, '_')
        image_name = image_name.replace('[', '').replace(']','')
        perf_scatter.write_image(
            f"{path.absolute()}/{image_name}.{file_type}")


def main():
    print(sys.argv)
    results_nbr = sys.argv[2] if len(sys.argv) > 2 else ""
    for file_type in file_types:
        if sys.argv[1] == "stencil":
            bench_results: dict = {"stencil": read_stencil_bench()}
        if sys.argv[1] == "map":
            bench_results: dict = {"map": read_map_bench()}
        for name, results in bench_results.items():
            save(results, PATH_SAVE / file_type / name / results_nbr, file_type)
    pass


# %%
if __name__ == "__main__":
    main()
    pass
