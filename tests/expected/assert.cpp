#include "py14/runtime/builtins.h"
#include "py14/runtime/sys.h"
#include <cassert>
template <typename T1, typename T2> void compare_assert(T1 a, T2 b) {
  assert(a == b);
}

int main(int argc, char *const argv[]) {
  py14::sys::argv = std::vector<std::string>(argv, argv + argc);
  compare_assert(1, 1);
}
