import json
import sys
from json_reader import read_data_from_json
from plot import plot_simulation
import numpy as np
from json_writer import write_data_to_json
from submarine import detection_probability


def prediction(N, Z, paths_x, paths_y, paths_z, wrecks, prob,sim_name):
    
    nearest_points = []
    threshold = 20
    speed = 1
    _s_based = 1
    _offset = 0
    _epsilon = 0.1
    
    for wreck in wrecks:
        min_dist = float('inf')
        min_dist_index = 0
        min_dist_sub = 0
        wx, wy, wz = wreck
        
        for _s in range(len(paths_x)):
            for i in range(len(paths_x[_s])):
                bx = paths_x[_s][i]
                by = paths_y[_s][i]
                bz = paths_z[_s][i]
                d = np.sqrt((bx - wx)**2 + (by - wy)**2 + (bz - wz)**2)
                if d < min_dist:
                    min_dist_index=i
                    min_dist_sub=_s
                    min_dist = d
        nearest_points.append((min_dist_index,min_dist_sub,wreck))
    
    for _index,_submarine,_wreck in nearest_points:
        wx, wy, wz = _wreck
        _n = _index
        _s = _submarine
        
        if _s_based!=_s:
            _offset = 0
            _s_based = _s
        
        _n += _offset
        
        #if point goes beyond the range of the new boat's path
        if _n>=len(paths_x[_s]):
            continue
            
        paths_x[_s][_n+1] = wx 
        paths_y[_s][_n+1] = wy
        paths_z[_s][_n+1] = wz
        prob[_s][_n+1] = 1

        _x = paths_x[_s][_n]  
        _y = paths_y[_s][_n] 
        _z = paths_x[_s][_n]  
        
        dist_2d = np.sqrt((wx-_x)**2+(wy-_y)**2)
            
        if dist_2d > threshold:
            
            x_points = []
            y_points = []
            frac = speed/dist_2d
            dx = wx-_x
            dy = wy-_y
            additional_prob = []
            
            while abs(wx-_x)>_epsilon and abs(wy-_y)>_epsilon:
                _x += dx * frac
                _y += dy * frac
                x_points.append(_x)
                y_points.append(_y)
                additional_prob.append(detection_probability(np.sqrt((wx-_x)**2+(wy-_y)**2+(wz-_z)**2)))
           
            additional_points_len = len(x_points)
            if (len(paths_x[_s])-2*additional_points_len-1)<_n:
                continue

            paths_x[_s] = paths_x[_s][:-2*additional_points_len]
            paths_y[_s] = paths_y[_s][:-2*additional_points_len]
            paths_z[_s] = paths_z[_s][:-2*additional_points_len]
            prob[_s] = prob[_s][:-2*additional_points_len]

            x_points.append(x_points[::-1])
            y_points.append(y_points[::-1])
            additional_prob.append(additional_prob[::-1])

            paths_x[_s].insert(_n,x_points)
            paths_y[_s].insert(_n,y_points)
            paths_z[_s].insert(_n,2*additional_points_len*[_z])
            prob[_s].insert(_n,additional_prob)

            _offset += 2*additional_points_len
    
    #for testing, how it looks
    #plot_simulation(N, Z, paths_x, paths_y, paths_z, wrecks, "predict_sim")
    write_data_to_json(N, Z, paths_x, paths_y, paths_z, wrecks, prob,sim_name)

def main():
    N, Z, paths_x, paths_y, paths_z, wrecks, prob, sim_name = read_data_from_json(sys.argv[1])
    prediction(N, Z, paths_x, paths_y, paths_z, wrecks, prob,sim_name)


if __name__ == "__main__":
    main()
