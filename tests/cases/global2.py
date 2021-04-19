code_0 = 0
code_1 = 1

code_a = "a"
code_b = "b"

l_b = {
    code_a,
}

l_c = {
    code_b: code_0,
}

if __name__ == "__main__":
    for i in l_b:
        print(i)
    # Dereferencing items in the dict fails on Rust.
