
proc cast_types() =
  let a = int(float(1))
  echo a

proc cast_ctypes() =
  let a = int16(1)
  let b = a
  echo b
  let c = int64(1)
  let d = c
  echo d
  let e = uint64(1)
  let f = e
  echo f

proc main() =
  cast_types()
  cast_ctypes()

main()
