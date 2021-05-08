#include "py14/runtime/builtins.h" // NOLINT(build/include_order)
#include "py14/runtime/sys.h"      // NOLINT(build/include_order)
#include <cassert>                 // NOLINT(build/include_order)
#include <iostream>                // NOLINT(build/include_order)

class Rectangle {
public: // NOLINT(whitespace/indent)
  int height;
  int length;

  Rectangle(int height, int length) {
    this->height = height;
    this->length = length;
  }
  inline bool is_square() { return this->height == this->length; }
};

inline void show() {
  Rectangle r = Rectangle(1, 1);
  assert(r.is_square());
  r = Rectangle(1, 2);
  assert(!(r.is_square()));
  std::cout << r.height;
  std::cout << std::endl;
  std::cout << r.length;
  std::cout << std::endl;
}

int main(int argc, char **argv) {
  py14::sys::argv = std::vector<std::string>(argv, argv + argc);
  show();
}
