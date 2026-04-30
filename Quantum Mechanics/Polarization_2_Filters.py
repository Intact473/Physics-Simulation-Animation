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

ax.plot([0, 12], [0, 0], lw=2, color="black")
ax.set_title("Polarisationsfilter mit sichtbarem E-Feld")

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
        lw=2,
        color="black"
    )
    filter_artists.append(artist)

    # Stäbe liegen SENKRECHT zur Durchlassrichtung
    rod_angle = angle + np.pi / 2

    for s in np.linspace(-0.45, 0.45, 7):
        cx = x0 + s * np.cos(angle)
        cy = s * np.sin(angle)

        L = height

        dx = 0.18 * L * np.cos(rod_angle)
        dy = L * np.sin(rod_angle)

        artist, = ax.plot(
            [cx - dx, cx + dx],
            [cy - dy, cy + dy],
            lw=1.4,
            color="gray"
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
        color="red",
        length_includes_head=True
    )
    filter_artists.append(arrow)

    txt = ax.text(x0, 2.05, label, ha="center", fontsize=12)
    filter_artists.append(txt)

# -----------------------------
# Fester Filter 1
# -----------------------------
def draw_static_filter1():
    height = 2.0
    width = 0.55
    x0 = filter1_x

    ax.plot(
        [x0 - width/2, x0 + width/2, x0 + width/2, x0 - width/2, x0 - width/2],
        [-height, -height, height, height, -height],
        lw=2,
        color="black"
    )

    for s in np.linspace(-0.22, 0.22, 7):
        ax.plot(
            [x0 + s, x0 + s],
            [-height, height],
            lw=1,
            color="gray"
        )

    ax.arrow(
        x0, -2.15,
        1.0 * np.cos(theta_f1),
        1.0 * np.sin(theta_f1),
        head_width=0.1,
        head_length=0.15,
        lw=2,
        color="red",
        length_includes_head=True
    )

    ax.text(x0, 2.05, "Filter 1 fest", ha="center", fontsize=12)

draw_static_filter1()

# -----------------------------
# Wellenlinien
# -----------------------------
line_before, = ax.plot([], [], lw=3, color="blue", label="vor Filter")
line_mid, = ax.plot([], [], lw=3, color="green", label="nach Filter 1")
line_after, = ax.plot([], [], lw=3, color="orange", label="nach Filter 2")

# -----------------------------
# E-Feld-Pfeile
# -----------------------------
E_arrows = []

def clear_E_arrows():
    global E_arrows
    for a in E_arrows:
        a.remove()
    E_arrows = []

def draw_E_arrows(xs, amplitudes, angle, color):
    global E_arrows

    for xi, Ei in zip(xs, amplitudes):
        dx = 0.45 * Ei * np.cos(angle)
        dy = 0.45 * Ei * np.sin(angle)

        arr = ax.arrow(
            xi, 0,
            dx, dy,
            head_width=0.06,
            head_length=0.08,
            lw=1.3,
            color=color,
            alpha=0.9,
            length_includes_head=True
        )
        E_arrows.append(arr)

# -----------------------------
# Texte
# -----------------------------
ax.text(1.0, 1.8, "vor Filter", color="blue", fontsize=12)
ax.text(5.0, 1.8, "nach Filter 1", color="green", fontsize=12)
ax.text(9.0, 1.8, "nach Filter 2", color="orange", fontsize=12)

info_text = ax.text(8.5, -2.38, "", ha="center", fontsize=11)

# -----------------------------
# Animation
# -----------------------------
def update(frame):
    clear_E_arrows()
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

    # Positionen für E-Feld-Pfeile
    xs1 = np.linspace(1, filter1_x - 0.5, 6)
    xs2 = np.linspace(filter1_x + 0.5, filter2_x - 0.5, 6)
    xs3 = np.linspace(filter2_x + 0.5, 11, 6)

    # E-Feld vor Filter
    draw_E_arrows(
        xs1,
        A0 * np.cos(k * xs1 - omega * t),
        theta_in,
        color="blue"
    )

    # E-Feld nach Filter 1
    draw_E_arrows(
        xs2,
        A1 * np.cos(k * xs2 - omega * t),
        theta_f1,
        color="green"
    )

    # E-Feld nach Filter 2
    draw_E_arrows(
        xs3,
        A2 * np.cos(k * xs3 - omega * t),
        theta_f2,
        color="orange"
    )

    # relative Intensität nach Filter 2 bezogen auf nach Filter 1
    delta = theta_f2 - theta_f1
    intensity_factor = np.cos(delta) ** 2

    info_text.set_text(
        f"Filter 2: {angle_slider.val:.0f}°   |   I₂/I₁ = cos²(Δθ) = {intensity_factor:.2f}"
    )

    return line_before, line_mid, line_after, info_text

ani = FuncAnimation(fig, update, frames=400, interval=30, blit=False)

plt.show()