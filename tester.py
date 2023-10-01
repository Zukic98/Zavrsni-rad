import math

from matplotlib import pyplot as plt

fig1, ax = plt.subplots()

ax.set_xlim(0, 100)
ax.set_ylim(0,100)
ax.set_box_aspect(1)

def get_partition_of_neighbours(central_position_x,central_position_y, number_of_neighbours):
    if number_of_neighbours == 0:
        c1 = plt.Circle((central_position_x, central_position_y), radius=3)
        ax.add_patch(c1)
    if number_of_neighbours == 1:
        c2 = plt.Circle((central_position_x, central_position_y + 6), radius=3)
        plt.gca().add_artist(c2)
    if number_of_neighbours == 2:
        c3 = plt.Circle((central_position_x, central_position_y - 6), radius=3)
        plt.gca().add_artist(c3)
    if number_of_neighbours == 3:
        c4 = plt.Circle((central_position_x + 5.2, central_position_y + 3), radius=3)
        plt.gca().add_artist(c4)
    if number_of_neighbours == 4:
        c5 = plt.Circle((central_position_x + 5.2, central_position_y - 3), radius=3)
        plt.gca().add_artist(c5)
    if number_of_neighbours == 5:
        c6 = plt.Circle((central_position_x - 5.2, central_position_y + 3), radius=3)
        plt.gca().add_artist(c6)
    if number_of_neighbours == 6:
        c7 = plt.Circle((central_position_x - 5.2, central_position_y - 3), radius=3)
        plt.gca().add_artist(c7)

number_of_penguins = 50
number_of_clusters = number_of_penguins/6

for i in range (1,number_of_penguins+1,6):
    get_partition_of_neighbours(40+i*10,40*i*10,6)

#get_partition_of_neighbours(15, 15,number_of_penguins % number_of_clusters)


plt.draw()