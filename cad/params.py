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

# --- Drive: JGB37-520 333 RPM + L-bracket + 68.5 mm wheel (measured Nov 3) ---
WHEEL_D = 68.5          # measured 68-69
WHEEL_W = 27.5          # measured 27-28
TRACK = 220.0           # wheel centre to wheel centre
AXLE_Z = WHEEL_D / 2    # motor shaft height above floor

# L-bracket foot screws (via the printed adapter) to the deck underside; the
# motor hangs below it. All measured from the foot's flat mounting face.
BRACKET_FOOT = (40.0, 42.0)   # (across the motor = X, along the motor = Y)
BRACKET_AXLE_DROP = 30.5      # mounting face to shaft centre
MOTOR_D = 37.0
MOTOR_OFFSET = 7.0            # body centre sits this much further from the foot than the shaft
MOTOR_BODY_DROP = 56.0        # mounting face to farthest point of the motor body
FOOT_TO_WHEEL = 14.0          # foot's wheel-side edge to the wheel's inner face
ENCODER_PAST_FOOT = 15.0      # encoder board sticks out past the foot's inner edge
CONNECTOR_ALLOW = 15.0        # encoder connector + wire bend

# Printed adapter between bracket and deck. If the bracket hole pattern is off,
# only this small part is reprinted; the laser-cut deck stays valid.
# Direct mount (Nov 4): the bracket foot bolts straight to the deck underside.
# Its 4 holes are hand-drilled using the bracket itself as the template; the
# deck carries 2 mm locating holes just outside each foot corner instead.
ADAPTER_T = 0.0               # 0 = no printed adapter (set 6.0 to bring it back)
FOOT_MARK_D = 2.0             # locating-hole diameter
FOOT_MARK_GAP = 1.5           # locating holes sit this far outside the foot's corners
ADAPTER_SIZE = (BRACKET_FOOT[0] + 14.0, BRACKET_FOOT[1] + 14.0)
# MEASURE (trace the foot on paper): bracket holes relative to the foot centre,
# (x across, y along the motor; +y = wheel side). Estimated from photos.
BRACKET_HOLES = [(-12.0, 15.0), (12.0, 15.0), (-9.5, -15.0), (9.5, -15.0)]
BRACKET_SLOT = 2.0            # holes are slotted +/- this much across the motor
ADAPTER_DECK_HOLES = [(sx * 22.0, sy * 23.0) for sx in (-1, 1) for sy in (-1, 1)]
NUT_DEPTH = 2.6               # M3 nut pocket depth on the adapter's top face

LOWER_DECK_Z = AXLE_Z + BRACKET_AXLE_DROP + ADAPTER_T   # underside of lower deck
UPPER_DECK_Z = LOWER_DECK_Z + DECK_T + STANDOFF_H
GROUND_CLEARANCE = AXLE_Z + BRACKET_AXLE_DROP - MOTOR_BODY_DROP   # under the motors

FOOT_OUTER_Y = TRACK / 2 - WHEEL_W / 2 - FOOT_TO_WHEEL   # left side; right is mirrored
FOOT_CY = FOOT_OUTER_Y - BRACKET_FOOT[1] / 2

WHEEL_SLOT_HALF_X = WHEEL_D / 2 + 4.0
WHEEL_SLOT_Y0 = TRACK / 2 - WHEEL_W / 2 - 4.0

# --- Casters: 5/8" ball caster, 49 x 32 flange, 21 mm tall, 38 mm hole pitch --
CASTER_H = 21.0         # flange mounting face to floor
CASTER_FLANGE = (32.0, 49.0)  # (X, Y): flange long axis runs left-right
CASTER_PITCH = 38.0     # hole centres, along Y
CASTER_X = 80.0         # front (+) and rear (-)
CASTER_PRELOAD = 1.0    # casters sit this much high so the wheels always grip
CASTER_SPACER = (36.0, 54.0)

# --- Lower-deck payload --------------------------------------------------------
BATTERY = (70.0, 64.5, 44.5)            # AshvaVolt 3S2P 5.8 Ah, laid flat, label up
BATT_CLEAR = 1.5                        # per side
BATT_WALL_H = 15.0
BATT_TRAY_CENTER = (-65.0, 0.0)         # leads exit at the rear (-X) end
# countersunk M3 from inside the tray down through the deck, relative to tray centre
TRAY_HOLES = [(-28.5, 0.0), (28.5, 0.0), (0.0, -25.75), (0.0, 25.75)]
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
