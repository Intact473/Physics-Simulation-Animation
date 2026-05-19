"""
NV-Zentrum: Animation zu NV-Achsen, Magnetfeld-Projektion und ESR-Dips

Es werden zwei Fälle animiert:
1) Magnetfeld schräg zu allen NV-Achsen  -> viele verschiedene Projektionen -> bis zu 8 Dips
2) Magnetfeld parallel zu einer NV-Achse -> 1 Achse speziell, 3 Achsen gleich -> 4 sichtbare Dips

Die Atome sind stark vereinfacht gezeichnet:
- graue Punkte: Kohlenstoffatome im Diamantgitter
- blauer Punkt: Stickstoffatom N
- leere Stelle: Vacancy V, also fehlendes Kohlenstoffatom
- gestrichelte Linien: die vier möglichen NV-Achsen
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

D = 2.87          # GHz, Nullfeldaufspaltung
gamma = 0.028    # GHz/mT, ungefähr 28 GHz/T
B0 = 25.0        # mT, künstlich deutlich gewählt

# Vier mögliche NV-Achsen im Diamant: <111>-Richtungen
nv_axes = np.array([
    [ 1,  1,  1],
    [ 1, -1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
], dtype=float)

nv_axes = nv_axes / np.linalg.norm(nv_axes, axis=1)[:, None]

# Zwei Magnetfeldrichtungen
B_parallel = nv_axes[0]
B_tilted = np.array([0.25, 0.65, 1.0])
B_tilted = B_tilted / np.linalg.norm(B_tilted)

cases = [
    ("B schräg zu allen NV-Achsen", B_tilted),
    ("B parallel zu einer NV-Achse", B_parallel),
]


def resonance_frequencies(B_dir):
    """
    Für jede NV-Achse berechnen wir:
        B_parallel = B0 * cos(theta)

    Dann entstehen zwei Übergänge:
        f_minus = D - gamma * B_parallel
        f_plus  = D + gamma * B_parallel
    """
    freqs = []
    projections = []

    for axis in nv_axes:
        B_proj = B0 * np.dot(axis, B_dir)
        projections.append(B_proj)

        freqs.append(D - gamma * B_proj)
        freqs.append(D + gamma * B_proj)

    return np.array(freqs), np.array(projections)


def spectrum(freq_axis, resonances, width=0.025):
    """
    Künstliches ESR-Spektrum:
    Jede Resonanz erzeugt einen Dip.
    Wenn mehrere Resonanzen übereinanderliegen,
    wird der Dip tiefer.
    """
    y = np.ones_like(freq_axis)

    for f in resonances:
        y -= 0.12 * np.exp(-0.5 * ((freq_axis - f) / width) ** 2)

    return y


fig = plt.figure(figsize=(13, 7))
ax3d = fig.add_subplot(121, projection="3d")
ax_spec = fig.add_subplot(122)

fig.suptitle(
    "NV-Zentrum: Magnetfeld-Projektion und ESR-Dips",
    fontsize=14
)

freq_axis = np.linspace(1.7, 4.1, 900)

# Vereinfachte Diamant-Umgebung
carbon_positions = np.array([
    [ 1,  1,  1],
    [ 1, -1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
    [ 1,  0,  0],
    [-1,  0,  0],
    [ 0,  1,  0],
    [ 0, -1,  0],
    [ 0,  0,  1],
    [ 0,  0, -1],
], dtype=float)

N_pos = np.array([0.0, 0.0, 0.0])
V_pos = 1.25 * nv_axes[0]  # Vacancy liegt entlang einer NV-Achse neben N


def draw_scene(frame):
    ax3d.clear()
    ax_spec.clear()

    # Fall wechseln
    case_index = 0 if frame < 160 else 1
    local_frame = frame if frame < 160 else frame - 160

    title, B_dir = cases[case_index]

    # 3D-Ansicht langsam drehen
    ax3d.view_init(elev=23, azim=35 + 0.35 * frame)

    # Kohlenstoffatome
    ax3d.scatter(
        carbon_positions[:, 0],
        carbon_positions[:, 1],
        carbon_positions[:, 2],
        s=70,
        alpha=0.85,
        label="C-Atome"
    )

    # Stickstoffatom
    ax3d.scatter(
        [N_pos[0]], [N_pos[1]], [N_pos[2]],
        s=160,
        marker="o",
        label="N-Atom"
    )

    # Fehlstelle / Vacancy
    ax3d.scatter(
        [V_pos[0]], [V_pos[1]], [V_pos[2]],
        s=190,
        marker="x",
        linewidths=3,
        label="Vacancy V"
    )

    # N-V-Verbindung andeuten
    ax3d.plot(
        [N_pos[0], V_pos[0]],
        [N_pos[1], V_pos[1]],
        [N_pos[2], V_pos[2]],
        linestyle=":",
        linewidth=2
    )

    # NV-Achsen
    for i, axis in enumerate(nv_axes):
        start = -1.45 * axis
        end = 1.65 * axis

        ax3d.plot(
            [start[0], end[0]],
            [start[1], end[1]],
            [start[2], end[2]],
            linestyle="--",
            linewidth=2
        )

        ax3d.text(
            *(1.8 * axis),
            f"NV {i + 1}",
            fontsize=9
        )

    # Magnetfeldpfeil B0
    B_start = np.array([-1.6, -1.6, -1.4])
    B_vec = 2.0 * B_dir

    ax3d.quiver(
        B_start[0], B_start[1], B_start[2],
        B_vec[0], B_vec[1], B_vec[2],
        length=1.0,
        normalize=False,
        linewidth=3
    )

    ax3d.text(
        *(B_start + 1.1 * B_vec),
        "B₀",
        fontsize=13
    )

    # Projektionen des Magnetfelds auf die NV-Achsen
    _, projections = resonance_frequencies(B_dir)

    for axis in nv_axes:
        proj_len = np.dot(B_dir, axis)
        proj_vec = proj_len * axis

        ax3d.quiver(
            0, 0, 0,
            proj_vec[0], proj_vec[1], proj_vec[2],
            length=1.15,
            normalize=False,
            linestyle="dashed",
            alpha=0.6
        )

    ax3d.set_title(
        title + "\nGestrichelt: NV-Achsen und Magnetfeld-Projektionen"
    )

    ax3d.set_xlim(-2, 2)
    ax3d.set_ylim(-2, 2)
    ax3d.set_zlim(-2, 2)

    ax3d.set_xlabel("x")
    ax3d.set_ylabel("y")
    ax3d.set_zlabel("z")

    ax3d.legend(loc="upper left", fontsize=8)

    # ESR-Spektrum
    freqs, projections = resonance_frequencies(B_dir)
    y = spectrum(freq_axis, freqs)

    # Frequenzscan
    scan_fraction = min(local_frame / 145, 1.0)
    scan_freq = freq_axis[0] + scan_fraction * (freq_axis[-1] - freq_axis[0])

    ax_spec.plot(freq_axis, y, linewidth=2)
    ax_spec.axvline(scan_freq, linestyle="--", linewidth=2)

    ax_spec.set_xlim(freq_axis[0], freq_axis[-1])
    ax_spec.set_ylim(0.45, 1.05)

    ax_spec.set_xlabel("Mikrowellenfrequenz f_M in GHz")
    ax_spec.set_ylabel("Fluoreszenz / Kontrast")
    ax_spec.set_title("ESR-Spektrum: Dip, wenn f_M = f_res")

    # Resonanzstellen markieren
    for f in freqs:
        ax_spec.axvline(f, linestyle=":", alpha=0.35)

    # Aktuellen Resonanztreffer anzeigen
    close = np.abs(freqs - scan_freq) < 0.018

    if np.any(close):
        for f in freqs[close]:
            ax_spec.annotate(
                "Resonanz!\nf_M = f_res",
                xy=(f, spectrum(np.array([f]), [f])[0]),
                xytext=(f, 0.55),
                arrowprops=dict(arrowstyle="->"),
                ha="center",
                fontsize=9
            )

    # Erklärungstext
    text = (
        f"{title}\n\n"
        f"B₀ ist vorhanden: B₀ = {B0:.0f} mT\n"
        f"Für jede NV-Achse zählt nur:\n"
        f"B_parallel = B₀ cos(θ)\n\n"
        f"Übergänge pro Achse:\n"
        f"m_s = 0 → m_s = +1\n"
        f"m_s = 0 → m_s = -1\n\n"
        f"Wenn mehrere f_res gleich sind,\n"
        f"liegen Dips übereinander."
    )

    ax_spec.text(
        0.02, 0.04,
        text,
        transform=ax_spec.transAxes,
        fontsize=9,
        va="bottom",
        bbox=dict(boxstyle="round", alpha=0.15)
    )

    # Projektionen anzeigen
    proj_text = "B_parallel je NV-Achse [mT]:\n"

    for i, p in enumerate(projections):
        proj_text += f"NV {i + 1}: {p:+.1f}\n"

    ax_spec.text(
        0.58, 0.04,
        proj_text,
        transform=ax_spec.transAxes,
        fontsize=9,
        va="bottom",
        bbox=dict(boxstyle="round", alpha=0.15)
    )


ani = FuncAnimation(
    fig,
    draw_scene,
    frames=320,
    interval=55,
    repeat=True
)

plt.tight_layout()
plt.show()