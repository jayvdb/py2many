
fun cast_types() {
    val a = 1.toDouble().toInt()
    println("$a")
}

fun cast_ctypes() {
    val a = 1.toShort()
    val b = a
    println("$b")
    val c = 1.toLong()
    val d = c
    println("$d")
    val e = 1.toULong()
    val f = e
    println("$f")
}

fun main(argv: Array<String>) {
    cast_types()
    cast_ctypes()
}
