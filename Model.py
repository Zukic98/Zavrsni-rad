import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt
import formulas
class ModelSample:
    name = None
    number = None
    Peclet = None
    R = None
    polygon = None

    def __init__(self):
        pass

    def generatePenguins(self):
        #define polygon boundaries of huddle
        x, y = self.polygon.exterior.xy
        plt.plot(x, y, c="blue")
        #find center of polygon
        x,y = formulas.findCenterOfPolygon(self.polygon)
        #create core
        radius_of_penguin = formulas.getRadiusForCircles(formulas.areaOfPolygon(self.polygon), self.number)
        for i in range(1,self.number + 1):
            if :

        for i in range(1, 43):
            peripheral_penguins[i] = Penguin(i, True, 0, (i, i))
        for i in range(1, 57):
            central_penguins[i] = Penguin(i, False, 0, (i, i))
        plt.plot(x, y, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="green")



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