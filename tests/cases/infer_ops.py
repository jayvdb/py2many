#!/usr/bin/env python3

from ctypes import (
    c_int8,
    c_int16,
    c_int32,
    c_int64,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
)


def foo():
    a = 10
    b = 20
    c1 = a + b
    assert c1 == 30
    c2 = a - b
    assert c2 == -10
    c3 = a * b
    assert c3 == 200
    c4 = a / b
    assert c4 == 0.5
    c5 = -a
    assert c5 == -10
    d = 2.0
    e1 = a + d
    assert e1 == 12.0
    e2 = a - d
    assert e2 == 8.0
    e3 = a * d
    assert e3 == 20.0
    e4 = a / d
    assert e4 == 5.0
    f = -3.0
    assert f < -2.9


def add1(x: c_int8, y: c_int8):
    return x + y


def add2(x: c_int16, y: c_int16):
    return x + y


def add3(x: c_int32, y: c_int32):
    return x + y


def add4(x: c_int64, y: c_int64):
    return x + y


def add5(x: c_uint8, y: c_uint8):
    return x + y


def add6(x: c_uint16, y: c_uint16):
    return x + y


def add7(x: c_uint32, y: c_uint32):
    return x + y


def add8(x: c_uint64, y: c_uint64):
    return x + y


def add9(x: c_int8, y: c_uint16):
    return x + y


def sub(x: c_int8, y: c_int8):
    return x - y


def mul(x: c_int8, y: c_int8):
    return x * y


def fadd1(x: c_int8, y: float):
    return x + y


def show():
    foo()
    assert fadd1(6, 6.0) == 12
    # assert add1(127, 1) == 128
    # assert add2(32767, 1) == 32768
    # assert add3(2147483647, 1) == 2147483648
    # assert add4(9223372036854775807, 1) == 9223372036854775808
    print("OK")


if __name__ == "__main__":
    foo()
    show()
