import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ============================================================
# Fenster erstellen
# ============================================================

fig, (ax_wave, ax_circle) = plt.subplots(
    1, 2,
    figsize=(14, 6)
)

fig.suptitle(
    r"Warum gilt bei $P_2=(\sin\alpha,\cos\alpha)$: "
    r"$\varphi=\frac{\pi}{2}-\alpha$?",
    fontsize=16
)


# ============================================================
# LINKS: Sinus und Cosinus
# ============================================================

x = np.linspace(0, np.pi / 2, 500)

ax_wave.plot(
    x,
    np.sin(x),
    linewidth=2,
    label=r"$x=\sin(\alpha)$"
)

ax_wave.plot(
    x,
    np.cos(x),
    linewidth=2,
    label=r"$y=\cos(\alpha)$"
)

ax_wave.set_xlim(0, np.pi / 2)
ax_wave.set_ylim(0, 1.15)

ax_wave.set_xticks(
    [0, np.pi/6, np.pi/4, np.pi/3, np.pi/2],
    [
        r"$0$",
        r"$\frac{\pi}{6}$",
        r"$\frac{\pi}{4}$",
        r"$\frac{\pi}{3}$",
        r"$\frac{\pi}{2}$"
    ]
)

ax_wave.set_xlabel(r"$\alpha$")
ax_wave.set_ylabel("Wert")

ax_wave.grid(alpha=0.3)
ax_wave.legend()

ax_wave.set_title(
    "Die Koordinaten werden durch α bestimmt"
)


# Animierte Punkte auf den Wellen
sin_point, = ax_wave.plot(
    [], [],
    "o",
    markersize=10
)

cos_point, = ax_wave.plot(
    [], [],
    "o",
    markersize=10
)

vertical_line, = ax_wave.plot(
    [], [],
    "--",
    color="gray",
    alpha=0.6
)

wave_text = ax_wave.text(
    0.05,
    0.05,
    "",
    transform=ax_wave.transAxes,
    fontsize=12
)


# ============================================================
# RECHTS: Einheitskreis
# ============================================================

t = np.linspace(0, 2*np.pi, 500)

ax_circle.plot(
    np.cos(t),
    np.sin(t),
    color="gray",
    linewidth=1.5
)

ax_circle.axhline(
    0,
    color="black",
    linewidth=1
)

ax_circle.axvline(
    0,
    color="black",
    linewidth=1
)

ax_circle.set_xlim(-0.2, 1.3)
ax_circle.set_ylim(-0.2, 1.3)

ax_circle.set_aspect("equal")

ax_circle.set_xlabel("x")
ax_circle.set_ylabel("y")

ax_circle.grid(alpha=0.2)

ax_circle.set_title(
    r"Polarwinkel $\varphi$ wird von der x-Achse gemessen"
)


# ============================================================
# Elemente im Kreis
# ============================================================

# Radius zum Punkt
radius, = ax_circle.plot(
    [], [],
    linewidth=3
)

# Punkt
point, = ax_circle.plot(
    [], [],
    "o",
    markersize=11
)

# Projektionen
projection_x, = ax_circle.plot(
    [], [],
    "--",
    alpha=0.6
)

projection_y, = ax_circle.plot(
    [], [],
    "--",
    alpha=0.6
)


# Winkel phi
phi_arc, = ax_circle.plot(
    [], [],
    linewidth=4,
    label=r"$\varphi$"
)

# Winkel alpha
alpha_arc, = ax_circle.plot(
    [], [],
    linewidth=4,
    label=r"$\alpha$"
)

ax_circle.legend(loc="upper right")


# Beschriftungen der Winkel
phi_label = ax_circle.text(
    0, 0, "",
    fontsize=14
)

alpha_label = ax_circle.text(
    0, 0, "",
    fontsize=14
)


# Text unten
circle_text = ax_circle.text(
    0.02,
    -0.13,
    "",
    transform=ax_circle.transAxes,
    fontsize=12
)


# ============================================================
# Animation
# ============================================================

