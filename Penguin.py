import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt

class Penguin:
    ID = 0
    edge = True
    heat_loss = 0.
    position = (0, 0)
    radius = 0
    neighbours = []

    def __init__(self, ID=0, edge=True, heat_loss=0, position=(0, 0), radius = 0, neighbours=[]):
        self.ID = ID
        self.edge = edge
        self.position = position
        self.radius = radius
        self.neighbours = neighbours
        self.heat_loss = 0
    def updateHeatLoss(self, above_boundary, belove_boundary, delta_r, f):
        # Rombergs algorithm for integration
        N = 2
        h = (above_boundary - belove_boundary) / N
        s = (f(delta_r, belove_boundary) + f(delta_r, above_boundary)) / 2
        I_old = s
        I = []
        eps = 0.00000001
        for i in range(1, 6):
            for j in range(1, int(N / 2)):
                s = s + f(delta_r, belove_boundary + (2 * j - 1) * h)
            I[i] = h * s
            p = 4
            for k in range(i - 1, -1, 1):
                I[k] = (p * I[k + 1] - I[k]) / (p - 1)
                p = 4 * p
            if abs(I[1] - I_old) <= eps:
                self.heat_loss = I[1]
                break
            I_old = I[1]
            h /= 2
            N *= 2
            return -self.heat_loss

    def addNeighbour(self,neighbour_id):
        self.neighbours.append(neighbour_id)
