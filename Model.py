import cmath
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
    delta_r = None
    polygon = None
    numberOfIteration = 10
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
        self.peripheral_penguins[startIndexOfPeripheralPenguin] = self.central_penguins[startIndexOfPeripheralPenguin]

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

            self.peripheral_penguins[indexOfPeripheralPenguin] = self.central_penguins[indexOfPeripheralPenguin]

            previous_index = indexOfPeripheralPenguin
            indexOfPeripheralPenguin = indexTarget

        for edgeIndex in self.peripheral_penguins:
            del self.central_penguins[edgeIndex]


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
        self.extractPeripheralPenguins(q)

        for i in range(0, q):
            print(self.central_penguins[i].ID, ":", "Position", self.central_penguins[i].position[0], ",",
                  self.central_penguins[i].position[1], "Susjedi:",
                  self.central_penguins[i].neighbours,self.central_penguins[i].edge)
        plt.show()

        return self.peripheral_penguins

    def computeBoundaries(self, penguinID, inverse_SchwarzCristoffel_function):

        z1 = 0+0j
        z2 = 0+0j
        firstFound = True

        for neighbour_id in self.peripheral_penguins[penguinID].neighbours:
            if self.peripheral_penguins[neighbour_id].edge:
                if firstFound:
                    z1 = complex(self.peripheral_penguins[neighbour_id].position[0],
                                 self.peripheral_penguins[neighbour_id].position[1])
                    firstFound = False
                else:
                    z2 = complex(self.peripheral_penguins[neighbour_id].position[0],
                                 self.peripheral_penguins[neighbour_id].position[1])

        point = self.peripheral_penguins[penguinID].position

        zCenter = complex(point[0],point[1])

        z1 = formulas.getCenterOfLine(z1, zCenter)
        z2 = formulas.getCenterOfLine(z2, zCenter)

        above_boundary = cmath.phase(inverse_SchwarzCristoffel_function(z1))

        belove_boundary = cmath.phase(inverse_SchwarzCristoffel_function(z2))

        return above_boundary, belove_boundary

    def computeHeatLossForPeripheralPenguins(self, inverse_SchwarzCristoffel_function):

        max_heat_loss = float('-inf')
        min_heat_loss = float('inf')

        id_of_max_heat_loss = 0
        id_of_min_heat_loss = 0
        id_of_second_min_heat_loss_neighbour = 0

        for penguinID, penguin in self.peripheral_penguins.items():

            above_boundary, belove_boundary = self.computeBoundaries(penguinID)

            penguin.updateHeatLoss(above_boundary, belove_boundary, self.delta_r, self.R, self.Peclet)

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

    def getPoints(self):
        list_of_points = []
        for x in self.peripheral_penguins.values():
            list_of_points.append(x.position)
        return list_of_points


    def changePositions(self, max_heat_id, min_heat_id, min_heat_id_neighbour):

        #eliminate max_heat_id from his neighbours
        for neighbour_id in self.peripheral_penguins[max_heat_id].neighbours:
            if neighbour_id in self.peripheral_penguins:
                self.peripheral_penguins[neighbour_id].neighbours.remove(max_heat_id)
            else:
                self.central_penguins[neighbour_id].neighbours.remove(max_heat_id)
                if len(self.central_penguins[neighbour_id].neighbours) == 5:
                    self.peripheral_penguins[neighbour_id] = self.central_penguins[neighbour_id]
                    self.peripheral_penguins[neighbour_id].edge = True
                    del self.central_penguins[neighbour_id]

        self.peripheral_penguins[max_heat_id].neighbours = []

        #add penguin next to new neighbours
        firstPoint = self.peripheral_penguins[min_heat_id].position
        secondPoint = self.peripheral_penguins[min_heat_id_neighbour].position

        x1, y1, x2, y2 = formulas.getTwoPossibleCircles(firstPoint[0], firstPoint[1], secondPoint[0], secondPoint[1])

        for neighbour_id in self.peripheral_penguins[min_heat_id].neighbours:
            if neighbour_id in self.central_penguins and "JEDNAKI1":
                self.peripheral_penguins[max_heat_id].position = (x1, y1)
            if neighbour_id in self.central_penguins and "JEDNAKI2":
                self.peripheral_penguins[max_heat_id].position = (x2, y2)

        self.changePositionOnGUI(max_heat_id)

        self.peripheral_penguins[min_heat_id].neighbours.append(max_heat_id)
        self.peripheral_penguins[min_heat_id_neighbour].neighbours.append(max_heat_id)

        if len(self.peripheral_penguins[min_heat_id].neighbours) == 6:
            self.central_penguins[min_heat_id] = self.peripheral_penguins[min_heat_id]
            del self.peripheral_penguins[min_heat_id]

        if len(self.peripheral_penguins[min_heat_id_neighbour].neighbours) == 6:
            self.central_penguins[min_heat_id_neighbour] = self.peripheral_penguins[min_heat_id_neighbour]
            del self.peripheral_penguins[min_heat_id_neighbour]

        self.peripheral_penguins[max_heat_id].neighbours.extend([min_heat_id, min_heat_id_neighbour])

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

        for i in range(0, self.numberOfIteration):

            complexPoints = self.getComplexPoints()
            inverse_SchwarzCristoffel_function = formulas.InverseSchwarzCristoffelMapping(complexPoints)
            max_heat_id, min_heat_id, min_heat_id_neighbour = self.computeHeatLossForPeripheralPenguins(inverse_SchwarzCristoffel_function)
            self.changePositions(max_heat_id, min_heat_id, min_heat_id_neighbour)
