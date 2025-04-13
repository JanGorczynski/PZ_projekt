import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import random

hills_coordinates = []
wrecs_coordinates = []


def add_hill(Z, N, x_hill, y_hill, radius, height):
    for x in range(N):
        for y in range(N):
            if ((x - x_hill) ** 2 + (y - y_hill) ** 2) < radius:
                Z[x, y] = (radius - ((x - x_hill) ** 2 + (y - y_hill) ** 2)) / 1000 * height
                hills_coordinates.append((x, y, Z[x, y]))
    return Z


def get_random_sea_floor(hill_number: int = 8, N=1000):
    Z = np.zeros((N, N))
    for _ in range(hill_number):
        X_hill = int(random.random() * N)
        Y_hill = int(random.random() * N)
        radius = (random.random() + 0.5) * N * 10
        height = random.uniform(0.5, 3)
        Z = add_hill(Z, N, X_hill, Y_hill, radius, height)
    return Z


def add_wrecks(n: int = 8, N=1000):
    hills_wrecks = int(n / 4)
    number_of_wrecks = 0
    while number_of_wrecks < hills_wrecks:
        wreck = random.choice(hills_coordinates)
        if wreck not in wrecs_coordinates:
            wrecs_coordinates.append(wreck)
            number_of_wrecks += 1

    while number_of_wrecks < n:
        X = int(random.random() * N)
        Y = int(random.random() * N)

        is_valid = True
        for cord in hills_coordinates:
            if X == cord[0] and Y == cord[1]:
                is_valid = False
                break

            if is_valid and (X, Y, 0) not in wrecs_coordinates:
                wrecs_coordinates.append((X, Y, 0))
                number_of_wrecks += 1


def draw_sea_floor(Z, N=1000):
    X = np.linspace(0, N - 1, N)
    Y = np.linspace(0, N - 1, N)
    X, Y = np.meshgrid(X, Y)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    # if you want to see all the wrecks more crearly
    # ax.view_init(elev=90, azim=90)
    ax.plot_surface(X, Y, Z, cmap='viridis')
    for (X, Y, Z) in wrecs_coordinates:
        ax.scatter(X, Y, Z + 55, color='red', s=15)
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_zlim(0, 100)
    ax.set_title('Sea floor visualization')

    plt.show()
