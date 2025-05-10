import json
import sys
from json_reader import read_data_from_json

def heatmap(N, Z, paths_x, paths_y, paths_z, wrecks, prob):
    pass
def main():
    N, Z, paths_x, paths_y, paths_z, wrecks, prob = read_data_from_json(sys.argv[1])
    heatmap(N, Z, paths_x, paths_y, paths_z, wrecks, prob)


if __name__ == "__main__":
    main()
