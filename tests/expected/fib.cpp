#include "py14/runtime/builtins.h" // NOLINT(build/include_order)
#include "py14/runtime/sys.h"      // NOLINT(build/include_order)
#include <iostream>                // NOLINT(build/include_order)
inline int fib(int i) {
  if (i == 0 || i == 1) {
    return 1;
  }
  return (fib(i - 1)) + (fib(i - 2));
}

int main(int argc, char **argv) {
  py14::sys::argv = std::vector<std::string>(argv, argv + argc);
  int rv = fib(5);
  std::cout << rv;
  std::cout << std::endl;
}
