// @dart=2.9
import 'package:sprintf/sprintf.dart';

foo() {
  final int a = 10;
  final int b = 20;
  final int c1 = (a + b);
  assert(c1 == 30);
  final int c2 = (a - b);
  assert(c2 == -10);
  final int c3 = (a * b);
  assert(c3 == 200);
  final int c4 = (a ~/ b);
  assert(c4 == 0.5);
  final int c5 = -(a);
  assert(c5 == -10);
  final double d = 2.0;
  final double e1 = (a + d);
  assert(e1 == 12.0);
  final double e2 = (a - d);
  assert(e2 == 8.0);
  final double e3 = (a * d);
  assert(e3 == 20.0);
  final double e4 = (a / d);
  assert(e4 == 5.0);
  final double f = -3.0;
  assert(f < -2.9);
}

int add1(int x, int y) {
  return (x + y);
}

int add2(int x, int y) {
  return (x + y);
}

int add3(int x, int y) {
  return (x + y);
}

int add4(int x, int y) {
  return (x + y);
}

int add5(int x, int y) {
  return (x + y);
}

int add6(int x, int y) {
  return (x + y);
}

int add7(int x, int y) {
  return (x + y);
}

int add8(int x, int y) {
  return (x + y);
}

int add9(int x, int y) {
  return (x + y);
}

int sub(int x, int y) {
  return (x - y);
}

int mul(int x, int y) {
  return (x * y);
}

double fadd1(int x, double y) {
  return (x + y);
}

show() {
  foo();
  assert(fadd1(6, 6.0) == 12);
  print(sprintf("%s", ["OK"]));
}

main(List<String> argv) {
  foo();
  show();
}
