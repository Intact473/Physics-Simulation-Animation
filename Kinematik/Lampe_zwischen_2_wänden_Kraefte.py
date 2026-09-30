import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --------------------------------------------------
# Physikalische Werte
# --------------------------------------------------

T = 150  # Zugkraft im Seil [N]
winkel = np.deg2rad(20)

# Vertikale Komponente EINER Seilhälfte
F_y = T * np.sin(winkel)

# Beide Seilhälften tragen die Lampe
F_G = 2 * F_y

print(f"Vertikale Kraft pro Seilhälfte: {F_y:.2f} N")
print(f"Maximale Gewichtskraft der Lampe: {F_G:.2f} N")


# --------------------------------------------------
# Geometrie der Zeichnung
# --------------------------------------------------

lampe = np.array([0.0, 0.0])

links = np.array([
    -np.cos(winkel),
     np.sin(winkel)
])

rechts = np.array([
    np.cos(winkel),
    np.sin(winkel)
])


# --------------------------------------------------
# Plot vorbereiten
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 6))

ax.set_xlim(-5, 5)
ax.set_ylim(-3, 4)
ax.set_aspect("equal")

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid()


# --------------------------------------------------
# Animationsfunktion
# --------------------------------------------------

def update(frame):

    ax.clear()

    ax.set_xlim(-5, 5)
    ax.set_ylim(-3, 4)
    ax.set_aspect("equal")
    ax.grid()

    # Fortschritt der Animation von 0 bis 1
    faktor = frame / 100

    # --------------------------------------------------
    # Seil zeichnen
    # --------------------------------------------------

    seil_laenge = 4

    linker_punkt = lampe + seil_laenge * links
    rechter_punkt = lampe + seil_laenge * rechts

    ax.plot(
        [linker_punkt[0], lampe[0], rechter_punkt[0]],
        [linker_punkt[1], lampe[1], rechter_punkt[1]],
        linewidth=3
    )

    # Lampe
    ax.scatter(0, 0, s=200)

    ax.text(
        0,
        -0.35,
        "Lampe",
        ha="center",
        fontsize=12
    )


    # --------------------------------------------------
    # Zugkräfte im Seil
    # --------------------------------------------------

    pfeil_laenge = 2.5 * faktor

    # linke Zugkraft
    ax.quiver(
        0,
        0,
        links[0] * pfeil_laenge,
        links[1] * pfeil_laenge,
        angles="xy",
        scale_units="xy",
        scale=1,
        width=0.012
    )

    # rechte Zugkraft
    ax.quiver(
        0,
        0,
        rechts[0] * pfeil_laenge,
        rechts[1] * pfeil_laenge,
        angles="xy",
        scale_units="xy",
        scale=1,
        width=0.012
    )


    # Beschriftungen
    ax.text(
        -2.2,
        1.15,
        "150 N",
        fontsize=14
    )

    ax.text(
        1.6,
        1.15,
        "150 N",
        fontsize=14
    )


    # --------------------------------------------------
    # Ab Hälfte der Animation:
    # Komponenten anzeigen
    # --------------------------------------------------

    if frame > 50:

        faktor2 = (frame - 50) / 50

        horizontal = 2.5 * np.cos(winkel) * faktor2
        vertikal = 2.5 * np.sin(winkel) * faktor2

        # horizontale Komponenten

        ax.quiver(
            0, 0,
            -horizontal, 0,
            angles="xy",
            scale_units="xy",
            scale=1,
            width=0.008
        )

        ax.quiver(
            0, 0,
            horizontal, 0,
            angles="xy",
            scale_units="xy",
            scale=1,
            width=0.008
        )

        # vertikale Komponenten

        ax.quiver(
            -0.1, 0,
            0, vertikal,
            angles="xy",
            scale_units="xy",
            scale=1,
            width=0.008
        )

        ax.quiver(
            0.1, 0,
            0, vertikal,
            angles="xy",
            scale_units="xy",
            scale=1,
            width=0.008
        )


        ax.text(
            0,
            2.8,
            "Horizontale Kräfte heben sich auf",
            ha="center",
            fontsize=13
        )

        ax.text(
            0,
            2.4,
            f"Vertikal: 2 · 150 · sin(20°) = {F_G:.1f} N",
            ha="center",
            fontsize=13
        )


    # --------------------------------------------------
    # Titel
    # --------------------------------------------------

    ax.set_title(
        "Warum jede Seilhälfte mit 150 N belastet wird",
        fontsize=15
    )


# --------------------------------------------------
# Animation starten
# --------------------------------------------------

animation = FuncAnimation(
    fig,
    update,
    frames=101,
    interval=50
)

plt.show()