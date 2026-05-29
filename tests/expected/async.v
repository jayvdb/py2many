@[translated]
module main

fn async_gen() chan int {
	ch := chan int{cap: 100}
	spawn fn [ch] () {
		defer { ch.close() }
		for i in 0 .. 3 {
			ch <- i
		}
	}()
	return ch
}

fn show_async() {
	// WARNING: async for converted to sync for
	for val in async_gen() {
		println(val.str())
	}
}

fn show() {
	asyncio.run(show_async())
}

fn main() {
	show()
}
