#!/usr/bin/env python3
from ctypes import c_size_t, c_int32, c_uint64
from math import floor
from typing import List


def comb_sort(seq: List[int]) -> List[int]:
    gap: c_size_t = len(seq)
    swap = True
    while gap > 1 or swap:
        n: c_int32 = c_int32(floor(gap / 1.25))
        gap = int(max(1, float(n.value)))
        swap = False
        for i in range(len(seq) - gap):
            if seq[i] > seq[i + gap]:
                seq[i], seq[i + gap] = seq[i + gap], seq[i]
                swap = True
    return seq


if __name__ == "__main__":
    unsorted = [14, 11, 19, 5, 16, 10, 19, 12, 5, 12]
    expected = [5, 5, 10, 11, 12, 12, 14, 16, 19, 19]

    assert comb_sort(unsorted) == expected
    print("OK")
