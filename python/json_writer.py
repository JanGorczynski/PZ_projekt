import json
import numpy as np

# This script writes simulation data from a JSON file, including submarine paths, seafloor topography, wreck positions, and grid dimensions.



def write_data_to_json(dimension, Z, paths_x, paths_y, paths_z, wrecks, prob, sim_name):


    json_data = {}
    seafloor = Z.tolist()
    json_data['dimension'] = dimension
    json_data['seafloor'] = seafloor
    json_data['simulationName'] = sim_name
    submarines = []

    for _ in range(len(paths_x)):
        submarines.append({})
        submarines[_]['id'] = _+1
        submarines[_]['path'] = []
        for i in range(len(paths_x[0])):
            submarines[_]['path'].append({'x':paths_x[_][i],'y':paths_y[_][i],'z':paths_z[_][i],'prob':prob[_][i]})
    
    json_data["submarines"] = submarines
    json_data['wrecks'] = wrecks
    json_object = json.dumps(json_data, indent=2)
    file_path = "./simulation_data/"+sim_name+"_predict.json"
    with open(file_path, "w") as outfile:
        outfile.write(json_object)