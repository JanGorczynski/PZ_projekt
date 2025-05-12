import sys

import numpy as np
import matplotlib.pyplot as plt
import json
from json_reader import read_data_from_json

# This script visualizes submarine simulation data in 3D using Matplotlib.
# It plots the sea floor, submarine paths, and wreck locations based on data read from a JSON file.
# The generated visualization is displayed and also saved as a PNG image.

def plot_simulation(N, Z, paths_x, paths_y, paths_z, wrecks):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot sea floor
    x_coords = np.arange(N)
    y_coords = np.arange(N)
    X, Y = np.meshgrid(x_coords, y_coords)
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)

    # Plot submarine paths
    for i in range(len(paths_x)):
        ax.plot(paths_x[i], paths_y[i], paths_z[i], label=f"Submarine {i + 1}")

    # Plot wrecks
    wx = [wreck[0] for wreck in wrecks]
    wy = [wreck[1] for wreck in wrecks]
    wz = [wreck[2] for wreck in wrecks]
    ax.scatter(wx, wy, [z + 1 for z in wz], c='red', marker='x', s=100, label='Wrecks')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_zlim(0, 100)
    ax.legend()

    plt.tight_layout()
    plt.savefig("visualization/submarine_simulation_matplotlib.png", dpi=300, bbox_inches='tight')
    plt.show()



def main():
    N, Z, paths_x, paths_y, paths_z, wrecks, prob = read_data_from_json(sys.argv[1])
    plot_simulation(N, Z, paths_x, paths_y, paths_z, wrecks)


if __name__ == "__main__":
    main()
