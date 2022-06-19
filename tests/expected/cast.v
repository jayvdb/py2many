[translated]
module main

fn cast_types() {
	a := int(f64(1))
	println(a.str())
}

fn cast_ctypes() {
	a := i16(1)
	b := a
	println(b.str())
	c := i64(1)
	d := c
	println(d.str())
	e := u64(1)
	f := e
	println(f.str())
}

fn main() {
	cast_types()
	cast_ctypes()
}
