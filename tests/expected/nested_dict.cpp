#include "py14/runtime/builtins.h" // NOLINT(build/include_order)
#include "py14/runtime/sys.h"      // NOLINT(build/include_order)
#include <algorithm>               // NOLINT(build/include_order)
#include <iostream>                // NOLINT(build/include_order)
#include <map>                     // NOLINT(build/include_order)
#include <vector>                  // NOLINT(build/include_order)
inline bool nested_containers() {
  std::map<std::string, std::vector<int>> CODES =
      std::map<std::string, std::vector<int>>{
          {std::string{"KEY"}, std::vector<int>{1, 3}}};
  return (std::find(CODES[std::string{"KEY"}].begin(),
                    CODES[std::string{"KEY"}].end(),
                    1) != CODES[std::string{"KEY"}].end());
}

int main(int argc, char **argv) {
  py14::sys::argv = std::vector<std::string>(argv, argv + argc);
  if (nested_containers()) {
    std::cout << std::string{"OK"};
    std::cout << std::endl;
  }
}
