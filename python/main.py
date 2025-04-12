import sys
import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from submarine import Submarine, simulate_random
from world_generation import get_random_sea_floor, add_wrecks, wrecs_coordinates

if __name__ == "__main__":
    N = 1000

    if len(sys.argv) > 1:
        N = int(sys.argv[1])
        # print(f"N: {N}")

    hills_num = 8

    if len(sys.argv) > 2:
        hills_num = int(sys.argv[2])
        # print(f"hills num: {hills_num}")

    wrecks_num = 8

    if len(sys.argv) > 3:
        wrecks_num = int(sys.argv[3])
        # print(f"wrecks num: {wrecks_num}")

    submarine_num = 3

    if len(sys.argv) > 4:
        submarine_num = int(sys.argv[4])
        # print(f"Submarine: {wrecks_num}")

    Z = get_random_sea_floor(hills_num)
    add_wrecks(wrecks_num)

    wrecks = wrecs_coordinates[:]
    max_hill = np.max(Z)
    subs = []
    for _ in range(submarine_num):
        x = random.randint(0, N - 1)
        y = random.randint(0, N - 1)
        ground = Z[x, y]
        altitude = max_hill + 5
        subs.append(Submarine(x, y, z=altitude, speed=2.0))
    history = simulate_random(Z, subs, wrecks, time_steps=1000)

    paths_x = [[] for _ in subs]
    paths_y = [[] for _ in subs]
    paths_z = [[] for _ in subs]
    for step_data in history:
        for i, data in enumerate(step_data):
            px, py, pz = data['pos']
            paths_x[i].append(px)
            paths_y[i].append(py)
            paths_z[i].append(pz)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot sea floor
    x_coords = np.arange(N)
    y_coords = np.arange(N)
    X, Y = np.meshgrid(x_coords, y_coords)
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)

    # Plot submarine paths
    for i in range(len(subs)):
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
    plt.savefig("submarine_simulation_matplotlib.png", dpi=300, bbox_inches='tight')
    plt.show()