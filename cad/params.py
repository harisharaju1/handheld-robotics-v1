"""Single source of truth for every dimension (mm).

Change a value here, re-run `python cad/build.py`, and every part and the
assembly regenerate. Values marked MEASURE should be checked with calipers
against your actual parts before the first print order.
"""

# --- Printer / fit tolerances (tune after printing the coupons) -------------
M3_CLEAR = 3.4          # through-hole for an M3 screw
M3_INSERT = 4.0         # bore for an M3 heat-set insert (MEASURE: insert OD - 0.2)
INSERT_DEPTH = 6.0
M3_NUT_FLATS = 5.7      # hex nut pocket across flats

# --- Chassis -----------------------------------------------------------------
DECK_D = 250.0          # deck diameter
DECK_T = 5.0            # 5 mm acrylic / ply, laser cut
STANDOFF_H = 60.0       # gap between decks
STANDOFF_D = 5.5        # M3 hex standoff, across corners ~ 6.4

# --- Drive -------------------------------------------------------------------
WHEEL_D = 65.0          # MEASURE
WHEEL_W = 26.0          # MEASURE
TRACK = 210.0           # wheel centre to wheel centre
MOTOR_D = 25.0          # 25GA-370 gearbox OD (MEASURE)
MOTOR_FIT = 0.3         # added to MOTOR_D for the clamp bore
MOTOR_LEN = 66.0        # gearbox + can + encoder, approx (MEASURE)
MOTOR_FACE_GAP = 4.0    # gearbox face to inner wheel face (shaft + hub)

AXLE_Z = WHEEL_D / 2                    # motor axis height above floor
CLAMP_DROP = 16.0                       # motor axis below lower-deck underside
LOWER_DECK_Z = AXLE_Z + CLAMP_DROP      # underside of lower deck
UPPER_DECK_Z = LOWER_DECK_Z + DECK_T + STANDOFF_H

MOTOR_FACE_Y = TRACK / 2 - WHEEL_W / 2 - MOTOR_FACE_GAP
CLAMP_W = 44.0          # across the motor
CLAMP_L = 20.0          # along the motor axis
CLAMP_BELOW = 18.0      # cap thickness below the axis
CLAMP_SQUEEZE = 0.4     # gap left between saddle and cap so the bolts pinch
CLAMP_BOLT_X = 17.5
CLAMP_Y = MOTOR_FACE_Y - 12.0           # clamp centred on the gearbox

WHEEL_SLOT_HALF_X = WHEEL_D / 2 + 4.0
WHEEL_SLOT_Y0 = TRACK / 2 - WHEEL_W / 2 - 4.0

# --- Casters -----------------------------------------------------------------
CASTER_H = 20.0         # MEASURE: caster mounting face to floor
CASTER_X = 80.0         # front (+) and rear (-)
CASTER_SLOT_X = 13.0    # slot centres either side of the caster centre
CASTER_SLOT_LEN = 9.4   # fits hole spacings ~ 2*(13 +/- 3) mm
CASTER_PRELOAD = 1.0    # casters sit this much short so wheels carry the load
CASTER_PAD = 40.0

# --- Lower-deck payload --------------------------------------------------------
BATTERY = (75.0, 60.0, 22.0)            # MEASURE your 3S pack (x, y, z)
BATT_TRAY_CENTER = (-50.0, 0.0)
EPLATE_SIZE = (95.0, 70.0)
EPLATE_CENTER = (55.0, 0.0)
EPLATE_STANDOFF = 6.0
GRID_PITCH = 10.0       # perfboard-style M3 grid on the electronics plate

# --- Upper-deck payload --------------------------------------------------------
MAST_CENTER = (-55.0, 0.0)
MAST_TUBE_D = 10.0      # aluminium tube or M8 rod -> set 8.0
MAST_LEN = 150.0
LIDAR_D = 56.0          # RPLIDAR C1 approx footprint (check Slamtec STEP)
LIDAR_H = 41.0
MODULE_CENTER = (60.0, 0.0)
MODULE_SIZE = 80.0
MODULE_INSERT_SQ = 25.0 # module bolts to the plate on this +/- square
MODULE_DECK_SQ = 35.0   # plate bolts to the deck on this +/- square
PI_BOX = (85.0, 56.0, 20.0)
PI_CENTER = (0.0, -70.0)

# --- Standoff layout (avoid wheel slots and caster pads) -------------------------
import math as _m
STANDOFF_PTS = [(100 * _m.cos(_m.radians(a)), 100 * _m.sin(_m.radians(a)))
                for a in (45, 135, 225, 315)] + [(110.0, 0.0), (-110.0, 0.0)]

PETG_DENSITY = 1.27     # g/cm3, for print-weight estimates
