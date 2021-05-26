#include <cassert>   // NOLINT(build/include_order)
#include <iostream>  // NOLINT(build/include_order)

#include "pycpp/runtime/builtins.h"  // NOLINT(build/include_order)
#include "pycpp/runtime/sys.h"       // NOLINT(build/include_order)

inline void foo() {
  int a = 10;
  int b = 20;
  int c1 = a + b;
  assert(c1 == 30);
  int c2 = a - b;
  assert(c2 == -10);
  int c3 = a * b;
  assert(c3 == 200);
  double c4 = a / b;
  assert(c4 == 0.5);
  int c5 = -(a);
  assert(c5 == -10);
  double d = 2.0;
  double e1 = a + d;
  assert(e1 == 12.0);
  double e2 = a - d;
  assert(e2 == 8.0);
  double e3 = a * d;
  assert(e3 == 20.0);
  double e4 = a / d;
  assert(e4 == 5.0);
  double f = -3.0;
  assert(f < -2.9);
}

inline int16_t add1(int8_t x, int8_t y) { return x + y; }

inline int32_t add2(int16_t x, int16_t y) { return x + y; }

inline int64_t add3(int32_t x, int32_t y) { return x + y; }

inline int64_t add4(int64_t x, int64_t y) { return x + y; }

inline uint16_t add5(uint8_t x, uint8_t y) { return x + y; }

inline uint32_t add6(uint16_t x, uint16_t y) { return x + y; }

inline uint64_t add7(uint32_t x, uint32_t y) { return x + y; }

inline uint64_t add8(uint64_t x, uint64_t y) { return x + y; }

inline uint32_t add9(int8_t x, uint16_t y) { return x + y; }

inline int8_t sub(int8_t x, int8_t y) { return x - y; }

inline int16_t mul(int8_t x, int8_t y) { return x * y; }

inline double fadd1(int8_t x, double y) { return x + y; }

inline void show() {
  foo();
  assert(fadd1(6, 6.0) == 12);
  std::cout << std::string{"OK"};
  std::cout << std::endl;
}

int main(int argc, char** argv) {
  pycpp::sys::argv = std::vector<std::string>(argv, argv + argc);
  foo();
  show();
}
