from enum import Enum


class Colors(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


def show():
    assert str(Colors.RED) == "red", str(Colors.RED)
    assert str(Colors.GREEN) == "green"
    assert str(Colors.BLUE) == "blue"
    print("OK")


if __name__ == "__main__":
    show()
