#!/usr/bin/env python3


def infer_int():
    a = 10
    # infer that b is an int
    b = a
    assert b == 10
    print(b)


def infer_arg_list(b):
    a = 'a'
    return b == a


#def infer_arg_set(b):
#    a = {'a'}
#    return b in a


if __name__ == "__main__":
    infer_int()
    assert infer_arg_list("a")
    #assert infer_arg_set("a")
