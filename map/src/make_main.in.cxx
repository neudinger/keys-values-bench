#define PARENS ()
#define EXPAND(arg) EXPAND1(EXPAND1(EXPAND1(EXPAND1(arg))))
#define EXPAND1(arg) EXPAND2(EXPAND2(EXPAND2(EXPAND2(arg))))
#define EXPAND2(arg) EXPAND3(EXPAND3(EXPAND3(EXPAND3(arg))))
#define EXPAND3(arg) EXPAND4(EXPAND4(EXPAND4(EXPAND4(arg))))
#define EXPAND4(arg) arg

#define FOR_EACHM(macro, ...) __VA_OPT__(EXPAND(FOR_EACH_HELPERM(macro, __VA_ARGS__)))
#define FOR_EACH_HELPERM(macro, a1, a2, ...) macro(a1, a2) __VA_OPT__(FOR_EACH_AGAINM PARENS(macro, a2##V, __VA_ARGS__))
#define FOR_EACH_AGAINM() FOR_EACH_HELPERM

#define NESTED_FOR_MAP_KV(map, k) for (auto const &[k, k##V] : map)

#define FOR_EACHS(macro, assignedvalue, ...)                                                                           \
    macro __VA_OPT__(EXPAND(FOR_EACH_HELPERS(macro, assignedvalue, __VA_ARGS__))) = assignedvalue
#define FOR_EACH_HELPERS(macro, assignedvalue, a1, ...)                                                                \
    [a1] __VA_OPT__(FOR_EACH_AGAINS PARENS(macro, assignedvalue, __VA_ARGS__))
#define FOR_EACH_AGAINS() FOR_EACH_HELPERS

#define FOR_EACH(macro, ...) __VA_OPT__(EXPAND(FOR_EACH_HELPER(macro, __VA_ARGS__)))
#define FOR_EACH_HELPER(macro, a1, ...) macro(a1) __VA_OPT__(FOR_EACH_AGAIN PARENS(macro, __VA_ARGS__))
#define FOR_EACH_AGAIN() FOR_EACH_HELPER

#define MAPER(macro, name_list, ...) __VA_OPT__(EXPAND(MAP_HELPER(macro, name_list, __VA_ARGS__)))
#define MAP_HELPER(macro, listname, a1, ...)                                                                           \
    macro(a1, listname) __VA_OPT__(MAP_AGAIN PARENS(macro, listname, __VA_ARGS__))
#define MAP_AGAIN() MAP_HELPER
#define NESTED_FOR(val, vals) for (auto &val : vals)

#if !defined(TYPES)
#define TYPES uint64_t, uint64_t, uint64_t
#endif // TYPES
#if !defined(LIST_TYPE)
#define LIST_TYPE uint64_t
#endif // LIST_TYPE
#if !defined(KEYNAMES)
#define KEYNAMES k1, k2
#endif // KEYNAMES
#if !defined(MAP_VALUE)
// #define MAP_VALUE generateRandomId(K1)
#define MAP_VALUE k1
#endif // MAP_VALUE
#if !defined(RECURSION)
// #define RECURSION generateRandomId(K1)
#define RECURSION 1
#endif // RECURSION

int main(int argc, char **argv)
{
    ssize_t nb_elems = 200;
    if (argc >= 2)
    {
        nb_elems = atoll(argv[1]);

        if (!(nb_elems))
        {
            std::cerr << "Input parameters errors" << std::endl;
            exit(-1);
        }
    }
    // Type
    MAP_TYPES(TYPES)::type map;
    // Generate integer
    std::list<uint64_t> valuesNbr(nb_elems);
    std::default_random_engine re(std::chrono::system_clock::now().time_since_epoch().count());
    std::uniform_int_distribution<uint64_t> uid(std::numeric_limits<uint64_t>::min(),
                                                std::numeric_limits<uint64_t>::max());
    std::generate(valuesNbr.begin(), valuesNbr.end(), std::bind(uid, re));
    // if constexpr (std::is_same<LIST_TYPE, std::string>::value)
    // {}
    // else if constexpr (std::is_integral<LIST_TYPE>::value)
    valuesNbr.sort();
    valuesNbr.unique();
    const std::string params = std::to_string(nb_elems) + "-" + std::to_string((uint64_t)std::pow(nb_elems, RECURSION));
    std::string marker = "WRITE-" + params;
    LIKWID_MARKER_INIT;
    LIKWID_MARKER_THREADINIT;
    LIKWID_MARKER_START(marker.c_str());
    MAPER(NESTED_FOR, valuesNbr, KEYNAMES)
    {
        FOR_EACHS(map, MAP_VALUE, KEYNAMES);
    }
    LIKWID_MARKER_STOP(marker.c_str());
    marker = "READ-" + params;
    uint64_t incr = 0;
    LIKWID_MARKER_START(marker.c_str());
    FOR_EACHM(NESTED_FOR_MAP_KV, map, KEYNAMES)
    {
        incr += 1;
    }
    LIKWID_MARKER_STOP(marker.c_str());
    LIKWID_MARKER_CLOSE;
    return 0;
}

/*
https://github.com/pfultz2/Cloak/wiki/C-Preprocessor-tricks,-tips,-and-idioms
https://www.scs.stanford.edu/~dm/blog/va-opt.html
c++ -std=c++2a -E make_enum.cc > make_enum.cpp
c++ -std=c++2a -E make_enum.cc > make_enum.cpp && sed -i '1i#include <iostream>' make_enum.cpp && c++ make_enum.cpp &&
./a.out Local Variables: c-macro-preprocessor: "c++ -x c++ -std=c++20 -E -" End:
*/