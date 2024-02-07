import Penguin
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