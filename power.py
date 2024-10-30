import numpy as np
import matplotlib.pyplot as plt


THETA = np.pi / 6  # rad
V = 8 * np.array([np.sin(THETA), np.cos(THETA)])  # m/s
delta_R = 0.3  # m
RADIUS = 4  # m
MASS = 50e-3  # kg

t = 0
dt = 0.01
bullet_distance = np.array([0.0, 0.0])
center_distance = np.array([0.0, 0.0])
while True:
    bullet_distance += V * dt
    V = V - np.array([0, 9.8]) * dt
    t += dt
    if np.linalg.norm(bullet_distance) > 1 / np.sqrt(2):
        center_distance += np.array([0, 2 * V[1] * dt])
    else:
        center_distance += np.array([0, 0])

    if t >= 0.4:
        plt.plot(0, center_distance[1], "ro")
        plt.plot(bullet_distance[0], bullet_distance[1], "bo")
        plt.plot(-bullet_distance[0], bullet_distance[1], "bo")
        plt.ylim(0, 3)
        plt.xlim(-2, 2)
        plt.show()
        break

    if bullet_distance[0] > 1 / np.sqrt(2):
        V[0] = -V[0]

    if bullet_distance[1] < 0:
        break


# print(
#     f"Outer Layer distance (x): {outer_layer_distance[0]:.2f} m\n\
# Net Center distance (x_center): {net_center_distance:.2f} m\n\
# Net Exapnsion (y): {outer_layer_distance[1]:.2f} m\n\
# Total time taken: {t:.2f} s \n\
# Forward Velocity at the end: {V[0]:.2f} m/s \n\
# Net Expansion Velocity at the end: {V[1]:.2f} m/s\n\n\
# Total Energy Required: {energy:.2f} J"
# )
