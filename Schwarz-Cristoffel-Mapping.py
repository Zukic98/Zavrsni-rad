from math import pi
def InverseSchwarzCristoffelMapping(points_and_angles, C):
    def product(point_z):
        accumulator = 1
        for x in points_and_angles:
            point, angle = x
            accumulator *= pow( (1-point_z/point), -angle)
        return C*accumulator
    return product
def JoukowskyRealPartGradient(z):
    return 1 + (-z.real * z.real + z.imag * z.imag)/pow((z.real * z.real + z.imag * z.imag),2), (-2*z.real*z.imag)/pow((z.real * z.real + z.imag * z.imag),2)



points_and_angles = [ ( 1+1j,pi/3), ( 1+1j,pi/3),( 1+1j,pi/3),( 1+1j,pi/3),( 1+1j,pi/3)]
f = InverseSchwarzCristoffelMapping(points_and_angles,4)
print(JoukowskyRealPartGradient(f(2+3j)))