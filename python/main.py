import sys
import numpy as np
import random
from submarine import Submarine, simulate_random
from world_generation import get_random_sea_floor, add_wrecks, wrecs_coordinates
import json
from plot import plot_simulation

if __name__ == "__main__":
    N = 10

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

    sim_name = "simulation"
    if len(sys.argv) > 5:
        sim_name = sys.argv[5]

    Z = get_random_sea_floor(hills_num, N)
    add_wrecks(wrecks_num, N)

    wrecks = wrecs_coordinates[:]
    max_hill = np.max(Z)
    subs = []
    for _ in range(submarine_num):
        x = random.randint(0, N - 1)
        y = random.randint(0, N - 1)
        ground = Z[x, y]
        altitude = max_hill + 5
        subs.append(Submarine(x, y, z=altitude, speed=2.0))
    history = simulate_random(Z, subs, wrecks, time_steps=100)

    paths_x = [[] for _ in subs]
    paths_y = [[] for _ in subs]
    paths_z = [[] for _ in subs]
    prob = [[] for _ in subs]

    for step_data in history:
        for i, data in enumerate(step_data):
            px, py, pz = data['pos']
            paths_x[i].append(px)
            paths_y[i].append(py)
            paths_z[i].append(pz)
            prob[i].append(data['prob'])

    submarines_data = []
    for i in range(len(subs)):
        path_points = [
            {"x": x, "y": y, "z": z, "prob": prob}
            for x, y, z, prob in zip(paths_x[i], paths_y[i], paths_z[i], prob[i])
        ]
        submarines_data.append({
            "id": i,
            "path": path_points
        })

    print(json.dumps({"submarines": submarines_data, "seafloor": Z.tolist(), "dimension": N, "wrecks": wrecks, "simulationName": sim_name}, indent=2))


    plot_simulation(N, Z, paths_x, paths_y, paths_z, wrecks, sim_name)

