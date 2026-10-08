"""Printed mounts that sit on the decks."""
import cadquery as cq
import params as P
from parts.common import box, vcyl, drill, square_pts


def battery_tray():
    bx, by, bz = P.BATTERY
    wall, base = 2.4, 3.0
    ox, oy = bx + 2 * wall + 1.0, by + 2 * wall + 1.0
    t = box(ox, oy, base + 10)
    t = t.cut(box(bx + 1.0, by + 1.0, 20, z0=base))
    # open one short end for the balance lead / XT60
    t = t.cut(box(wall * 3, by - 16, 20, cx=-ox / 2, z0=base))
    # strap slots through the base, across the pack
    for sx in (-1, 1):
        t = t.cut(box(4, 22, base + 2, cx=sx * (bx / 2 - 12), cy=0, z0=-1))
    # deck screws, matching chassis._rect_corners(battery + 12)
    hx, hy = (bx + 12) / 2 - 6, (by + 12) / 2 - 6
    t = drill(t, [(a * hx, b * hy) for a in (-1, 1) for b in (-1, 1)], P.M3_CLEAR, -1, base + 2)
    return t


def electronics_plate():
    sx, sy = P.EPLATE_SIZE
    t = 3.0
    p = box(sx, sy, t)
    # perfboard-style M3 grid: zip-tie or screw any board on
    pts = []
    nx, ny = int((sx - 16) // P.GRID_PITCH), int((sy - 16) // P.GRID_PITCH)
    for i in range(nx + 1):
        for j in range(ny + 1):
            pts.append((-nx * P.GRID_PITCH / 2 + i * P.GRID_PITCH,
                        -ny * P.GRID_PITCH / 2 + j * P.GRID_PITCH))
    p = (p.faces(">Z").workplane().pushPoints(pts).hole(3.2))
    # corner deck bosses (6 mm tall, insert from below)
    hx, hy = sx / 2 - 6, sy / 2 - 6
    corners = [(a * hx, b * hy) for a in (-1, 1) for b in (-1, 1)]
    for (x, y) in corners:
        p = p.union(vcyl(9, P.EPLATE_STANDOFF, x, y, -P.EPLATE_STANDOFF))
    p = drill(p, corners, P.M3_INSERT, -P.EPLATE_STANDOFF - 0.01, P.INSERT_DEPTH)
    return p


def mast_base():
    d, t, boss_h = 50.0, 6.0, 25.0
    b = vcyl(d, t).union(vcyl(P.MAST_TUBE_D + 8, boss_h))
    b = b.cut(vcyl(P.MAST_TUBE_D + 0.2, boss_h, z0=2.0))
    # radial pinch screw into the boss
    b = b.cut(cq.Workplane("YZ").circle(P.M3_INSERT / 2).extrude(20).translate((0, 0, boss_h - 8)))
    # deck mounting, inserts from below
    pts = [(19, 0), (-19, 0), (0, 19), (0, -19)]
    b = drill(b, pts, P.M3_INSERT, -0.01, min(P.INSERT_DEPTH, t - 1.2))
    return b


def lidar_plate():
    d, t, boss_h = 64.0, 4.0, 16.0
    p = vcyl(d, t).union(vcyl(P.MAST_TUBE_D + 8, boss_h, z0=-boss_h + t))
    p = p.cut(vcyl(P.MAST_TUBE_D + 0.2, boss_h, z0=-boss_h + t - 2))
    # 4 radial slots so any lidar hole pattern from r = 14 to r = 28 fits
    for ang in (45, 135, 225, 315):
        p = p.cut(cq.Workplane("XY").slot2D(14, 2.9).extrude(t + 2)
                  .translate((21, 0, -1)).rotate((0, 0, 0), (0, 0, 1), ang))
    # cable notch
    p = p.cut(box(12, 10, t + 2, cx=-d / 2 + 4, z0=-1))
    return p


def module_plate():
    s, t = P.MODULE_SIZE, 8.0
    p = box(s, s, t)
    # deck screws (clearance + counterbore from the top)
    deck_pts = square_pts(P.MODULE_DECK_SQ)
    p = drill(p, deck_pts, P.M3_CLEAR, -1, t + 2)
    p = drill(p, deck_pts, 6.0, t - 3.0, 4.0)
    # module screws: inserts from the top
    p = drill(p, square_pts(P.MODULE_INSERT_SQ), P.M3_INSERT, t - P.INSERT_DEPTH + 0.01, P.INSERT_DEPTH)
    # wire pass-through
    p = p.cut(cq.Workplane("XY").slot2D(30, 10).extrude(t + 2).translate((0, 0, -1)))
    return p
