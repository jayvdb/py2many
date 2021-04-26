from enum import IntEnum, IntFlag, auto


class Colors(IntEnum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


class Permissions(IntFlag):
    R = 1
    W = 2
    X = 16


def show():
    color_map = {Colors.RED: "red", Colors.GREEN: "green", Colors.BLUE: "blue"}
    a = Colors.GREEN
    if a == Colors.GREEN:
        print("green")
    else:
        print("Not green")
    b = Permissions.R | Permissions.W
    if b & Permissions.R:
        print("R")
    else:
        print("Not R")
    if b & Permissions.W:
        print("W")
    else:
        print("Not W")
    if b & Permissions.X:
        print("X")
    else:
        print("Not X")


if __name__ == "__main__":
    show()
