x_array = parse.(Float64, split("2.3,4.3", ","))

k = "2.07+3.2im"

t = replace(k, r"im"=>"")
r, i = parse.(Float64, split(t, "+"))
println(r)
println(i)

z = 2+3im
println(string(z))