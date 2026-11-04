"""Build every part + the base assembly.

    source ~/venvs/cad/bin/activate
    python cad/build.py            # all parts
    python cad/build.py coupon     # only parts whose name contains 'coupon'

Outputs: exports/step/*.step (Onshape import), exports/stl/*.stl (print
service), exports/dxf/*.dxf (laser-cut decks), exports/manifest.md.
"""
import sys
import pathlib
import traceback

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cadquery as cq  # noqa: E402
import params as P  # noqa: E402
from parts import chassis, payload, coupons  # noqa: E402
from parts.common import box, vcyl, ycyl  # noqa: E402

ROOT = HERE.parent
OUT = ROOT / "exports"
for sub in ("step", "stl", "dxf"):
    (OUT / sub).mkdir(parents=True, exist_ok=True)


def parts():
    spacer, _ = chassis.caster_spacer()
    # name: (workplane, qty, printed?)
    d = {
        "00_coupon_holes": (coupons.holes_coupon(), 1, True),
        "00_coupon_bores": (coupons.bores_coupon(), 1, True),
        "10_deck_lower": (chassis.deck(lower=True), 1, False),
        "11_deck_upper": (chassis.deck(lower=False), 1, False),
        "22_caster_spacer": (spacer, 2, True),
        "30_battery_tray": (payload.battery_tray(), 1, True),
        "31_electronics_plate": (payload.electronics_plate(), 1, True),
        "40_mast_base": (payload.mast_base(), 1, True),
        "41_lidar_plate": (payload.lidar_plate(), 1, True),
        "50_module_plate": (payload.module_plate(), 1, True),
    }
    if P.ADAPTER_T > 0:
        d["20_motor_adapter"] = (chassis.motor_adapter(), 2, True)
    return d


def color(r, g, b):
    return cq.Color(r, g, b, 1.0)


def assembly(built):
    a = cq.Assembly(name="base_v1")
    L = cq.Location
    V = cq.Vector
    deck_c, print_c, dark, metal = color(.86, .83, .76), color(.89, .42, .17), color(.15, .16, .18), color(.72, .74, .77)
    zl, zu, t = P.LOWER_DECK_Z, P.UPPER_DECK_Z, P.DECK_T
    a.add(built["10_deck_lower"], name="deck_lower", loc=L(V(0, 0, zl)), color=deck_c)
    a.add(built["11_deck_upper"], name="deck_upper", loc=L(V(0, 0, zu)), color=deck_c)
    for i, (x, y) in enumerate(P.STANDOFF_PTS):
        a.add(vcyl(P.STANDOFF_D, P.STANDOFF_H), name=f"standoff_{i}", loc=L(V(x, y, zl + t)), color=metal)
    for side, sign in (("left", 1), ("right", -1)):
        rot = 0 if sign > 0 else 180
        if "20_motor_adapter" in built:
            a.add(built["20_motor_adapter"], name=f"motor_adapter_{side}",
                  loc=L(V(0, sign * P.FOOT_CY, zl - P.ADAPTER_T), V(0, 0, 1), rot), color=print_c)
        fx, fy = P.BRACKET_FOOT
        a.add(box(fx, fy, 2.5, cy=sign * P.FOOT_CY, z0=zl - P.ADAPTER_T - 2.5),
              name=f"bracket_foot_{side}", color=dark)
        m_len = fy + P.ENCODER_PAST_FOOT
        y_motor0 = P.FOOT_OUTER_Y - m_len if sign > 0 else -P.FOOT_OUTER_Y
        a.add(ycyl(P.MOTOR_D, m_len, 0, y_motor0, P.AXLE_Z - P.MOTOR_OFFSET),
              name=f"motor_{side}", color=metal)
        y_shaft0 = P.FOOT_OUTER_Y if sign > 0 else -P.FOOT_OUTER_Y - P.FOOT_TO_WHEEL
        a.add(ycyl(9.0, P.FOOT_TO_WHEEL, 0, y_shaft0, P.AXLE_Z), name=f"hub_{side}",
              color=color(.80, .65, .25))
        y_wheel0 = P.TRACK / 2 - P.WHEEL_W / 2 if sign > 0 else -P.TRACK / 2 - P.WHEEL_W / 2
        a.add(ycyl(P.WHEEL_D, P.WHEEL_W, 0, y_wheel0, P.AXLE_Z), name=f"wheel_{side}", color=dark)
    sp_h = P.LOWER_DECK_Z - P.CASTER_H - P.CASTER_PRELOAD
    for name, x in (("front", P.CASTER_X), ("rear", -P.CASTER_X)):
        a.add(built["22_caster_spacer"], name=f"caster_spacer_{name}", loc=L(V(x, 0, zl - sp_h)), color=print_c)
        a.add(vcyl(28, P.CASTER_H), name=f"caster_{name}", loc=L(V(x, 0, P.CASTER_PRELOAD)), color=metal)
    bx, by = P.BATT_TRAY_CENTER  # noqa
    a.add(built["30_battery_tray"], name="battery_tray", loc=L(V(bx, by, zl + t)), color=print_c)
    a.add(box(*P.BATTERY), name="battery_3s", loc=L(V(bx, by, zl + t + 3.0)), color=color(.23, .43, .65))
    ex, ey = P.EPLATE_CENTER
    a.add(built["31_electronics_plate"], name="electronics_plate",
          loc=L(V(ex, ey, zl + t + P.EPLATE_STANDOFF)), color=print_c)
    top = zu + t
    mx, my = P.MAST_CENTER
    a.add(built["40_mast_base"], name="mast_base", loc=L(V(mx, my, top)), color=print_c)
    a.add(vcyl(P.MAST_TUBE_D, P.MAST_LEN), name="mast_tube", loc=L(V(mx, my, top + 2.0)), color=metal)
    plate_z = top + 2.0 + P.MAST_LEN - 2.0
    a.add(built["41_lidar_plate"], name="lidar_plate", loc=L(V(mx, my, plate_z)), color=print_c)
    a.add(vcyl(P.LIDAR_D, P.LIDAR_H), name="rplidar_c1", loc=L(V(mx, my, plate_z + 4.0)), color=dark)
    cx, cy = P.MODULE_CENTER
    a.add(built["50_module_plate"], name="module_plate", loc=L(V(cx, cy, top)), color=print_c)
    px, py = P.PI_CENTER
    a.add(box(*P.PI_BOX), name="raspberry_pi_5", loc=L(V(px, py, top + 6.0)), color=color(.18, .49, .31))
    return a


