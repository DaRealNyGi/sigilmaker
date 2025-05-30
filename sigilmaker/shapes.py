# sigilmaker/shapes.py
"""
Central registry for all built-in and plugin shapes.
Each function decorated with @register_shape automatically registers itself.
"""

import numpy as np
from math import pi, sin, cos, sqrt
import matplotlib.pyplot as plt

# The registry mapping name -> draw_function
SHAPES: dict[str, callable] = {}


def register_shape(name: str):
    """
    Decorator to register a shape drawing function under SHAPES[name].
    Usage:
        @register_shape("Seed-of-Life")
        def draw_seed(ax, **kwargs): ...
    """
    def decorator(func):
        SHAPES[name] = func
        return func
    return decorator


@register_shape("Seed-of-Life")
def draw_seed(ax, R=1):
    centers = [(0,0)] + [(cos(k*pi/3), sin(k*pi/3)) for k in range(6)]
    for x,y in centers:
        ax.add_patch(plt.Circle((x,y), R,
                                 fill=False,
                                 edgecolor="#FFD700",
                                 linewidth=1.5,
                                 alpha=0.3))

# Additional patterns below...
@register_shape("Flower-of-Life")
def draw_flower(ax, R=1):
    coords = [
        (q + r/2, r*(sqrt(3)/2))
        for q in range(-2,3)
        for r in range(-2,3)
        if abs(q+r) <= 2
    ]
    for x,y in coords:
        ax.add_patch(plt.Circle((x*R, y*R), R,
                                 fill=False,
                                 edgecolor="#FFD700",
                                 linewidth=1,
                                 alpha=0.2))

@register_shape("Vesica Piscis")
def draw_vesica(ax, R=1):
    for ox in (-R/2, R/2):
        ax.add_patch(plt.Circle((ox, 0), R,
                                 fill=False,
                                 edgecolor="#FFD700",
                                 linewidth=1.5,
                                 alpha=0.4))

# ... define other shapes similarly ...
