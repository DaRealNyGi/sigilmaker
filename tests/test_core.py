import pytest
import numpy as np
from sigilmaker.core import get_symbols, compute_common, blend


def test_get_symbols_only_consonants_and_digits():
    phrase = "Hello World 123! AEIOU"
    symbols = get_symbols(phrase)
    # Expected: H, L, L, W, R, L, D, 1,2,3
    assert symbols == ['H','L','L','W','R','L','D','1','2','3']


def test_compute_common_regular_polygon_and_star_path():
    # Test n=5 yields 5 vertices and a star pentagon
    verts, path = compute_common(5, radius=1)
    assert len(verts) == 5
    # Vertices on unit circle approx
    for x,y in verts:
        r = np.hypot(x,y)
        assert pytest.approx(1, rel=1e-6) == r
    # Path should contain 6 points (start repeated)
    assert len(path) == 6
    # Path should start and end at same index
    assert path[0] == path[-1]
    # All indices in path are valid
    for idx in path:
        assert 0 <= idx < 5


def test_blend_midpoint_of_colors():
    c1 = (1.0, 0.0, 0.0, 1.0)  # Red opaque
    c2 = (0.0, 0.0, 1.0, 0.5)  # Blue semi-transparent
    mid = blend(c1, c2)
    # Expected midpoint: (0.5,0,0.5,0.75)
    assert mid == pytest.approx((0.5, 0.0, 0.5, 0.75))


if __name__ == "__main__":
    pytest.main([__file__])
