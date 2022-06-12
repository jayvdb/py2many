
function bubble_sort(seq::Array{Int64})::Array{Int64}
    L::Int64 = length(seq)
    start::Int64 = 1
    for _ in (0:L-1)
        for n in (start:L-1)
            if seq[n+1] < seq[(n-1)+1]
                seq[(n-1)+1], seq[n+1] = (seq[n+1], seq[(n-1)+1])
            end
        end
    end
    return seq
end

function main()
    unsorted = [14, 11, 19, 5, 16, 10, 19, 12, 5, 12]
    expected = [5, 5, 10, 11, 12, 12, 14, 16, 19, 19]
    @assert(bubble_sort(unsorted) == expected)
    println(join(["OK"], " "))
end

main()
