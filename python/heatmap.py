import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from json_reader import read_data_from_json

def accumulate_probability_field(N, paths_x, paths_y, probs, influence_radius=5, sigma=2.0):
    field = np.zeros((N, N))

    size = 2 * influence_radius + 1
    x = np.linspace(-influence_radius, influence_radius, size)
    y = np.linspace(-influence_radius, influence_radius, size)
    X, Y = np.meshgrid(x, y)
    kernel = np.exp(-(X**2 + Y**2) / (2 * sigma**2))

    for sub_idx in range(len(paths_x)):
        for x, y, p in zip(paths_x[sub_idx], paths_y[sub_idx], probs[sub_idx]):
            xi = int(round(x))
            yi = int(round(y))
            if 0 <= xi < N and 0 <= yi < N:
                for dx in range(-influence_radius, influence_radius + 1):
                    for dy in range(-influence_radius, influence_radius + 1):
                        nx = xi + dx
                        ny = yi + dy
                        if 0 <= nx < N and 0 <= ny < N:
                            kx = dx + influence_radius
                            ky = dy + influence_radius
                            field[nx, ny] += p * kernel[kx, ky]

    norm = np.nanmax(field)
    if norm > 0:
        field /= norm
    return field.T

def heatmap(N, Z, paths_x, paths_y, paths_z, wrecks, probs, sim_name):
    prob_field = accumulate_probability_field(N, paths_x, paths_y, probs)
    masked_field = np.ma.masked_equal(prob_field, 0)

    plt.figure(figsize=(10, 8))
    cmap = plt.get_cmap('hot').copy()
    cmap.set_bad(color='black')

    img = plt.imshow(masked_field, cmap=cmap, origin='lower', vmin=0, vmax=1)
    plt.colorbar(img, label='Smoothed Detection Probability')

    for x, y, _ in wrecks:
        plt.scatter(x, y, color='cyan', marker='x', s=100)

    plt.title("Submarine Detection Probability Heatmap")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"visualization/heatmap_{sim_name}_{timestamp}.png"
    plt.savefig(filename, dpi=300)
    plt.show()

def main():
    N, Z, paths_x, paths_y, paths_z, wrecks, probs, sim_name = read_data_from_json(sys.argv[1])
    heatmap(N, Z, paths_x, paths_y, paths_z, wrecks, probs, sim_name)

if __name__ == "__main__":
    main()
