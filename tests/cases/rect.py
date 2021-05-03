class Rectangle:

    def __init__(self, height=0, length=0):
        self.height = height
        self.length = length

    def is_square(self) -> bool:
        return self.height == self.length


def show():

    r = Rectangle()
    assert r.length == 0
    assert r.height == 0

    r = Rectangle(height=1, length=1)
    assert r.height == 1
    assert r.length == 1
    assert r.is_square()

    r = Rectangle(height=1, length=2)
    assert r.height == 1
    assert r.length == 2
    assert not r.is_square()

    print(r.height)
    print(r.length)


if __name__ == "__main__":
    show()
