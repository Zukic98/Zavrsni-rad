import math
import geopandas as gpd
from scipy.optimize import fsolve
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt

#points and angles must be dictionary where key is complex number and angle is float type
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
"""
def JoukowskyRealPartGradient(z):
    return 1 + (-z.real * z.real + z.imag * z.imag) / pow((z.real * z.real + z.imag * z.imag), 2), (-2 * z.real * z.imag) / pow((z.real * z.real + z.imag * z.imag), 2)

def real_part_Joukowsky(z):
    X, Y = z
    return 1 + (Y * Y - X * X) / ((X * X + Y * Y) * (X * X + Y * Y)), (-2 * X * Y) / ((X * X + Y * Y) * (X * X + Y * Y))
"""

def argument_of_complex_number(complex_number):
    return math.atan(complex_number.imag / complex_number.real)

def distance_between_two_points(complex1, complex2):
    return math.sqrt(
        (complex1.real - complex2.real) * (complex1.real - complex2.real) + (complex1.imag - complex2.imag) * (
                complex1.imag - complex2.imag))

def angleBetweenPoints(point1 , centralPoint, point2):
    vector1 = [0, 0]
    vector1[0] = point1[0] - centralPoint[0]
    vector1[1] = point1[1] - centralPoint[1]

    vector2 = [0, 0]
    vector2[0] = point2[0] - centralPoint[0]
    vector2[1] = point2[1] - centralPoint[1]

    angle = math.acos((vector1[0]*vector2[0]+vector1[1]*vector2[1]) / (math.sqrt( vector1[0]**2 + vector1[1]**2) * math.sqrt( vector2[0]**2 + vector2[1]**2 )))
    #if angle < 0:
    #    angle = 180 - angle
    return angle
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
    return center.representative_point()[0].x.item(), center.representative_point()[0].y.item()

def getTwoPossibleCircles(x1_center, y1_center, x2_center, y2_center, r1, r2, r3):
    R1 = (r1 + r3)**2
    R2 = (r2 + r3)**2

    q = 2 * (y2_center-y1_center)
    p = R1 - R2 -x1_center**2 + x2_center**2 - y1_center**2 + y2_center**2
    t = 2 * (x2_center - x1_center)

    if abs(t) < 1:

        y = p / q
        b = -2 * x1_center
        c = x1_center ** 2 + y1_center ** 2 - 2 * y1_center * y + y ** 2 - R1
        if b * b - 4 * c < 0:
            print("This")
        return round((-b + math.sqrt(b * b - 4 * c)) / 2,2), round(y,2), round((-b - math.sqrt(b * b - 4 * c)) / 2,2), round(y,2)

    if abs(q) < 1:

        x = p / t
        b = -2 * y1_center
        c = x1_center ** 2 - 2 * x1_center * x + x ** 2 + y1_center ** 2 - R1
        if b ** 2 - 4 * c < 0:
            print("Ovaj")
        return round(x,2), round((-b + math.sqrt(b ** 2 - 4 * c)) / 2,2), round(x,2), round((-b - math.sqrt(b ** 2 - 4 * c)) / 2,2)

    a = t**2 + q**2
    b = 2 * x1_center * t * q - 2*p*q - 2*y1_center*t**2
    c = x1_center**2 * t**2 - 2 * x1_center * t * p + p * p + y1_center**2 * t**2 - R1 * t**2

    if b * b - 4 * a * c < 0:
        print("To je taj")
        exit()

    y1 = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
    y2 = (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)

    x1 = (p - q * y1) / t
    x2 = (p - q * y2) / t

    return round(x1,2), round(y1,2), round(x2,2), round(y2,2)

