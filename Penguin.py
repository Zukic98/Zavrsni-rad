import math
from logging import raiseExceptions

import sys
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

import formulas

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

    def f_radial_derivation(self, delta_r, angle_theta, R, Pe):

        number_of_equations = int(((R-1)/delta_r)-1)
        r_acc = 1 + delta_r

        p = []
        q = []

        for i in range(0,number_of_equations):

            ReJNext = formulas.realPartofJoukowskyTransform(complex(r_acc * math.cos(angle_theta), r_acc * math.sin(angle_theta)))
            ReJ = formulas.realPartofJoukowskyTransform(complex( (r_acc-delta_r) * math.cos(angle_theta), (r_acc-delta_r) * math.sin(angle_theta)))

            C = Pe * (ReJNext - ReJ)

            p.append(2 - C)
            q.append(C - 1)

            r_acc += delta_r

        r = [-1] * number_of_equations

        b = [0] * number_of_equations
        b[0] = 1

        T_prim = formulas.solveSystemOfLinearEquation(p, q, r, b)[0]

        return (T_prim - 1)/delta_r

    def updateHeatLoss(self, above_boundary, belove_boundary, delta_r, R, Pe):
        resultFound = False
        M = 6
        N = 2
        h = (above_boundary - belove_boundary) / N
        s = (self.f_radial_derivation(delta_r, belove_boundary, R, Pe) + self.f_radial_derivation(delta_r, above_boundary, R,
                                                                                        Pe)) / 2
        I_old = s
        I = []
        eps = 10e-12
        for i in range(1, M):
            for j in range(1, int(N / 2)):
                s += self.f_radial_derivation(delta_r, belove_boundary + (2 * j - 1) * h, R, Pe)

            I.append(h * s)

            p = 4

            for k in range(i - 1, -1, 1):
                I[k] = (p * I[k + 1] - I[k]) / (p - 1)
                p = 4 * p

            if abs(I[0] - I_old) < eps:
                self.heat_loss = I[0]
                resultFound = True
                break

            I_old = I[0]

            h /= 2

            N *= 2

        if not resultFound:
            raise ValueError("Precision is not achieved!")

        return abs(self.heat_loss)


    def addNeighbour(self,neighbour_id):
        self.neighbours.append(neighbour_id)

