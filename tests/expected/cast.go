package main

import (
	"fmt"
)

func CastTypes() {
	var a int = int(float64(1))
	fmt.Printf("%v\n", a)
}

func CastCtypes() {
	var a int16 = int16(1)
	b := a
	fmt.Printf("%v\n", b)
	var c int64 = int64(1)
	d := c
	fmt.Printf("%v\n", d)
	var e uint64 = uint64(1)
	f := e
	fmt.Printf("%v\n", f)
}

func main() {
	CastTypes()
	CastCtypes()
}
