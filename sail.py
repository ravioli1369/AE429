import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# https://www.sciencedirect.com/book/9780323992992/attitude-dynamics-and-control-of-space-debris-during-ion-beam-transportation
P_SRP = 4.54e-6  # N/m^2
A = 35.0  # m^2
C_R_reflecting = 1.9
C_R_absorbing = 1.1

isa = pd.read_csv("atmosphere_data.csv", comment="#")
Cd = 1.4  # https://en.wikipedia.org/wiki/Drag_coefficient

G = 6.67430e-11  # m^3/kg/s^2
M = 5.972e24  # kg
R = 6371e3  # m
m = 500  # kg

h = 500e3  # m
t = [0.0]
dt = 3600  # s
altitudes = [h]
angles = [0.0]
total_force = [0.0]


def get_dt(h):
    if h > 250e3:
        return 3600
    elif h > 100e3:
        return 10
    else:
        return 10


while h > 0:
    dt = get_dt(h)
    F_g = G * M * m / (R + h) ** 2
    omega = np.sqrt(F_g / (m * (R + h)))
    A_n = A * np.cos(np.sum(angles) + omega * dt)
    angles.append(omega * dt)
    earth_shadow_angle = np.arcsin(R / (R + h))
    current_angle = (np.sum(angles) + omega * dt) % (2 * np.pi)
    if (current_angle > np.pi - earth_shadow_angle) and (current_angle < np.pi):
        C_R = -C_R_reflecting
    elif (current_angle > np.pi) and (current_angle < 2 * np.pi - earth_shadow_angle):
        C_R = C_R_absorbing
    else:
        C_R = 0
    F_SRP = P_SRP * A_n * C_R

    # Calculate the current orbital velocity
    v = np.sqrt(F_g * (R + h) / m)

    density = np.interp(h / 1000, isa["Altitude(km)"], isa["Density(kg/m^3)"])
    F_ATM_DRAG = -0.5 * Cd * A * density * v**2

    # Calculate the change in velocity due to F_SRP
    delta_v = (F_SRP + F_ATM_DRAG) * dt / m

    # Update the velocity
    v_new = v - delta_v

    # Calculate the new altitude using the updated velocity
    h_new = (G * M / (v_new**2)) - R

    # Append the new altitude to the list
    altitudes.append(h_new)

    # Update the altitude
    h = h_new

    # Update the time
    t.append(t[-1] + dt / 60 / 60 / 24)
    total_force.append(np.abs(F_SRP + F_ATM_DRAG))
    print(f"Time: {t[-1]:.2f} days, Altitude: {h / 1000:.2f} km")

# Plot the altitude vs. time
altitudes = altitudes[:-1]
altitudes.append(0)
altitudes = np.array(altitudes) / 1000

fig, ax = plt.subplots(1, 2, dpi=200)

ax[0].plot(t, altitudes)
ax[0].set_xlabel("Time (days)")
ax[0].set_ylabel("Altitude (km)")

ax[1].plot(t, total_force)
ax[1].set_yscale("log")
ax[1].set_xlabel("Time (days)")
ax[1].set_ylabel("Total Force (N)")

fig.tight_layout()
fig.savefig("sail.png")
