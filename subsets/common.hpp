#pragma once

#include "hackycpp.hpp"

static inline int hw(uint64_t x) {
    return __builtin_popcountll(x);
}

static inline int log2(uint64_t n) {
    ensure((n & (n - 1)) == 0);
    ensure(n != 0);
    int ret = __builtin_ctzll(n);
    ensure((1ull << ret) == n);
    return ret;
}

static inline int log3(uint64_t n) {
    ensure(n != 0);
    int ret = 0;
    while (n > 1) {
        ret += 1;
        n /= 3;
    }
    return ret;
}

static const uint64_t TABLE_POW3[41] = {1ull,3ull,9ull,27ull,81ull,243ull,729ull,2187ull,6561ull,19683ull,59049ull,177147ull,531441ull,1594323ull,4782969ull,14348907ull,43046721ull,129140163ull,387420489ull,1162261467ull,3486784401ull,10460353203ull,31381059609ull,94143178827ull,282429536481ull,847288609443ull,2541865828329ull,7625597484987ull,22876792454961ull,68630377364883ull,205891132094649ull,617673396283947ull,1853020188851841ull,5559060566555523ull,16677181699666569ull,50031545098999707ull,150094635296999121ull,450283905890997363ull,1350851717672992089ull,4052555153018976267ull,12157665459056928801ull};
static inline uint64_t pow3(int e) {
    ensure(0 <= e && e <= 40);
    return TABLE_POW3[e];
}