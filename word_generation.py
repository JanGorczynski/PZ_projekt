import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import random

N = 1000

def add_hill(Z,N,x_hill,y_hill,radius,height):
    for x in range(N):
        for y in range(N):
            if ((x-x_hill)**2+(y-y_hill)**2) < radius:
                Z[x,y] =  (radius - ((x-x_hill)**2+(y-y_hill)**2))/1000 * height
    return  Z

def get_random_sea_floor(hill_number: int = 8):
    
    Z = np.zeros((N,N))
    for _ in range(hill_number):
        X_hill = int(random.random()*N)
        Y_hill = int(random.random()*N)
        radius = (random.random()+0.5)*N*10
        height = random.uniform(0.5, 3)
        Z = add_hill(Z,N,X_hill,Y_hill,radius,height)
    return Z

def draw_sea_floor(Z):
    X = np.linspace(0, N-1, N)
    Y = np.linspace(0, N-1, N)
    X, Y = np.meshgrid(X, Y)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_zlim(0, 100)
    ax.set_title('Sea floor visualization')

    plt.show()
