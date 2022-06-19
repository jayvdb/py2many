
function cast_types()
    a = Int64(floor(float(1)))
    println(join([a], " "))
end

function cast_ctypes()
    a = convert(Int16, 1)
    b = a
    println(join([b], " "))
    c = convert(Int64, 1)
    d = c
    println(join([d], " "))
    e = convert(UInt64, 1)
    f = e
    println(join([f], " "))
end

function main()
    cast_types()
    cast_ctypes()
end

main()
