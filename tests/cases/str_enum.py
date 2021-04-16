from enum import Enum


class Colors(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


def show():
    print(Colors.RED.value)
    print(Colors.GREEN.value)
    print(Colors.BLUE.value)


if __name__ == "__main__":
    show()