def main():
    filt = sys.argv[1] if len(sys.argv) > 1 else ""
    built, rows, failed = {}, [], []
    for name, fn_result in parts().items():
        if filt and filt not in name:
            continue
        wp, qty, printed = fn_result
        try:
            cq.exporters.export(wp, str(OUT / "step" / f"{name}.step"))
            cq.exporters.export(wp, str(OUT / "stl" / f"{name}.stl"),
                                tolerance=0.02, angularTolerance=0.1)
            if name.startswith("1") and "deck" in name:
                cq.exporters.export(wp.faces("<Z"), str(OUT / "dxf" / f"{name}.dxf"))
            vol = wp.val().Volume() / 1000.0  # cm3
            grams = vol * P.PETG_DENSITY
            bb = wp.val().BoundingBox()
            rows.append((name, qty, printed, grams, (bb.xlen, bb.ylen, bb.zlen)))
            built[name] = wp
            print(f"ok   {name:28s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f} mm  {grams:6.1f} g solid")
        except Exception:
            failed.append(name)
            print(f"FAIL {name}")
            traceback.print_exc()

    print(f"info lower deck underside {P.LOWER_DECK_Z:.2f} mm, upper deck {P.UPPER_DECK_Z:.2f} mm, "
          f"caster spacer {P.LOWER_DECK_Z - P.CASTER_H - P.CASTER_PRELOAD:.2f} mm, "
          f"ground clearance under motors {P.GROUND_CLEARANCE:.2f} mm")
    if not filt and not failed:
        try:
            a = assembly(built)
            path = str(OUT / "step" / "99_base_assembly.step")
            try:
                a.export(path)
            except AttributeError:
                a.save(path)
            print("ok   99_base_assembly.step")
        except Exception:
            failed.append("assembly")
            traceback.print_exc()

    lines = ["# Export manifest", "",
             "| Part | Qty | Made by | Bounding box (mm) | Solid PETG (g, each) |",
             "| --- | --- | --- | --- | --- |"]
    total = 0.0
    for name, qty, printed, g, (x, y, z) in rows:
        how = "3D print (PETG)" if printed else "laser cut 5 mm (DXF)"
        lines.append(f"| {name} | {qty} | {how} | {x:.1f} x {y:.1f} x {z:.1f} | {g:.0f} |")
        if printed:
            total += g * qty
    lines += ["", f"Printed total if solid: {total:.0f} g. At 40% infill / 3 walls expect roughly "
              f"{total * 0.55:.0f} g.", ""]
    (OUT / "manifest.md").write_text("\n".join(lines))
    print("\n".join(lines))
    if failed:
        print("FAILED:", failed)
        sys.exit(1)


if __name__ == "__main__":
    main()
