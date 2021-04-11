from enum import Enum


class Colors(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


def show():
	for color in ColorNames:
		print(color)
		print(color.value)


if __name__ == "__main__":
	show()