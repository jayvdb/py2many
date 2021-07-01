#!/usr/bin/env python3


def nested_containers():
    codes = {"KEY": [1, 3]}
    return 1 in codes["KEY"]


if __name__ == "__main__":
    if nested_containers():
        print("OK")
