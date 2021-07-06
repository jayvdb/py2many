#!/usr/bin/env python3


def do_unsupported():
    a = [1]
    x = a[0]
    print(x)
    b = 2
    del a
    print(b)


if __name__ == "__main__":
    do_unsupported()