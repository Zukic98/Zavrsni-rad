import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt

from shapely.geometry import Point

import formulas

import Penguin
class ModelSample:
    name = None
    number = None
    Peclet = None
    R = None
    polygon = None

    def __init__(self):
        pass

    def isPointOutsideOfPolygon(self,x,y):
        return Point(x,y).within(self.polygon)
    def generateSeed(self):
        2+2
    def generatePenguins(self):
        #define polygon boundaries of huddle
        x, y = self.polygon.exterior.xy

        fig = plt.figure()
        board = plt.axes()

        plt.plot(x, y, c="blue")
        #find center of polygon
        x,y = formulas.findCenterOfPolygon(self.polygon)

        radius_of_penguin = formulas.getRadiusForCircles(formulas.areaOfPolygon(self.polygon), self.number)
        radius_of_penguin = int(radius_of_penguin)
        board.add_patch(plt.Circle((x,y), radius_of_penguin, fc = "cyan"))

        peripheral_penguins = {}
        central_penguins = {}
        circles = {}

        peripheral_penguins[1] = Penguin.Penguin(ID=1, edge=True, heat_loss=0, position=(x, y), radius = radius_of_penguin, neighbours=[])
        circles[1] = plt.Circle((x, y), radius_of_penguin, fc="cyan")
        board.add_patch(circles[1])

        y = y - 2 * radius_of_penguin

        peripheral_penguins[2] = Penguin.Penguin(ID=2, edge=True, heat_loss=0, position=(x, y), radius=radius_of_penguin, neighbours=[])

        circles[2] = plt.Circle((x, y), radius_of_penguin, fc="cyan")
        board.add_patch(circles[2])

        

        plt.autoscale()
        plt.draw()

        #for i in range(3,self.number):

        #    for j in range(6):

        plt.show()

    def run(self):
        if self.name == "" or self.number == "" or self.Peclet == "" or self.R == "" or self.polygon == None:
            raise ValueError("You need to fill all the fields and set the polygon to start the simulation")
        if not self.number.isnumeric():
            raise ValueError("Error: Number of penguins must be natural number!")
        if not self.Peclet.isnumeric():
            raise ValueError("Error: Peclet's number must be natural number!")
        if not self.R.isnumeric():
            raise ValueError("Error: R must be natural number!")
        self.generatePenguins()