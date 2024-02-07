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

    def __init__(self):
        pass

    def isPointOutsideOfPolygon(self, x, y):
        return Point(x, y).within(self.polygon)

    def generatePenguins(self):
        # define polygon boundaries of huddle
        x, y = self.polygon.exterior.xy

        fig = plt.figure()
        board = plt.axes()
        #plt.autoscale
        plt.plot(x, y, c="blue")
        # find center of polygon
        x, y = formulas.findCenterOfPolygon(self.polygon)

        radius_of_penguin = formulas.getRadiusForCircles(formulas.areaOfPolygon(self.polygon), self.number)

        peripheral_penguins = {}
        central_penguins = {}
        circles = {}
        text = {}

        peripheral_penguins[0] = Penguin.Penguin(ID=1, edge=True, heat_loss=0, position=(x, y),
                                                 radius=radius_of_penguin, neighbours=[1])
        circles[0] = plt.Circle((x, y), radius_of_penguin, fc="cyan", edgecolor = "black")
        text[0] = plt.text(x, y, "ID: 0")
        board.add_patch(circles[0])
        plt.draw()

        if shapely.geometry.Point(x,y+2*radius_of_penguin).within(self.polygon):
            y = y + 2 * radius_of_penguin
        else:
            y = y - 2 * radius_of_penguin
        peripheral_penguins[1] = Penguin.Penguin(ID=2, edge=True, heat_loss=0, position=(x, y),
                                                 radius=radius_of_penguin, neighbours=[0])
        circles[1] = plt.Circle((x, y), radius_of_penguin, fc="cyan", edgecolor = "black")
        text[1] = plt.text(x, y, "ID: 1")
        board.add_patch(circles[1])
        plt.draw()

        x3, y3, x4, y4 = formulas.getTwoPossibleCircles(peripheral_penguins[0].position[0], peripheral_penguins[0].position[1],
                                                        peripheral_penguins[1].position[0], peripheral_penguins[1].position[1], radius_of_penguin)

        peripheral_penguins[2] = Penguin.Penguin(ID=2, edge=True, heat_loss=0, position=(x3, y3),
                                                 radius=radius_of_penguin, neighbours=[0,1])
        circles[2] = plt.Circle((x3, y3), radius_of_penguin, fc="cyan", edgecolor="black")
        text[2] = plt.text(x3, y3, "ID: 2")
        board.add_patch(circles[2])
        plt.draw()

        q = 2 #variable for counting number of created penguins
        for i in range(0, self.number):
            if i == 2:
                break
            list_of_neighbours = peripheral_penguins[i].neighbours
            x1 = peripheral_penguins[i].position[0]
            y1 = peripheral_penguins[i].position[1]

            clock = len(list_of_neighbours)

            if q == self.number:
                break
            for j in list_of_neighbours:
                if clock == 6:
                    break
                x2 = peripheral_penguins[j].position[0]
                y2 = peripheral_penguins[j].position[1]

                x3, y3, x4, y4 = formulas.getTwoPossibleCircles(x1, y1, x2, y2, radius_of_penguin)

                existFirst = False
                existSecond = False
                for k in list_of_neighbours:
                    if abs(x3 - peripheral_penguins[k].position[0]) < 0.001 and abs(y3 - peripheral_penguins[k].position[1]) < 0.001:
                        existFirst = True
                    if abs(x4 - peripheral_penguins[k].position[0]) < 0.001 and abs(y4 - peripheral_penguins[k].position[1]) < 0.001:
                        existSecond = True
                if not existFirst and shapely.geometry.Point(x3,y3).within(self.polygon):
                    peripheral_penguins[q] = Penguin.Penguin(ID=q, edge=True, heat_loss=0, position=(x3, y3),
                                                             radius=radius_of_penguin, neighbours=[i, j])
                    circles[q] = plt.Circle((x3, y3), radius_of_penguin, fc="cyan", edgecolor="black")
                    text[q] = plt.text(x3, y3, "ID: " + str(q))
                    board.add_patch(circles[q])
                    plt.draw()
                    peripheral_penguins[i].addNeighbour(q)
                    peripheral_penguins[j].addNeighbour(q)
                    q += 1
                    clock += 1
                    # list_of_neighbours.append(q - 1)
                if not existSecond and shapely.geometry.Point(x4,y4).within(self.polygon):
                    peripheral_penguins[q] = Penguin.Penguin(ID=q, edge=True, heat_loss=0, position=(x4, y4),
                                                             radius=radius_of_penguin, neighbours=[i, j])
                    circles[q] = plt.Circle((x4, y4), radius_of_penguin, fc="cyan", edgecolor="black")
                    text[q] = plt.text(x4, y4, "ID: " + str(q))
                    board.add_patch(circles[q])
                    plt.draw()
                    peripheral_penguins[i].addNeighbour(q)
                    peripheral_penguins[j].addNeighbour(q)
                    q += 1
                    clock += 1
                    # list_of_neighbours.append(q - 1)
                print(j)
                print(len(list_of_neighbours))
                print(list_of_neighbours)

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
        self.number = int(self.number)
        self.generatePenguins()
