import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt

class Penguin:
    ID = 0
    edge = False
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

#1 generate penguins
def algorithm():
    peripheral_penguins = {}
    central_penguins = {}

    for i in range(1, 43):
        peripheral_penguins[i] = Penguin(i, True, 0, (i, i))
    for i in range(1, 57):
        central_penguins[i] = Penguin(i, False, 0, (i, i))

# 2 Compute the wind flow around the huddle


#def wind_velocity():
#    return real_part_Joukowsky(Inverse_Schwarz_Cristoffel)


# 3 Compute the profile around the huddle

# 4 Compute the local heat rate loss for each penguin,#5 Add random variations,#6 Identify and relocate the penguin

    max_heat_loss = float('-inf')

    min_heat_loss = float('inf')

    index_of_max = 0
    index_of_min = 0
# finding maximum and minimal heat loss for each penguin
    for key, penguin in peripheral_penguins.items():

        # penguin.update_heat_loss(1,1,1,1)

        if max_heat_loss < penguin.heat_loss:
            max_heat_loss = penguin.heat_loss
            index_of_max = key

        if min_heat_loss > penguin.heat_loss:
            min_heat_loss = penguin.heat_loss
            index_of_min = key

# update list of neigbours
# 1.1 update list of neigbours on position where was mover
    mover = peripheral_penguins[index_of_max]
    mover_id = mover.ID

    old_neighbours = mover.neighbours

    for x in old_neighbours:
        if x not in peripheral_penguins:
            temporary_penguin = central_penguins[x]
            temporary_penguin.neighbours.remove(mover_id)

            del central_penguins[x]
            peripheral_penguins[x] = temporary_penguin

        else:
            peripheral_penguins[x].neighbours.remove(mover_id)

# 1.2 get new penguin to edge, because he doesn't have six neigbours
    peripheral_penguins[index_of_min].neighbours.append(mover_id)
    peripheral_penguins[index_of_max].neighbours.append(index_of_min)

    second_max_heat_loss = float('-inf')
    index_of_second_max_heat_loss = 0

    for x in peripheral_penguins[index_of_min].neighbours:
        if x in peripheral_penguins and peripheral_penguins[x].heat_loss > second_max_heat_loss:
            second_max_heat_loss = peripheral_penguins[x].heat_loss
            index_of_second_max_heat_loss = x

    peripheral_penguins[index_of_max].neighbours.append(index_of_second_max_heat_loss)
    peripheral_penguins[index_of_second_max_heat_loss].neighbours.append(index_of_max)
