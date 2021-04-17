from enum import IntEnum, IntFlag, auto


class Colors(IntEnum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


#class Permissions(IntFlag):
#    R = 1
#    W = 2
#    X = 16


def show():
    assert Colors.RED is not None
    #assert int(Colors.GREEN) == 2
    #assert int(Colors.BLUE) == 3
    print("OK")
    #for perm in Permissions:
    #    print(perm)
    #    print(perm.value)


if __name__ == "__main__":
    show()
