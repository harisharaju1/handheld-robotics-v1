import cadquery as cq


def box(x, y, z, cx=0.0, cy=0.0, z0=0.0):
    """Box with its base at z0, centred on (cx, cy)."""
    return (cq.Workplane("XY")
            .box(x, y, z, centered=(True, True, False))
            .translate((cx, cy, z0)))


def vcyl(d, h, x=0.0, y=0.0, z0=0.0):
    """Vertical cylinder (along +Z) starting at z0."""
    return cq.Workplane("XY").circle(d / 2).extrude(h).translate((x, y, z0))


def ycyl(d, length, x=0.0, y0=0.0, z=0.0):
    """Cylinder along +Y starting at y0."""
    return cq.Workplane("XY").add(
        cq.Solid.makeCylinder(d / 2, length, cq.Vector(x, y0, z), cq.Vector(0, 1, 0)))


def drill(part, pts, d, z0, h):
    for (x, y) in pts:
        part = part.cut(vcyl(d, h, x, y, z0))
    return part


def square_pts(half):
    return [(sx * half, sy * half) for sx in (-1, 1) for sy in (-1, 1)]
