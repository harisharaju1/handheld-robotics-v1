"""Decks, motor adapter, caster spacer. Decks are laser-cut (DXF), not printed.

Frame: +X forward, +Y left, Z up from the floor. Left motor at +Y; the right
motor uses the same parts rotated 180 deg about Z.
"""
import cadquery as cq
import params as P
from parts.common import box, vcyl, drill


def _rect_corners(size, center, inset=6.0):
    sx, sy = size
    cx, cy = center
    hx, hy = sx / 2 - inset, sy / 2 - inset
    return [(cx + a * hx, cy + b * hy) for a in (-1, 1) for b in (-1, 1)]


def adapter_deck_holes():
    """Deck holes for both motor adapters (left at +Y, right rotated 180 deg)."""
    pts = []
    for (x, y) in P.ADAPTER_DECK_HOLES:
        pts.append((x, P.FOOT_CY + y))
        pts.append((-x, -(P.FOOT_CY + y)))
    return pts


def foot_mark_holes():
    """Locating holes just outside each bracket-foot corner (both motors)."""
    hx = P.BRACKET_FOOT[0] / 2 + P.FOOT_MARK_GAP
    hy = P.BRACKET_FOOT[1] / 2 + P.FOOT_MARK_GAP
    pts = []
    for sign in (1, -1):
        for a in (-1, 1):
            for b in (-1, 1):
                pts.append((a * hx, sign * (P.FOOT_CY + b * hy)))
    return pts


def caster_deck_holes():
    return [(cx, sy * P.CASTER_PITCH / 2) for cx in (P.CASTER_X, -P.CASTER_X) for sy in (-1, 1)]


def tray_deck_holes():
    bx, by = P.BATT_TRAY_CENTER
    return [(bx + x, by + y) for (x, y) in P.TRAY_HOLES]


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
        if P.ADAPTER_T > 0:
            d = drill(d, adapter_deck_holes(), P.M3_CLEAR, -1, t + 2)
        else:
            d = drill(d, foot_mark_holes(), P.FOOT_MARK_D, -1, t + 2)
        d = drill(d, caster_deck_holes(), P.M3_CLEAR, -1, t + 2)
        d = drill(d, tray_deck_holes(), P.M3_CLEAR, -1, t + 2)
        d = drill(d, _rect_corners(P.EPLATE_SIZE, P.EPLATE_CENTER), P.M3_CLEAR, -1, t + 2)
        # cable pass-through to the upper deck
        d = d.cut(cq.Workplane("XY").slot2D(40, 14).extrude(t + 2).translate((0, 0, -1)))
    else:
        mx, my = P.MAST_CENTER
        d = drill(d, [(mx + 19 * a, my + 19 * b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))],
                  P.M3_CLEAR, -1, t + 2)
        cx, cy = P.MODULE_CENTER
        d = drill(d, [(cx + sx * P.MODULE_DECK_SQ, cy + sy * P.MODULE_DECK_SQ)
                      for sx in (-1, 1) for sy in (-1, 1)], P.M3_CLEAR, -1, t + 2)
        px, py = P.PI_CENTER
        # Raspberry Pi 5 hole pattern 58 x 49 mm
        d = drill(d, [(px + a * 29, py + b * 24.5) for a in (-1, 1) for b in (-1, 1)],
                  P.M3_CLEAR, -1, t + 2)
        d = d.cut(cq.Workplane("XY").slot2D(40, 14).extrude(t + 2).translate((0, 0, -1)))
    return d


def motor_adapter():
    """Plate between the JGB37-520 L-bracket foot and the deck underside.

    Local frame: centred on the bracket foot, z = 0 is the face the bracket
    bolts to, z = ADAPTER_T is the face against the deck. +y = wheel side.
    Bracket: M3 screws up through the foot into captive nuts (slotted across
    the motor to absorb measurement error). Deck: M3 down through the deck into
    heat-set inserts.
    """
    T = P.ADAPTER_T
    ax, ay = P.ADAPTER_SIZE
    p = box(ax, ay, T)
    slot_len = P.M3_CLEAR + 2 * P.BRACKET_SLOT
    pocket_w = P.M3_NUT_FLATS + 0.3          # nut can slide along the slot but not spin
    pocket_len = 6.4 + 2 * P.BRACKET_SLOT + 0.4
    for (x, y) in P.BRACKET_HOLES:
        p = p.cut(cq.Workplane("XY").slot2D(slot_len, P.M3_CLEAR)
                  .extrude(T + 2).translate((x, y, -1)))
        p = p.cut(box(pocket_len, pocket_w, P.NUT_DEPTH + 1, cx=x, cy=y, z0=T - P.NUT_DEPTH))
    depth = min(P.INSERT_DEPTH, T - 1.0)
    p = drill(p, P.ADAPTER_DECK_HOLES, P.M3_INSERT, T - depth, depth + 1)
    return p


def caster_spacer():
    """Block between deck underside (top, z = h) and caster flange (bottom, z = 0).
    Heat-set inserts at both ends: M3x10 down through the deck, M3x8 up through the caster."""
    h = P.LOWER_DECK_Z - P.CASTER_H - P.CASTER_PRELOAD
    sx, sy = P.CASTER_SPACER
    s = box(sx, sy, h)
    pts = [(0.0, -P.CASTER_PITCH / 2), (0.0, P.CASTER_PITCH / 2)]
    s = drill(s, pts, P.M3_CLEAR, -1, h + 2)
    s = drill(s, pts, P.M3_INSERT, -0.01, P.INSERT_DEPTH)
    s = drill(s, pts, P.M3_INSERT, h - P.INSERT_DEPTH, P.INSERT_DEPTH + 1)
    # lighten: open core between the two screw columns
    s = s.cut(box(sx - 14.0, P.CASTER_PITCH - 14.0, h + 2, z0=-1))
    return s, h
