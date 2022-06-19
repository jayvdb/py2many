[translated]
module main

import arrays
import math

fn comb_sort(mut seq []int) []int {
	mut gap := seq.len
	mut swap := true
	for gap > 1 || swap {
		n := int(int(math.floor((f64(gap) / 1.25))))
		gap = int(arrays.max([f64(1), f64(n)]) or { panic('!') })
		swap = false
		for i in 0 .. (seq.len - gap) {
			if seq[i] > seq[(i + gap)] {
				seq[i], seq[(i + gap)] = seq[(i + gap)], seq[i]
				swap = true
			}
		}
	}
	return seq
}

fn main() {
	mut unsorted := [14, 11, 19, 5, 16, 10, 19, 12, 5, 12]
	expected := [5, 5, 10, 11, 12, 12, 14, 16, 19, 19]
	assert comb_sort(mut unsorted) == expected
	println('OK')
}
