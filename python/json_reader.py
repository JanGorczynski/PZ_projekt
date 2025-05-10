import json
import numpy as np
def read_data_from_json(file_path):


    with open(file_path, 'r') as file:
        json_data = json.load(file)

    submarines = json_data['submarines']
    seafloor = json_data['seafloor']
    dimension = json_data['dimension']
    wrecks = json_data['wrecks']


    Z = np.array(seafloor)


    # Extract paths of submarines
    paths_x = []
    paths_y = []
    paths_z = []
    prob = []
    for submarine in submarines:
        path_x = [point['x'] for point in submarine['path']]
        path_y = [point['y'] for point in submarine['path']]
        path_z = [point['z'] for point in submarine['path']]
        prob = [point['prob'] for point in submarine['path']]
        paths_x.append(path_x)
        paths_y.append(path_y)
        paths_z.append(path_z)
        prob.append(prob)



    return dimension, Z, paths_x, paths_y, paths_z, wrecks, prob