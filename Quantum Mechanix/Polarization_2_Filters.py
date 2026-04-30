import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# -----------------------------
# Einstellungen
# -----------------------------
theta_in = np.deg2rad(45)     # Eingangspolarisation
theta_f1 = np.deg2rad(90)     # Filter 1 bleibt fest

x = np.linspace(0, 12, 900)
k = 2 * np.pi / 3
omega = 2.5

filter1_x = 4.5
filter2_x = 8.5

A0 = 1.0

# -----------------------------
# Projektion
# -----------------------------
def project(A, old_angle, new_angle):
    return A * np.cos(new_angle - old_angle)

# -----------------------------
# Figure + Slider
# -----------------------------
fig, ax = plt.subplots(figsize=(13, 6))
plt.subplots_adjust(bottom=0.22)

ax.set_xlim(0, 12)
ax.set_ylim(-2.5, 2.5)
ax.axis("off")

ax.plot([0, 12], [0, 0], lw=2)
ax.set_title("Polarisationsfilter mit drehbarem zweiten Filter")

# Slider

slider_ax = plt.axes([0.2, 0.08, 0.65, 0.04])
angle_slider = Slider(
    ax=slider_ax,
    label="Filter 2 Winkel",
    valmin=0,
    valmax=180,
    valinit=30,
    valstep=1
)

# -----------------------------
# Filter zeichnen
# -----------------------------
filter_artists = []

def clear_filter_artists():
    global filter_artists
    for obj in filter_artists:
        obj.remove()
    filter_artists = []

def draw_filter(x0, angle, label, size=1.8):
    height = size
    width = 0.55

    # Rahmen
    artist, = ax.plot(
        [x0 - width/2, x0 + width/2, x0 + width/2, x0 - width/2, x0 - width/2],
        [-height, -height, height, height, -height],
        lw=2
    )
    filter_artists.append(artist)

    # Gitterlinien
    for s in np.linspace(-0.22, 0.22, 7):
        artist, = ax.plot(
            [x0 + s, x0 + s],
            [-height, height],
            lw=1
        )
        filter_artists.append(artist)

    # Durchlassrichtung als Pfeil
    L = 1.0
    arrow = ax.arrow(
        x0, -2.15,
        L * np.cos(angle),
        L * np.sin(angle),
        head_width=0.1,
        head_length=0.15,
        lw=2,
        length_includes_head=True
    )
    filter_artists.append(arrow)

    txt = ax.text(x0, 2.05, label, ha="center", fontsize=12)
    filter_artists.append(txt)

# fester Filter 1 wird separat gezeichnet
def draw_static_filter1():
    height = 2.0
    width = 0.55
    x0 = filter1_x

    ax.plot(
        [x0 - width/2, x0 + width/2, x0 + width/2, x0 - width/2, x0 - width/2],
        [-height, -height, height, height, -height],
        lw=2
    )

    for s in np.linspace(-0.22, 0.22, 7):
        ax.plot([x0 + s, x0 + s], [-height, height], lw=1)

    ax.arrow(
        x0, -2.15,
        1.0 * np.cos(theta_f1),
        1.0 * np.sin(theta_f1),
        head_width=0.1,
        head_length=0.15,
        lw=2,
        length_includes_head=True
    )

    ax.text(x0, 2.05, "Filter 1 fest", ha="center", fontsize=12)

draw_static_filter1()

# -----------------------------
# Wellen
# -----------------------------
line_before, = ax.plot([], [], lw=3)
line_mid, = ax.plot([], [], lw=3)
line_after, = ax.plot([], [], lw=3)

arrows = []

def clear_arrows():
    global arrows
    for a in arrows:
        a.remove()
    arrows = []

def draw_arrows(xs, ys, angle):
    global arrows
    for xi, yi in zip(xs, ys):
        dx = 0.42 * yi * np.cos(angle)
        dy = 0.42 * yi * np.sin(angle)

        arr = ax.arrow(
            xi, 0,
            dx, dy,
            head_width=0.06,
            head_length=0.08,
            lw=1.2,
            alpha=0.8
        )
        arrows.append(arr)

# Texte
text_amp = ax.text(8.5, -2.35, "", ha="center", fontsize=12)

# -----------------------------
# Animation
# -----------------------------
def update(frame):
    clear_arrows()
    clear_filter_artists()

    t = frame * 0.07

    # Winkel aus Slider lesen
    theta_f2 = np.deg2rad(angle_slider.val)

    # Filter 2 neu zeichnen
    draw_filter(filter2_x, theta_f2, "Filter 2 drehbar", size=1.8)

    # Amplituden nach Filtern
    A1 = project(A0, theta_in, theta_f1)
    A2 = project(A1, theta_f1, theta_f2)

    # Bereiche
    xb = x[x < filter1_x]
    xm = x[(x >= filter1_x) & (x < filter2_x)]
    xa = x[x >= filter2_x]

    # Wellen
    yb = A0 * np.cos(k * xb - omega * t)
    ym = A1 * np.cos(k * xm - omega * t)
    ya = A2 * np.cos(k * xa - omega * t)

    line_before.set_data(xb, yb)
    line_mid.set_data(xm, ym)
    line_after.set_data(xa, ya)

    draw_arrows(
        np.linspace(1, filter1_x - 0.5, 6),
        A0 * np.cos(k * np.linspace(1, filter1_x - 0.5, 6) - omega * t),
        theta_in
    )

    draw_arrows(
        np.linspace(filter1_x + 0.5, filter2_x - 0.5, 6),
        A1 * np.cos(k * np.linspace(filter1_x + 0.5, filter2_x - 0.5, 6) - omega * t),
        theta_f1
    )

    draw_arrows(
        np.linspace(filter2_x + 0.5, 11, 6),
        A2 * np.cos(k * np.linspace(filter2_x + 0.5, 11, 6) - omega * t),
        theta_f2
    )

    intensity_factor = (A2 / A1) ** 2 if A1 != 0 else 0
    text_amp.set_text(
        f"Filter 2: {angle_slider.val:.0f}°   |   relative Intensität: {intensity_factor:.2f}"
    )

    return line_before, line_mid, line_after, text_amp

ani = FuncAnimation(fig, update, frames=400, interval=30, blit=False)

plt.show()