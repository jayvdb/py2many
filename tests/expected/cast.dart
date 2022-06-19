// @dart=2.9
import 'package:sprintf/sprintf.dart';

cast_types() {
  final int a = 1.toDouble().toInt();
  print(sprintf("%s", [a]));
}

cast_ctypes() {
  final int a = 1.toInt();
  final b = a;
  print(sprintf("%s", [b]));
  final int c = 1.toInt();
  final d = c;
  print(sprintf("%s", [d]));
  final int e = 1.toInt();
  final f = e;
  print(sprintf("%s", [f]));
}

main(List<String> argv) {
  cast_types();
  cast_ctypes();
}
