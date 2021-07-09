from typing import List


def indexing():
    sum = 0
    a: List[int] = []
    for i in range(10):
        a.append(i)
        sum += a[i]
    return sum


def infer_bool(code: int):
    return code in [1, 2, 4]


def show():
    # assign
    a1 = 10
    # multi-assign
    b1 = b2 = 15
    assert b1 == 15
    assert b2 == 15
    b9 = 2
    b10 = 2
    assert b9 == b10
    # annotated assign
    a2: float = 2.1
    print(a2)
    # for loop
    print("range(0, 10")
    for i in range(0, 10):
        print(i)
    print("range(0, 10, 2")
    for i in range(0, 10, 2):
        print(i)
    print("range end")
    # for i in range(1, 10):
    #     print(i)
    # unary op
    a3 = -a1
    # binary op
    a4 = a3 + a1
    print(a4)
    # ternary op
    t1 = 10 if a1 > 5 else 5
    assert t1 == 10
    sum1 = indexing()
    print(sum1)
    # lists, sets and dict
    a5 = [1, 2, 3]
    print(len(a5))
    a9: List[str] = ["a", "b", "c", "d"]
    print(len(a9))
    a7 = {"a": 1, "b": 2}
    print(len(a7))
    a8 = True
    # print()
    if a8:
        print("true")
    elif a4 > 0:
        print("never get here")
    if a1 == 11:
        print("false")
    else:
        print("true")
    if 1 != None:
        print("World is sane")
    print(True)
    if True:
        a1 += 1
    assert a1 == 11
    if True:
        print("true")
    s = "1\
    2"
    print(s)
    assert infer_bool(1)
    # assert 1 != 2 != 3
    # Escape quotes
    _escape_quotes = """ foo "bar" baz """
    (_c1, _, _c2) = (1, 2, 3)


if __name__ == "__main__":
    show()
