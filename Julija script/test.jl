using Pkg;
Pkg.add("SchwarzChristoffel");
Pkg.add("Plots")

using SchwarzChristoffel;
using Plots;

x_array = [6.,2.,1.,4.]
y_array = [2.,5.,3.,1.]

p = Polygon(x_array, y_array)
        
m = ExteriorMap(p)

m⁻¹ = InverseMap(m)

z1 = 6. + 2im
z2 = 2. + 5im
z3 = 1. + 3im
z4 = 4. + 1im

w1 = m⁻¹(z1)
w2 = m⁻¹(z2)
w3 = m⁻¹(z3)
w4 = m⁻¹(z4)

w5 = m⁻¹(2.5 + 2im)
w6 = m⁻¹(5 + 1.5im)

println(w1)
println(w2)
println(w3)
println(w4)
println(w5)
println(w6)
