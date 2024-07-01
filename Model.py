import math

import matplotlib
import shapely
import time

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
    central_penguins = {}
    peripheral_penguins = {}
    circles = {}
    text = {}

    def __init__(self):
        pass

    def isPointOutsideOfPolygon(self, x, y):
        return Point(x, y).within(self.polygon)

    def generatePenguin(self, ID, edge, heat_loss, position, radius, neighbours):
        self.central_penguins[ID] = Penguin.Penguin(ID, edge, heat_loss, position,
                                                       radius, neighbours)
        self.circles[ID] = plt.Circle(position, radius, fc="cyan", edgecolor="black")
        self.text[ID] = plt.text(position[0], position[1], str(ID), fontsize = "xx-small")

    def extractPeripheralPenguins(self, q):
        startIndexOfPeripheralPenguin = q - 1
        self.peripheral_penguins.append(self.central_penguins[startIndexOfPeripheralPenguin])

        for index in self.central_penguins[q - 1].neighbours:
            if self.central_penguins[index].edge:
                break

        indexOfPeripheralPenguin = index
        previous_index = startIndexOfPeripheralPenguin

        while startIndexOfPeripheralPenguin != indexOfPeripheralPenguin:
            # find peripheral neighbour

            list_of_neighbours = self.central_penguins[indexOfPeripheralPenguin].neighbours
            minNeighbours = 7
            indexTarget = 0
            for index in list_of_neighbours:
                if self.central_penguins[index].edge and index != previous_index and minNeighbours > len(
                        self.central_penguins[index].neighbours):
                    minNeighbours = len(self.central_penguins[index].neighbours)
                    indexTarget = index

            self.peripheral_penguins.append(self.central_penguins[indexOfPeripheralPenguin])
            # del self.central_penguins[indexOfPeripheralPenguin]

            previous_index = indexOfPeripheralPenguin
            indexOfPeripheralPenguin = indexTarget

    def generatePenguins(self):
        # define polygon boundaries of huddle

        x, y = self.polygon.exterior.xy

        fig = plt.figure()
        board = plt.axes()
        # plt.autoscale
        plt.plot(x, y, c="blue")
        # find center of polygon
        x, y = formulas.findCenterOfPolygon(self.polygon)

        #make corelation with formulas
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

            if i >= q or q == self.number:
                break

            try :
                list_of_neighbours = self.central_penguins[i].neighbours
            except :
                print("Fula")
                break
                plt.show()
                exit()
            x1 = self.central_penguins[i].position[0]
            y1 = self.central_penguins[i].position[1]

            for j in list_of_neighbours:

                if q == self.number:
                    break

                x2 = self.central_penguins[j].position[0]
                y2 = self.central_penguins[j].position[1]

                print("i:",i,"j:",j)
                x3, y3, x4, y4 = formulas.getTwoPossibleCircles(x1, y1, x2, y2, radius_of_penguin, radius_of_penguin, radius_of_penguin)

                existFirst = False
                existSecond = False

                for k in list_of_neighbours:
                    if abs(x3 - self.central_penguins[k].position[0]) < 10e-1 and abs(
                            y3 - self.central_penguins[k].position[1]) < 10e-1 :
                        existFirst = True
                    if abs(x4 - self.central_penguins[k].position[0]) < 10e-1 and abs(
                            y4 - self.central_penguins[k].position[1]) < 10e-1 :
                        existSecond = True

                if  i != 0 and not existFirst and not existSecond:
                    print("Problem",i,j,"(x3,y3): ")
                    print(self.central_penguins[j].neighbours)
                    plt.show()
                    for i in range(0, q):
                        print(self.central_penguins[i].ID, ":", "Position", self.central_penguins[i].position[0], ",",
                              self.central_penguins[i].position[1], "Susjedi:",
                              self.central_penguins[i].neighbours)
                    exit()

                if not existFirst and shapely.geometry.Point(x3, y3).within(self.polygon):
                    self.generatePenguin(q, True, 0, (x3, y3), radius_of_penguin, [i, j])
                    board.add_patch(self.circles[q])
                    plt.draw()

                    self.central_penguins[i].addNeighbour(q)
                    self.central_penguins[j].addNeighbour(q)

                    q += 1

                if not existSecond and shapely.geometry.Point(x4, y4).within(self.polygon):
                    self.generatePenguin(q, True, 0, (x4, y4), radius_of_penguin, [i, j])
                    board.add_patch(self.circles[q])
                    plt.draw()

                    self.central_penguins[i].addNeighbour(q)
                    self.central_penguins[j].addNeighbour(q)

                    q += 1


                if len(list_of_neighbours) == 6:

                    c = q-1
                    c2 = complex(self.central_penguins[c].position[0], self.central_penguins[c].position[1])

                    for k in list_of_neighbours:

                        c1 = complex(self.central_penguins[k].position[0], self.central_penguins[k].position[1])

                        if (abs(formulas.distance_between_two_points(c1, c2) - (2*radius_of_penguin)) < 10e-1 and
                                c not in self.central_penguins[k].neighbours):

                            self.central_penguins[k].neighbours.append(c)
                            self.central_penguins[c].neighbours.append(k)

                            break

                    self.central_penguins[i].edge = False
                    break


        #make two heaps for peripheral and central penguins
        print("Q iznosi",q)
        #self.extractPeripheralPenguins(q)



        #find angles and delete central_penguins on edge whose are now on peripheral penguins
        complexPoints_and_angles = {}

        """boundary = len(self.peripheral_penguins)

        for i in range(0, boundary):

            x_center, y_center = self.peripheral_penguins[i].position

            if i == 0:
                x_left, y_left = self.peripheral_penguins[boundary-1]
                x_right, y_right = self.peripheral_penguins[1]
                complexPoints_and_angles[complex(x, y)] = formulas.angleBetweenPoints(complex(x_left, y_left),
                                                                                      complex(x_center, y_center),
                                                                                      complex(x_right, y_right))
            elif i == boundary - 1:
                x_left, y_left = self.peripheral_penguins[i - 1]
                x_right, y_right = self.peripheral_penguins[0]
                complexPoints_and_angles[complex(x, y)] = formulas.angleBetweenPoints(complex(x_left, y_left),
                                                                                      complex(x_center, y_center),
                                                                                      complex(x_right, y_right))
            else :
                x_left, y_left = self.peripheral_penguins[i - 1]
                x_right, y_right = self.peripheral_penguins[i + 1]
                complexPoints_and_angles[complex(x, y)] = formulas.angleBetweenPoints(complex(x_left, y_left), complex(x_center, y_center), complex(x_right, y_right))

            del self.central_penguins[i]"""
        for i in range(0, q):
            print(self.central_penguins[i].ID, ":", "Position", self.central_penguins[i].position[0], ",",
                  self.central_penguins[i].position[1], "Susjedi:",
                  self.central_penguins[i].neighbours,self.central_penguins[i].edge)
        plt.show()

        return {}

    def computeBoundaries(self, penguinID):

        above_boundary = 0
        belove_boundary = 0
        delta_r = 0
        f = 0
        return above_boundary, belove_boundary, delta_r, f
    def updateHeatLosses(self):

        max_heat_loss = float('-inf')
        min_heat_loss = float('inf')

        id_of_max_heat_loss = 0
        id_of_min_heat_loss = 0
        id_of_second_min_heat_loss_neighbour = 0

        for penguinID, penguin in self.peripheral_penguins.items():

            penguin.updateHeatLoss(self.computeBoundaries(penguinID))

            if penguin.heat_loss >= max_heat_loss:
                max_heat_loss = penguin.heat_loss
                id_of_max_heat_loss = penguinID

            if penguin.heat_loss <= min_heat_loss:
                min_heat_loss = penguin.heat_loss
                id_of_min_heat_loss = penguinID

        min_heat_loss = float('inf')

        for neighbourID in self.peripheral_penguins[id_of_min_heat_loss].neighbours:

            if self.peripheral_penguins[neighbourID].heat_loss <= min_heat_loss and not self.peripheral_penguins[neighbourID].edge:
                min_heat_loss = self.peripheral_penguins[neighbourID].heat_loss
                id_of_second_min_heat_loss_neighbour = neighbourID

        return id_of_max_heat_loss, id_of_min_heat_loss, id_of_second_min_heat_loss_neighbour

    def updateHeatLosses(self):

        for i in range(0, self.numbers):
            if self.central_penguins[i].edge:

                x, y = self.central_penguins[i].position
                x_p1 = 0.0
                y_p1 = 0.0
                counter = 0

                for peng in self.central_penguins[i].neighbours:
                    if peng.edge and counter == 0:
                        x_p1, y_p1 = peng.position
                        counter += 1
                    elif peng.edge:
                        x_p2, y_p2 = peng.position

                x_half1 = (x + x_p1) / 2
                y_half1 = (y + y_p1) / 2
                x_half2 = (x + x_p2) / 2
                y_half2 = (y + y_p2) / 2

    """def computeHeatLossForPeripheralPenguins(self, inverse_SchwarzCristoffel_function):
        boundary = len(self.peripheral_penguins)

        for i in range(0, boundary):

            x_center, y_center = self.peripheral_penguins[i].position

            if i == 0:
                x_left_half = formulas.distance_between_two_points()
            elif i == boundary - 1:
                x_left, y_left = self.peripheral_penguins[i - 1]
                x_right, y_right = self.peripheral_penguins[0]
                complexPoints_and_angles[complex(x, y)] = formulas.angleBetweenPoints(complex(x_left, y_left),
                                                                                      complex(x_center, y_center),
                                                                                      complex(x_right, y_right))
            else:
                x_left, y_left = self.peripheral_penguins[i - 1]
                x_right, y_right = self.peripheral_penguins[i + 1]
                complexPoints_and_angles[complex(x, y)] = formulas.angleBetweenPoints(complex(x_left, y_left),
                                                                                      complex(x_center, y_center),
                                                                                      complex(x_right, y_right))
    """

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

        complexPoints_and_angles = self.generatePenguins()
        print(complexPoints_and_angles)
        """while True:
            inverse_SchwarzCristoffel_function = formulas.InverseSchwarzCristoffelMapping(complexPoints_and_angles, 1)
            max_heat_id, min_heat_id = self.computeHeatLossForPeripheralPenguins(inverse_SchwarzCristoffel_function)
            #changePositions(max_heat_id, min_heat_id)
        self.updateHeatLosses()"""