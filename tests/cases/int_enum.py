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
    print(Colors.RED.value)
    print(Colors.GREEN.value)
    print(Colors.BLUE.value)
    #for perm in Permissions:
    #    print(perm)
    #    print(perm.value)


if __name__ == "__main__":
    show()
