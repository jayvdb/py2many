#include "py14/runtime/builtins.h" // NOLINT(build/include_order)
#include "py14/runtime/range.hpp"  // NOLINT(build/include_order)
#include "py14/runtime/sys.h"      // NOLINT(build/include_order)
#include <algorithm>               // NOLINT(build/include_order)
#include <cassert>                 // NOLINT(build/include_order)
#include <iostream>                // NOLINT(build/include_order)
#include <map>                     // NOLINT(build/include_order)
#include <set>                     // NOLINT(build/include_order)
#include <vector>                  // NOLINT(build/include_order)

inline void do_pass() {
/* pass */}

inline void inline_pass() {
/* pass */}

inline int indexing() {
  int sum = 0;
  std::vector<int> a = {};
  for (auto i : rangepp::xrange(10)) {
    a.push_back(i);
    sum += a[i];
  }
  return sum;
}

inline auto infer_bool(int code) {
  return ({
    std::vector<int> __tmp1 = {1, 2, 4};
    (std::find(__tmp1.begin(), __tmp1.end(), code) != __tmp1.end());
  });
}

inline void show() {
  int a1 = 10;
  int b9 = 2;
  int b2 = 2;
  assert(b2 == b9);
  double a2 = 2.1;
  std::cout << a2;
  std::cout << std::endl;
  for (auto i : rangepp::xrange(0, 10)) {
    std::cout << i;
    std::cout << std::endl;
  }
  for (auto i : rangepp::xrange(0, 10, 2)) {
    std::cout << i;
    std::cout << std::endl;
  }
  int a3 = -(a1);
  int a4 = a3 + a1;
  std::cout << a4;
  std::cout << std::endl;
  int sum1 = indexing();
  std::cout << sum1;
  std::cout << std::endl;
  std::vector<int> a5 = {1, 2, 3};
  std::cout << a5.size();
  std::cout << std::endl;
  std::vector<std::string> a9 = std::vector<std::string>{
      std::string{"a"}, std::string{"b"}, std::string{"c"}, std::string{"d"}};
  std::cout << a9.size();
  std::cout << std::endl;
  std::set<int> a6 = std::set<int>{1, 2, 3, 4};
  std::cout << a6.size();
  std::cout << std::endl;
  std::map<std::string, int> a7 =
      std::map<std::string, int>{{std::string{"a"}, 1}, {std::string{"b"}, 2}};
  std::cout << a7.size();
  std::cout << std::endl;
  bool a8 = true;
  if (a8) {
    std::cout << std::string{"true"};
    std::cout << std::endl;
  } else {
    if (a4 > 0) {
      std::cout << std::string{"never get here"};
      std::cout << std::endl;
    }
  }
  if (a1 == 11) {
    std::cout << std::string{"false"};
    std::cout << std::endl;
  } else {
    std::cout << std::string{"true"};
    std::cout << std::endl;
  }
  if (1 != NULL) {
    std::cout << std::string{"World is sane"};
    std::cout << std::endl;
  }
  do_pass();
  inline_pass();
  std::string s = std::string{"1    2"};
  std::cout << s;
  std::cout << std::endl;
}

int main(int argc, char **argv) {
  py14::sys::argv = std::vector<std::string>(argv, argv + argc);
  show();
}
