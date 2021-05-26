
proc foo() =
  let a = 10
  let b = 20
  let c1 = (a + b)
  assert(c1 == 30)
  let c2 = (a - b)
  assert(c2 == -10)
  let c3 = (a * b)
  assert(c3 == 200)
  let c4 = (a / b)
  assert(c4 == 0.5)
  let c5 = -(a)
  assert(c5 == -10)
  let d = 2.0
  let e1 = (float64(a) + d)
  assert(e1 == 12.0)
  let e2 = (float64(a) - d)
  assert(e2 == 8.0)
  let e3 = (float64(a) * d)
  assert(e3 == 20.0)
  let e4 = (float64(a) / d)
  assert(e4 == 5.0)
  let f = -3.0
  assert(f < -2.9)

proc add1(x: int8, y: int8): int16 =
  return int16((x + y))

proc add2(x: int16, y: int16): int32 =
  return int32((x + y))

proc add3(x: int32, y: int32): int64 =
  return int64((x + y))

proc add4(x: int64, y: int64): int64 =
  return (x + y)

proc add5(x: uint8, y: uint8): uint16 =
  return uint16((x + y))

proc add6(x: uint16, y: uint16): uint32 =
  return uint32((x + y))

proc add7(x: uint32, y: uint32): uint64 =
  return uint64((x + y))

proc add8(x: uint64, y: uint64): uint64 =
  return (x + y)

proc add9(x: int8, y: uint16): uint32 =
  return uint32((uint16(x) + y))

proc sub(x: int8, y: int8): int8 =
  return (x - y)

proc mul(x: int8, y: int8): int16 =
  return int16((x * y))

proc fadd1(x: int8, y: float64): float64 =
  return (float64(x) + y)

proc show() =
  foo()
  assert(fadd1(6, 6.0) == 12)
  echo "OK"

proc main() =
  foo()
  show()

main()
