# sigilmaker/core.py
"""
Core geometry and drawing functions for SigilMaker.
This module is UI-agnostic and can be used by CLI, GUI, or API layers.
"""
import numpy as np
from math import gcd, pi, sin, cos, sqrt
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

# Constants
VOWELS = set("AEIOU")

# Utility functions
def get_symbols(phrase: str) -> list[str]:
    """Extract uppercase consonants (minus vowels) and digits from phrase."""
    return [c for c in phrase.upper() if (c.isalpha() and c not in VOWELS) or c.isdigit()]

def compute_common(n: int, radius: float = 1.5) -> tuple[list[tuple[float,float]], list[int]]:
    """
    Compute evenly spaced vertex coordinates on a circle and a star-polygon path.
    Returns (verts, path).
    """
    angles = [pi/2 - i * 2 * pi / n for i in range(n)]
    verts = [(radius * cos(a), radius * sin(a)) for a in angles]
    # find smallest step coprime with n
    step = next((k for k in range(n//2, 1, -1) if gcd(n, k) == 1), 1)
    path = []
    idx = 0
    while idx not in path:
        path.append(idx)
        idx = (idx + step) % n
    path.append(path[0])
    return verts, path

def blend(c1: tuple, c2: tuple) -> tuple:
    """Blend two RGBA colors to their midpoint."""
    return tuple((a + b) / 2 for a, b in zip(c1, c2))

def save_or_show(fig: plt.Figure, out_path: str | None, fmt: str, meta: dict) -> None:
    """Save figure to disk if out_path given, otherwise display interactively."""
    if out_path:
        fig.savefig(out_path, dpi=300, format=fmt, metadata=meta)
        plt.close(fig)
    else:
        plt.show()

def draw_sigil(
    symbols: list[str],
    shapes: dict[str, callable],
    patterns: list[str],
    radial: bool,
    out_path: str | None = None,
    fmt: str = 'png',
    palette: dict[str, tuple] | None = None
) -> None:
    """
    Draws a sigil: overlays patterns, connects symbols via star-polygon,
    and labels symbols. Delegates save/show to save_or_show().
    """
    n = len(symbols)
    verts, path = compute_common(n)
    # default palette: hsv for letters, tab10 for digits
    from . import letter_palette, number_palette
    palette_map = palette or {**letter_palette, **number_palette}
    colors = [palette_map[s] for s in symbols]
    rgba = [to_rgba(c) for c in colors]

    fig, ax = plt.subplots(figsize=(6, 6), facecolor='black')
    ax.axis('off'); ax.set_facecolor('black')

    # draw patterns
    for pat in patterns:
        if pat in shapes:
            shapes[pat](ax)

    # draw connecting star-polygon edges
    for i1, i2 in zip(path, path[1:]):
        x1, y1 = verts[i1]; x2, y2 = verts[i2]
        ax.plot([x1, x2], [y1, y2], color=blend(rgba[i1], rgba[i2]), linewidth=2)

    # outer boundary
    ax.add_patch(plt.Circle((0, 0), 1.5, fill=False, edgecolor='#FFD700', linewidth=2))

    # label symbols
    for (x, y), s, c in zip(verts, symbols, colors):
        rot = (np.degrees(np.arctan2(y, x)) - 90) if radial else 0
        ax.text(x, y, s, fontsize=30, fontweight='bold', color=c,
                rotation=rot, ha='center', va='center')

    ax.set_aspect('equal')
    ax.set_xlim(-2, 2); ax.set_ylim(-2, 2)
    save_or_show(fig, out_path, fmt, {'Mantra': ' '.join(symbols)})
