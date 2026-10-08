"""Print these FIRST. Measure, update params.py, regenerate everything."""
import cadquery as cq
import params as P
from parts.common import box, vcyl, drill


def holes_coupon():
    """Row 1: M3 clearance 3.0-3.7. Row 2: insert bores 3.7-4.4 (6 mm deep).
    Row 3: 4 mm D-shaft bores 3.9-4.3 with flat at 3.5 mm. Read left -> right;
    the notch marks the smallest size."""
    c = box(100, 42, 6)
    steps = [i * 0.1 for i in range(8)]
    xs = [-42 + i * 12 for i in range(8)]
    for x, s in zip(xs, steps):
        c = c.cut(vcyl(3.0 + s, 8, x, 13, -1))
        c = c.cut(vcyl(3.7 + s, P.INSERT_DEPTH, x, 0, 6 - P.INSERT_DEPTH + 0.01))
    for x, s in zip(xs[:5], steps[:5]):
        d = 3.9 + s
        shaft = vcyl(d, 8, x, -13, -1).cut(box(d, d, 10, cx=x, cy=-13 + 1.5 + d / 2, z0=-2))
        c = c.cut(shaft)
    c = c.cut(box(4, 4, 8, cx=-50, cy=13, z0=-1))  # orientation notch
    return c


def bores_coupon():
    """Motor-clamp bore test: 24.9 / 25.1 / 25.3 / 25.5 mm rings, 8 mm tall."""
    c = None
    for i, d in enumerate((24.9, 25.1, 25.3, 25.5)):
        ring = vcyl(d + 6, 8, x=i * 33.0).cut(vcyl(d, 10, x=i * 33.0, z0=-1))
        ring = ring.union(box(4, 3, 8, cx=i * 33.0, cy=-(d + 6) / 2 - 1.0))
        for k in range(i + 1):  # 1-4 tick marks = size index
            ring = ring.cut(box(1.2, 2, 2, cx=i * 33.0 - 3 + 2 * k, cy=-(d + 6) / 2 - 1.5, z0=6.5))
        c = ring if c is None else c.union(ring)
    return c
