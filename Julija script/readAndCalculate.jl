using Pkg;
Pkg.add("SchwarzChristoffel");
Pkg.add("Plots")

using SchwarzChristoffel;
using Plots;

function parse_complex(str::String)
    
    #first strip "im" then split string in two string variables and then parse to float64
    real_part, imaginary_part= parse.(Float64, split( replace(str, r"im"=>""), "+"))
    
    return Complex(real_part, imaginary_part)
end  

while true 
    f = open("dataTransfer.txt", "r")

    firstLine = readline(f)
    
    if cmp(firstLine,"start") == 0
        
        sleep(0.2)

        x_array = parse.(Float64, split(readline(f), ","))
        y_array = parse.(Float64, split(readline(f), ","))
        
        p = Polygon(x_array, y_array)
        
        m = ExteriorMap(p)
        
        global m⁻¹ = InverseMap(m)
        
        close(f)

        f = open("dataTransfer.txt", "w")
        
        write(f,"in_process")
    end
    
    if cmp(firstLine,"load") == 0
        
        sleep(0.2)

        complexValue = parse_complex( readline(f) )

        close(f)

        f = open("dataTransfer.txt", "w")
        
        write(f,"result\n")

        write(f,string(m⁻¹(complexValue)))

    end
       
    close(f)

end 