import math
import geopandas as gpd
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

def areaOfPolygon(arrayOfPoints):
    area = 0
    for i in range(len(arrayOfPoints) - 1):
        area += arrayOfPoints[i][0] * arrayOfPoints[i + 1][1] - arrayOfPoints[i + 1][0] * arrayOfPoints[i][1]
    area += arrayOfPoints[len(arrayOfPoints) - 1][0] * arrayOfPoints[0][1] - arrayOfPoints[len(arrayOfPoints) - 1][1] * arrayOfPoints[0][0]
    return math.fabs(area/2)

def getRadiusForCircles(polygonsArea,n):
    return math.sqrt(polygonsArea/(n*math.pi))

def findCenterOfPolygon(polygon):
    center = gpd.GeoSeries([polygon])
    return (center.representative_point().x, center.representative_point().y)


#points_and_angles = [ ( 1+1j,math.pi/3), ( 1+1j,math.pi/3),( 1+1j,math.pi/3),( 1+1j,math.pi/3),( 1+1j,math.pi/3)]
#f = InverseSchwarzCristoffelMapping(points_and_angles,4)
#print(JoukowskyRealPartGradient(f(2+3j)))
