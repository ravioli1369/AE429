import numpy as np
import matplotlib.pyplot as plt

THETA = np.pi / 6  # rad
V = 8 * np.array([np.cos(THETA), np.sin(THETA)])  # m/s
delta_R = 0.3  # m
RADIUS = 4  # m
MASS = 10  # kg

t = 0
dt = 0.01
T = 5

N = int(RADIUS / (delta_R))
layers = np.array([3 + 2 * i for i in range(N)])

energy = 0.5 * (MASS / np.sum(layers)) * layers[-1] * np.linalg.norm(V) ** 2

layer = N - 1
outer_layer_distance = np.array([0, 0]).astype(float)
layer_distance = 0
net_center_distance = 0

time_to_plot = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
while t < T:
    layer_distance += np.linalg.norm(V) * dt
    if outer_layer_distance[1] < N * delta_R:
        outer_layer_distance += V * dt
    else:
        outer_layer_distance[0] += V[0] * dt

    if layer == 0:
        net_center_distance += 2 * V[0] * dt
    elif layer_distance > delta_R:
        V = V * (np.sum(layers[layer:]) / (layers[layer - 1] + np.sum(layers[layer:])))
        layer -= 1
        layer_distance = 0

    t += dt

    if np.min(np.abs(time_to_plot - t)) < 0.01:
        plt.plot(
            [net_center_distance, outer_layer_distance[0]],
            [0, outer_layer_distance[1]],
            "ro-",
        )
        plt.plot(
            [net_center_distance, outer_layer_distance[0]],
            [0, -outer_layer_distance[1]],
            "ro-",
        )
        plt.xlim(-1, 10)
        plt.ylim(-6, 6)
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.title(f"t = {int(t)} s")
        plt.savefig(f"{int(np.rint(t))}.png", dpi=300)
        plt.close()


print(
    f"Outer Layer distance (x): {outer_layer_distance[0]:.2f} m\n\
Net Center distance (x_center): {net_center_distance:.2f} m\n\
Net Exapnsion (y): {outer_layer_distance[1]:.2f} m\n\
Total time taken: {t:.2f} s \n\
Forward Velocity at the end: {V[0]:.2f} m/s \n\
Net Expansion Velocity at the end: {V[1]:.2f} m/s\n\n\
Total Energy Required: {energy:.2f} J"
)
