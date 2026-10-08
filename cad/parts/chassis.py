"""Decks, motor clamp, caster spacer. Decks are laser-cut (DXF), not printed."""
import cadquery as cq
import params as P
from parts.common import box, vcyl, ycyl, drill, square_pts


def _rect_corners(size, center, inset=6.0):
    sx, sy = size
    cx, cy = center
    hx, hy = sx / 2 - inset, sy / 2 - inset
    return [(cx + a * hx, cy + b * hy) for a in (-1, 1) for b in (-1, 1)]


def clamp_deck_holes():
    """Deck holes for both motor clamps (left clamp at +Y, right rotated 180 deg)."""
    pts = []
    for x in (-P.CLAMP_BOLT_X, P.CLAMP_BOLT_X):
        pts.append((x, P.CLAMP_Y + 5.0))
        pts.append((x, -P.CLAMP_Y - 5.0))
    return pts


def deck(lower: bool):
    t = P.DECK_T
    d = cq.Workplane("XY").circle(P.DECK_D / 2).extrude(t)
    d = drill(d, P.STANDOFF_PTS, P.M3_CLEAR, -1, t + 2)
    if lower:
        # wheel slots, open to the rim
        for sign in (1, -1):
            slot_len = P.DECK_D / 2 - P.WHEEL_SLOT_Y0 + 5
            y0 = P.WHEEL_SLOT_Y0 if sign > 0 else -P.WHEEL_SLOT_Y0 - slot_len
            d = d.cut(cq.Workplane("XY")
                      .box(2 * P.WHEEL_SLOT_HALF_X, slot_len, t + 2, centered=(True, False, False))
                      .translate((0, y0, -1)))
        d = drill(d, clamp_deck_holes(), P.M3_CLEAR, -1, t + 2)
        # caster slots (through-bolted caster + spacer + deck)
        for cx in (P.CASTER_X, -P.CASTER_X):
            for sx in (-1, 1):
                d = d.cut(cq.Workplane("XY")
                          .slot2D(P.CASTER_SLOT_LEN, P.M3_CLEAR)
                          .extrude(t + 2)
                          .translate((cx + sx * P.CASTER_SLOT_X, 0, -1)))
        tray = (P.BATTERY[0] + 12, P.BATTERY[1] + 12)
        d = drill(d, _rect_corners(tray, P.BATT_TRAY_CENTER), P.M3_CLEAR, -1, t + 2)
        d = drill(d, _rect_corners(P.EPLATE_SIZE, P.EPLATE_CENTER), P.M3_CLEAR, -1, t + 2)
        # cable pass-through to the upper deck
        d = d.cut(cq.Workplane("XY").slot2D(40, 14).extrude(t + 2).translate((0, 0, -1)))
    else:
        mx, my = P.MAST_CENTER
        d = drill(d, [(mx + 19 * a, my + 19 * b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))],
                  P.M3_CLEAR, -1, t + 2)
        cx, cy = P.MODULE_CENTER
        d = drill(d, [(cx + x, cy + y) for x, y in square_pts(P.MODULE_DECK_SQ)],
                  P.M3_CLEAR, -1, t + 2)
        px, py = P.PI_CENTER
        # Raspberry Pi 5 hole pattern 58 x 49 mm
        d = drill(d, [(px + a * 29, py + b * 24.5) for a in (-1, 1) for b in (-1, 1)],
                  P.M3_CLEAR, -1, t + 2)
        d = d.cut(cq.Workplane("XY").slot2D(40, 14).extrude(t + 2).translate((0, 0, -1)))
    return d


def motor_clamp():
    """Two-piece split clamp. Mounting face (deck underside) at z = 0, motor axis along Y."""
    W, L, drop, below = P.CLAMP_W, P.CLAMP_L, P.CLAMP_DROP, P.CLAMP_BELOW
    bore = ycyl(P.MOTOR_D + P.MOTOR_FIT, L + 2, 0, -L / 2 - 1, -drop)
    saddle = box(W, L, drop, z0=-drop).cut(bore)
    cap_top = -drop - P.CLAMP_SQUEEZE
    cap = box(W, L, below - P.CLAMP_SQUEEZE, z0=-drop - below).cut(bore)
    xb = P.CLAMP_BOLT_X
    # deck screws: inserts from the top of the saddle
    saddle = drill(saddle, [(-xb, 5.0), (xb, 5.0)], P.M3_INSERT, -P.INSERT_DEPTH, P.INSERT_DEPTH + 1)
    # cap screws: clearance through the cap, inserts up into the saddle
    cap = drill(cap, [(-xb, -5.0), (xb, -5.0)], P.M3_CLEAR, -drop - below - 1, below + 2)
    saddle = drill(saddle, [(-xb, -5.0), (xb, -5.0)], P.M3_INSERT, -drop - 0.01, P.INSERT_DEPTH)
    # counterbore the cap screw heads
    cap = drill(cap, [(-xb, -5.0), (xb, -5.0)], 6.0, -drop - below - 1, 4.0)
    return saddle, cap


def caster_spacer():
    h = P.LOWER_DECK_Z - P.CASTER_H - P.CASTER_PRELOAD
    s = box(P.CASTER_PAD, P.CASTER_PAD * 0.8, h)
    for sx in (-1, 1):
        s = s.cut(cq.Workplane("XY").slot2D(P.CASTER_SLOT_LEN, P.M3_CLEAR)
                  .extrude(h + 2).translate((sx * P.CASTER_SLOT_X, 0, -1)))
    # lighten
    s = s.cut(box(10, P.CASTER_PAD * 0.8 - 8, h + 2, z0=-1))
    return s, h
