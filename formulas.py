import math
import geopandas as gpd

import matplotlib
matplotlib.use('TKAgg')

##############################################################
# Function provide first making skeleton for transformation  #
# then return function for compute inverse SC in some point  #
##############################################################

def InverseSchwarzCristoffelMapping(points):
    file = open("dataTransfer.txt", "w")

    file.write("start\n")

    string_x_array = ""
    string_y_array = ""

    for x,y in points:
        string_x_array = string_x_array + str(x) + ","
        string_y_array = string_y_array + str(y) + ","

    #write in file in format x,y,z\nk,p,r
    file.write(string_x_array[:-1] + "\n" + string_y_array[:-1])

    file.close()

    def product(point_z):
        file = open("dataTransfer.txt", "w")

        string_of_complex = "load\n" + point_z.real + "+" + point_z.imag + "im"

        file.write(string_of_complex)

        file.close()

        returnValue = 0.

        while True:
            file = open("dataTransfer.txt", "r")

            firstLine = file.readline()

            if firstLine == "result":

                real, imag =  file.readline().replace("im","").split("+")

                returnValue = complex(float(real), float(imag))

                break

            file.close()


        return returnValue

    return product

def realPartofJoukowskyTransform(complex_number : complex):
    return complex_number.real*(1+(1/(complex_number.real**2 + complex_number.imag**2)))

#Function provide solve of three-diagonal systems
def solveSystemOfLinearEquation(p, q, r, b):

    n = len(b)
    x = [None] * n

    for i in range(0,n-1):
        mi = r[i]/p[i]
        p[i+1] = p[i+1] - mi*q[i]
        b[i+1] = b[i+1] - mi*b[i]

    x[n-1] = b[n-1]/p[n-1]
    for i in reversed(range(n-1)) :
        x[i] = (b[i] - q[i]*x[i+1])/p[i]

    return x

def argument_of_complex_number(complex_number):
    return math.atan(complex_number.imag / complex_number.real)

def distance_between_two_points(complex1, complex2):
    return math.sqrt(
        (complex1.real - complex2.real) * (complex1.real - complex2.real) + (complex1.imag - complex2.imag) * (
                complex1.imag - complex2.imag))

def areaOfPolygon(arrayOfPoints):
    area = 0.

    arrayOfPoints = tuple(arrayOfPoints.exterior.coords)

    for i in range(len(arrayOfPoints) - 1):
        area += arrayOfPoints[i][0] * arrayOfPoints[i + 1][1] - arrayOfPoints[i + 1][0] * arrayOfPoints[i][1]

    area += arrayOfPoints[len(arrayOfPoints) - 1][0] * arrayOfPoints[0][1] - arrayOfPoints[len(arrayOfPoints) - 1][1] * arrayOfPoints[0][0]

    return math.fabs(area / 2)

def getRadiusForCircles(polygonsArea, n):
    return math.sqrt(polygonsArea / (n * math.pi))

def findCenterOfPolygon(polygon):
    center = gpd.GeoSeries([polygon])
    return center.representative_point()[0].x, center.representative_point()[0].y

def getTwoPossibleCircles(x1_center, y1_center, x2_center, y2_center, r1, r2, r3):

    R1 = (r1 + r3) ** 2
    R2 = (r2 + r3) ** 2

    p = R1 - R2 + x1_center ** 2 - x2_center ** 2 + y1_center ** 2 - y2_center ** 2
    q = 2 * (y2_center - y1_center)
    t = 2 * (x2_center - x1_center)

    if abs(t) < 10e-3:

        y = -p / q

        return x1_center + math.sqrt(R1 - (y1_center-y)**2), y, x1_center - math.sqrt(R1 - (y1_center-y)**2), y

    if abs(q) < 10e-3:

        x = -p / t

        return x, y1_center + math.sqrt(R1-(x1_center-x)**2), x, y1_center - math.sqrt(R1-(x1_center-x)**2)

    a = t ** 2 + q ** 2
    b = 2 * x1_center * t * q + 2 * p * q - 2 * y1_center * t ** 2
    c = x1_center ** 2 * t ** 2 + 2 * x1_center * t * p + p * p + y1_center ** 2 * t ** 2 - R1 * t ** 2

    y1 = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
    y2 = (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)

    x1 = (-p - q * y1) / t
    x2 = (-p - q * y2) / t

    return x1, y1, x2, y2

def getCenterOfLine(z, zCenter):
    return complex((z.real + zCenter.real)/2,(z.imag + zCenter.imag)/2)
