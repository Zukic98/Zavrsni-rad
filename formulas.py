import math
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

def AngleBetweenTwoLines(l1, l2):
    return l1.angle_between(l2)

#def real_part_Joukowsky(z):
#    X, Y = z
#    return 1 + (Y * Y - X * X) / ((X * X + Y * Y) * (X * X + Y * Y)), (-2 * X * Y) / ((X * X + Y * Y) * (X * X + Y * Y))

def argument_of_complex_number(complex_number):
    return math.atan(complex_number.imag / complex_number.real)

def distance_between_two_points(complex1, complex2):
    return math.sqrt(
        (complex1.real - complex2.real) * (complex1.real - complex2.real) + (complex1.imag - complex2.imag) * (
                    complex1.imag - complex2.imag))



points_and_angles = [ ( 1+1j,math.pi/3), ( 1+1j,math.pi/3),( 1+1j,math.pi/3),( 1+1j,math.pi/3),( 1+1j,math.pi/3)]
f = InverseSchwarzCristoffelMapping(points_and_angles,4)
print(JoukowskyRealPartGradient(f(2+3j)))