#if !defined(MAPPING)
#define MAPPING

#ifdef LIKWID_PERFMON
#include <likwid-marker.h>
#else
#define LIKWID_MARKER_INIT
#define LIKWID_MARKER_THREADINIT
#define LIKWID_MARKER_SWITCH
#define LIKWID_MARKER_REGISTER(regionTag)
#define LIKWID_MARKER_START(regionTag)
#define LIKWID_MARKER_STOP(regionTag)
#define LIKWID_MARKER_CLOSE
#define LIKWID_MARKER_GET(regionTag, nevents, events, time, count)
#endif

#define xstr(s) str(s)
#define str(s) #s

#if defined(STD)
#include <map>
#define MAP std::map
#elif defined(LLVM)
#include <llvm/ADT/DenseMap.h>
#define MAP llvm::DenseMap
#elif defined(LLVM_MAP_VECTOR)
#include <llvm/ADT/MapVector.h>
#define MAP llvm::MapVector
#define LLVM
#elif defined(BOOST)
#include <boost/container/map.hpp>
#define MAP boost::container::map
// #else
// #include <map>
// #define MAP std::map
#endif

#if defined(LLVM)
void llvm::deallocate_buffer(void *Ptr, size_t Size, size_t Alignment)
{
    operator delete(Ptr);
}
void *llvm::allocate_buffer(size_t Size, size_t Alignment)
{
    return operator new(Size);
}
#endif

#include <chrono>
#include <functional>
#include <iostream>
#include <iterator>
#include <list>
#include <random>

#define MAP_TYPES(...) MultiMap<__VA_ARGS__>

template<typename... Ts>
struct MultiMap;
template<typename V>
struct MultiMap<V>
{
    typedef V type;
};
template<typename TK, typename TKN, typename... Ts>
struct MultiMap<TK, TKN, Ts...>
{
    typedef MAP<TK, typename MultiMap<TKN, Ts...>::type> type;
    static const std::uint16_t size = sizeof...(Ts) + 2;
};

const inline std::string generateRandomId(const uint32_t &length = 0)
{
    static const std::string allowed_chars{"123456789BCDFGHJKLMNPQRSTVWXZbcdfghjklmnpqrstvwxz"};
    static thread_local std::default_random_engine randomEngine(std::random_device{}());
    static thread_local std::uniform_int_distribution<uint32_t> randomDistribution(0, allowed_chars.size() - 1);
    std::string id(length ? length : 32, '\0');
    for (std::string::value_type &c : id)
        c = allowed_chars[randomDistribution(randomEngine)];
    return id;
}

#endif // MAPPING