def update(alpha):

    # --------------------------------------------------------
    # 1. Koordinaten aus der Aufgabe
    # --------------------------------------------------------

    x_value = np.sin(alpha)
    y_value = np.cos(alpha)

    # --------------------------------------------------------
    # 2. Der tatsächliche Polarwinkel
    # --------------------------------------------------------

    phi = np.pi / 2 - alpha

    # ========================================================
    # LINKE SEITE
    # ========================================================

    sin_point.set_data(
        [alpha],
        [x_value]
    )

    cos_point.set_data(
        [alpha],
        [y_value]
    )

    vertical_line.set_data(
        [alpha, alpha],
        [0, 1.1]
    )

    wave_text.set_text(
        rf"$\alpha={np.degrees(alpha):.0f}^\circ$"
        "\n\n"
        rf"$x=\sin(\alpha)={x_value:.2f}$"
        "\n"
        rf"$y=\cos(\alpha)={y_value:.2f}$"
    )


    # ========================================================
    # RECHTE SEITE
    # ========================================================

    # Punkt P2
    point.set_data(
        [x_value],
        [y_value]
    )

    # Radius
    radius.set_data(
        [0, x_value],
        [0, y_value]
    )


    # --------------------------------------------------------
    # Projektionen auf x und y
    # --------------------------------------------------------

    projection_x.set_data(
        [0, x_value],
        [y_value, y_value]
    )

    projection_y.set_data(
        [x_value, x_value],
        [0, y_value]
    )


    # ========================================================
    # φ:
    # wird von der x-Achse bis zum Vektor gemessen
    # ========================================================

    phi_angles = np.linspace(
        0,
        phi,
        100
    )

    phi_radius = 0.35

    phi_arc.set_data(
        phi_radius * np.cos(phi_angles),
        phi_radius * np.sin(phi_angles)
    )


    # Position des φ-Textes
    phi_middle = phi / 2

    phi_label.set_position(
        (
            0.43 * np.cos(phi_middle),
            0.43 * np.sin(phi_middle)
        )
    )

    phi_label.set_text(r"$\varphi$")


    # ========================================================
    # α:
    # wird hier vom Vektor bis zur y-Achse gemessen
    # ========================================================

    alpha_angles = np.linspace(
        phi,
        np.pi / 2,
        100
    )

    alpha_radius = 0.60

    alpha_arc.set_data(
        alpha_radius * np.cos(alpha_angles),
        alpha_radius * np.sin(alpha_angles)
    )


    # Position des α-Textes
    alpha_middle = (
        phi + np.pi / 2
    ) / 2

    alpha_label.set_position(
        (
            0.68 * np.cos(alpha_middle),
            0.68 * np.sin(alpha_middle)
        )
    )

    alpha_label.set_text(r"$\alpha$")


    # ========================================================
    # Erklärung
    # ========================================================

    circle_text.set_text(
        rf"$\alpha={np.degrees(alpha):.0f}^\circ$"
        "   "
        rf"$\varphi={np.degrees(phi):.0f}^\circ$"
        "\n"
        r"$\alpha+\varphi=90^\circ$"
        r" \quad\Rightarrow\quad "
        r"$\varphi=90^\circ-\alpha$"
    )

    return (
        sin_point,
        cos_point,
        vertical_line,
        point,
        radius,
        projection_x,
        projection_y,
        phi_arc,
        alpha_arc,
        phi_label,
        alpha_label,
        wave_text,
        circle_text
    )


# ============================================================
# Frames
# ============================================================

# Nicht ganz bei 0 starten, damit beide Winkel sichtbar sind
frames_forward = np.linspace(
    np.radians(5),
    np.radians(85),
    120
)

# Danach wieder zurück
frames_backward = frames_forward[::-1]

frames = np.concatenate(
    [frames_forward, frames_backward]
)


ani = FuncAnimation(
    fig,
    update,
    frames=frames,
    interval=40,
    repeat=True
)

plt.tight_layout()
plt.show()