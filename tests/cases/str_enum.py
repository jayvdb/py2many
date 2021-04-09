from enum import Enum


class ColorNames(str, Enum):
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"


def show():
	for color in ColorNames:
		print(color)
		print(color.value)


if __name__ == "__main__":
	show()
