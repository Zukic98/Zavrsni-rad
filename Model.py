import math

import matplotlib
import shapely

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
    peripheral_penguins = {}
    central_penguins = {}
    circles = {}
    text = {}

    def __init__(self):
        pass

    def isPointOutsideOfPolygon(self, x, y):
        return Point(x, y).within(self.polygon)

    def generatePenguin(self, ID, edge, heat_loss, position, radius, neighbours):
        self.peripheral_penguins[ID] = Penguin.Penguin(ID, edge, heat_loss, position,
                                                       radius, neighbours)
        self.circles[ID] = plt.Circle(position, radius, fc="cyan", edgecolor="black")
        self.text[ID] = plt.text(position[0], position[1], str(ID))

    def generatePenguins(self):
        # define polygon boundaries of huddle
        x, y = self.polygon.exterior.xy

        fig = plt.figure()
        board = plt.axes()
        # plt.autoscale
        plt.plot(x, y, c="blue")
        # find center of polygon
        x, y = formulas.findCenterOfPolygon(self.polygon)

        radius_of_penguin = formulas.getRadiusForCircles(formulas.areaOfPolygon(self.polygon), self.number)

        self.generatePenguin(0, True, 0, (x, y), radius_of_penguin, [1])
        board.add_patch(self.circles[0])

        plt.draw()

        # if second circle 
        if shapely.geometry.Point(x, y + 2 * radius_of_penguin).within(self.polygon):
            y = y + 2 * radius_of_penguin
        else:
            y = y - 2 * radius_of_penguin

        self.generatePenguin(1, True, 0, (x, y), radius_of_penguin, [0])
        board.add_patch(self.circles[1])
        plt.draw()

        q = 2  # variable for counting number of created penguins

        for i in range(0, self.number):

            if i >= q or q >= self.number:
                break

            list_of_neighbours = self.peripheral_penguins[i].neighbours

            x1 = self.peripheral_penguins[i].position[0]
            y1 = self.peripheral_penguins[i].position[1]

            for j in list_of_neighbours:

                x2 = self.peripheral_penguins[j].position[0]
                y2 = self.peripheral_penguins[j].position[1]

                try:
                    x3, y3, x4, y4 = formulas.getTwoPossibleCircles(x1, y1, x2, y2, radius_of_penguin,
                                                                    radius_of_penguin, radius_of_penguin)
                except:
                    print("Izuzetak")
                    break

                existFirst = False
                existSecond = False

                for k in list_of_neighbours:
                    if abs(x3 - self.peripheral_penguins[k].position[0]) < 1 and abs(
                            y3 - self.peripheral_penguins[k].position[1]) < 1:
                        existFirst = True
                    if abs(x4 - self.peripheral_penguins[k].position[0]) < 1 and abs(
                            y4 - self.peripheral_penguins[k].position[1]) < 1:
                        existSecond = True

                if not existFirst and shapely.geometry.Point(x3, y3).within(self.polygon):
                    self.generatePenguin(q, True, 0, (x3, y3), radius_of_penguin, [i, j])
                    board.add_patch(self.circles[q])
                    plt.draw()

                    self.peripheral_penguins[i].addNeighbour(q)
                    self.peripheral_penguins[j].addNeighbour(q)

                    q += 1
                    if q == self.number:
                        break

                if not existSecond and shapely.geometry.Point(x4, y4).within(self.polygon):
                    self.generatePenguin(q, True, 0, (x4, y4), radius_of_penguin, [i, j])
                    board.add_patch(self.circles[q])
                    board.add_patch(self.circles[q])
                    plt.draw()

                    self.peripheral_penguins[i].addNeighbour(q)
                    self.peripheral_penguins[j].addNeighbour(q)

                    q += 1
                    if q == self.number:
                        break

                if len(list_of_neighbours) == 6:

                    x3, y3, x4, y4 = formulas.getTwoPossibleCircles(self.peripheral_penguins[i].position[0],
                                                                    self.peripheral_penguins[i].position[1],
                                                                    self.peripheral_penguins[q - 1].position[0],
                                                                    self.peripheral_penguins[q - 1].position[1],
                                                                    radius_of_penguin, radius_of_penguin,
                                                                    radius_of_penguin)
                    for k in list_of_neighbours:

                        if abs(x3 - self.peripheral_penguins[k].position[0]) < 1 and abs(
                                y3 - self.peripheral_penguins[k].position[1]) < 1 and not (
                                k in self.peripheral_penguins[q - 1].neighbours):
                            self.peripheral_penguins[k].neighbours.append(q - 1)
                            self.peripheral_penguins[q - 1].neighbours.append(k)
                            break

                        if abs(x4 - self.peripheral_penguins[k].position[0]) < 1 and abs(
                                y4 - self.peripheral_penguins[k].position[1]) < 1 and not (
                                k in self.peripheral_penguins[q - 1].neighbours):
                            self.peripheral_penguins[k].neighbours.append(q - 1)
                            self.peripheral_penguins[q - 1].neighbours.append(k)
                            break

                    self.peripheral_penguins[i].edge = False

                    #self.central_penguins[i] = self.peripheral_penguins[i]

                    #del self.peripheral_penguins[i]

                print(list_of_neighbours)
        plt.show()

    def updateHeatLosses(self):


        invers_SchwarzCristoffel_function = formulas.InverseSchwarzCristoffelMapping()

        for i in range(0, self.numbers):
            if self.peripheral_penguins[i].edge:

                x, y = self.peripheral_penguins[i].position
                x_p1 = 0.0
                y_p1 = 0.0
                counter = 0

                for peng in self.peripheral_penguins[i].neighbours:
                    if peng.edge and counter == 0:
                        x_p1, y_p1 = peng.position
                        counter += 1
                    elif peng.edge:
                        x_p2, y_p2 = peng.position

                x_half1 = (x + x_p1) / 2
                y_half1 = (y + y_p1) / 2
                x_half2 = (x + x_p2) / 2
                y_half2 = (y + y_p2) / 2




    def run(self):
        if self.name == "" or self.number == "" or self.Peclet == "" or self.R == "" or self.polygon == None:
            raise ValueError("You need to fill all the fields and set the polygon to start the simulation")
        if not self.number.isnumeric():
            raise ValueError("Error: Number of penguins must be natural number!")
        if not self.Peclet.isnumeric():
            raise ValueError("Error: Peclet's number must be natural number!")
        if not self.R.isnumeric():
            raise ValueError("Error: R must be natural number!")
        self.number = int(self.number)
        self.generatePenguins()
        self.updateHeatLosses()
