import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle, Circle

# Parameter
L = 10
N = 500
x = np.linspace(0, L, N)

amplitude = 0.18
wavelength = 2.5
frequency = 1.5

k = 2 * np.pi / wavelength
omega = 2 * np.pi * frequency

fig, ax = plt.subplots(figsize=(12, 5))

ax.set_xlim(-1, 12)
ax.set_ylim(-2, 2)
ax.set_aspect("equal")
ax.set_title("Schwingungsübertragung durch Holz auf einen Propeller")
ax.set_xlabel("Position")
ax.set_yticks([])

# Holzstab
wood = Rectangle(
    (0, -0.25),
    L,
    0.5,
    facecolor="#C49A6C",
    edgecolor="black",
    alpha=0.5
)
ax.add_patch(wood)

# Rillen
for pos in np.arange(0.5, 9.5, 0.4):
    ax.plot(
        [pos, pos],
        [-0.25, 0.25],
        color="#795548",
        linewidth=1
    )

# Wellen
wave_forward, = ax.plot(
    [], [], color="blue", linewidth=2,
    label="Hinlaufende Welle"
)

wave_backward, = ax.plot(
    [], [], color="red", linewidth=2,
    label="Reflektierte Welle"
)

wave_total, = ax.plot(
    [], [], color="green", linewidth=2,
    label="Überlagerung"
)

# Propeller
center_x = 10.5
center_y = 0

hub = Circle(
    (center_x, center_y),
    0.12,
    color="black"
)
ax.add_patch(hub)

blades = []

for _ in range(3):
    blade, = ax.plot([], [], linewidth=6,
                     solid_capstyle="round")
    blades.append(blade)

ax.legend(loc="upper left")

# Zeit
dt = 0.025

def update(frame):

    t = frame * dt

    # Hinlaufende Welle
    y_forward = amplitude * np.sin(k*x - omega*t)

    # Reflektierte Welle
    y_backward = amplitude * np.sin(k*x + omega*t)

    # Überlagerung
    y_total = y_forward + y_backward

    wave_forward.set_data(x, y_forward + 1.1)
    wave_backward.set_data(x, y_backward - 1.1)
    wave_total.set_data(x, y_total)

    # Propellerrotation
    angle = 2 * np.pi * 0.8 * t

    for i, blade in enumerate(blades):

        phi = angle + i * 2*np.pi/3

        radius = 0.8

        x_end = center_x + radius*np.cos(phi)
        y_end = center_y + radius*np.sin(phi)

        blade.set_data(
            [center_x, x_end],
            [center_y, y_end]
        )

    return (
        wave_forward,
        wave_backward,
        wave_total,
        *blades
    )

animation = FuncAnimation(
    fig,
    update,
    frames=1000,
    interval=25,
    blit=True
)

plt.show()