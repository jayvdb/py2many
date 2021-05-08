#include "py14/runtime/builtins.h" // NOLINT(build/include_order)
#include "py14/runtime/sys.h"      // NOLINT(build/include_order)
#include <iostream>                // NOLINT(build/include_order)

inline void show() {
  auto myfunc = [](auto x, auto y) { return x + y; };
  std::cout << myfunc(1, 2);
  std::cout << std::endl;
}

int main(int argc, char **argv) {
  py14::sys::argv = std::vector<std::string>(argv, argv + argc);
  show();
}
