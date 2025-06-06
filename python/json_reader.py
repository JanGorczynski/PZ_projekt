import json
import numpy as np

# This script reads simulation data from a JSON file, including submarine paths, seafloor topography, wreck positions, and grid dimensions.
# It parses the data into structured NumPy arrays and lists for further analysis or visualization.
# Submarine path coordinates (x, y, z) and detection probabilities are extracted step by step.
# The function returns all relevant data for downstream use in simulations or plots.


def read_data_from_json(file_path):


    with open(file_path, 'r') as file:
        json_data = json.load(file)

    submarines = json_data['submarines']
    seafloor = json_data['seafloor']
    dimension = json_data['dimension']
    wrecks = json_data['wrecks']
    sim_name = json_data['simulationName']


    Z = np.array(seafloor)


    # Extract paths of submarines
    paths_x = []
    paths_y = []
    paths_z = []
    probs = []
    for submarine in submarines:
        path_x = [point['x'] for point in submarine['path']]
        path_y = [point['y'] for point in submarine['path']]
        path_z = [point['z'] for point in submarine['path']]
        prob = [point['prob'] for point in submarine['path']]
        paths_x.append(path_x)
        paths_y.append(path_y)
        paths_z.append(path_z)
        probs.append(prob)



    return dimension, Z, paths_x, paths_y, paths_z, wrecks, probs, sim_name