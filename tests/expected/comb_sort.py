from typing import Callable, Dict, List, Set, Optional
from ctypes import c_int8 as i8, c_int16 as i16, c_int32 as i32, c_int64 as i64
from ctypes import c_uint8 as u8, c_uint16 as u16, c_uint32 as u32, c_uint64 as u64
import sys
from ctypes import c_size_t, c_int32, c_uint64
from math import floor
from typing import List


def comb_sort(seq: List[int]) -> List[int]:
    gap: c_size_t = len(seq)
    swap: bool = True
    while gap > 1 or swap:
        n: c_int32 = c_int32(floor(gap / 1.25))
        gap = int(max(float(1), float(n.value)))
        swap = False
        for i in range(len(seq) - gap):
            if seq[i] > seq[i + gap]:
                if True:
                    (__tmp1, __tmp2) = (seq[i + gap], seq[i])
                    seq[i] = __tmp1
                    seq[i + gap] = __tmp2
                swap = True
    return seq


if __name__ == "__main__":
    unsorted: List[int] = [14, 11, 19, 5, 16, 10, 19, 12, 5, 12]
    expected: List[int] = [5, 5, 10, 11, 12, 12, 14, 16, 19, 19]
    assert comb_sort(unsorted) == expected
    print("OK")
