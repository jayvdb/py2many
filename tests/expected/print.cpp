#include "py14/runtime/builtins.h" // NOLINT(build/include_order)
#include "py14/runtime/sys.h"      // NOLINT(build/include_order)
#include <iostream>                // NOLINT(build/include_order)
inline void show() {
  std::cout << std::string{"b"};
  std::cout << std::endl;
  std::cout << 2;
  std::cout << " ";
  std::cout << std::string{"b"};
  std::cout << std::endl;
  double a = 2.1;
  std::cout << a;
  std::cout << std::endl;
  double b = 2.1;
  std::cout << b;
  std::cout << std::endl;
}

int main(int argc, char **argv) {
  py14::sys::argv = std::vector<std::string>(argv, argv + argc);
  show();
}
