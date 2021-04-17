const code_0 = 0
const code_1 = 1
const l_a = @[code_0, code_1]
const code_a = "a"
const code_b = "b"
const l_b = @[code_a, code_b]
proc main() =
  for i in l_a:
    echo i
  for i in l_b:
    echo i

main()
