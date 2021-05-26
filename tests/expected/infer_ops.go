package main

import (
	"fmt"
)

func Foo() {
	var a int = 10
	var b int = 20
	var c1 int = (a + b)
	if !(c1 == 30) {
		panic("assert")
	}
	var c2 int = (a - b)
	if !(c2 == -10) {
		panic("assert")
	}
	var c3 int = (a * b)
	if !(c3 == 200) {
		panic("assert")
	}
	var c4 float64 = float64((a / b))
	if !(c4 == 0.5) {
		panic("assert")
	}
	var c5 int = -(a)
	if !(c5 == -10) {
		panic("assert")
	}
	var d float64 = 2.0
	var e1 float64 = (float64(a) + d)
	if !(e1 == 12.0) {
		panic("assert")
	}
	var e2 float64 = (float64(a) - d)
	if !(e2 == 8.0) {
		panic("assert")
	}
	var e3 float64 = (float64(a) * d)
	if !(e3 == 20.0) {
		panic("assert")
	}
	var e4 float64 = (float64(a) / d)
	if !(e4 == 5.0) {
		panic("assert")
	}
	var f float64 = -3.0
	if !(f < -2.9) {
		panic("assert")
	}
}

func Add1(x int8, y int8) int16 {
	return int16((x + y))
}

func Add2(x int16, y int16) int32 {
	return int32((x + y))
}

func Add3(x int32, y int32) int64 {
	return int64((x + y))
}

func Add4(x int64, y int64) int64 {
	return (x + y)
}

func Add5(x uint8, y uint8) uint16 {
	return uint16((x + y))
}

func Add6(x uint16, y uint16) uint32 {
	return uint32((x + y))
}

func Add7(x uint32, y uint32) uint64 {
	return uint64((x + y))
}

func Add8(x uint64, y uint64) uint64 {
	return (x + y)
}

func Add9(x int8, y uint16) uint32 {
	return uint32((uint16(x) + y))
}

func Sub(x int8, y int8) int8 {
	return (x - y)
}

func Mul(x int8, y int8) int16 {
	return int16((x * y))
}

func Fadd1(x int8, y float64) float64 {
	return (float64(x) + y)
}

func Show() {
	Foo()
	if !(Fadd1(6, 6.0) == 12) {
		panic("assert")
	}
	fmt.Printf("%v\n", "OK")
}

func main() {
	Foo()
	Show()
}
