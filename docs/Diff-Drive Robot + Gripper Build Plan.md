# Diff-Drive Robot + Gripper Build Plan

Oct 8, 2026 · @Harish Raju

## Read this first

Building both robots in parallel only works at 4–5 hrs/week if they are one robot: a single differential-drive base, with the 2-finger gripper and the vacuum gripper as swappable modules bolted to its top deck. That plan takes about 34 weeks (\~155 hours) including the Phase 6 fetch mission and is the structure of everything below.

What this plan already pushed back on:

- **No steppers or BLDC for the drive.** Steppers draw current while idle and run open-loop; BLDC needs FOC drivers and tuning that is a project of its own. 12 V geared DC motors with Hall encoders are the standard hobby diff-drive choice and give you real odometry for ROS 2.
- **The gripper is servo-driven, not stepper-driven.** A parallel-jaw gripper on one metal-gear servo is simpler, lighter and fast enough. A stepper only earns its place in a lead-screw lift, which this plan does not need.
- **Don't 3D-print the decks.** At service rates of roughly ₹3–8 per gram for PLA and ₹5–12 for PETG, two 250 mm decks cost more than laser-cut 5 mm acrylic or plywood. Print only the brackets, mounts and gripper parts.
- **ESP32 + micro-ROS alone can't do navigation.** The ESP32 handles motors, encoders, IMU and servos in real time. A Raspberry Pi 5 on board runs ROS 2, the lidar and Nav2 from Phase 4 on; your Ubuntu PC is the dev and visualisation machine.
- **Full spec runs over ₹25,000.** The lidar, Pi 5 and camera alone are \~₹16,000. The BOM section shows a core build that fits, and what to defer.

Locked decisions:

| Decision | Choice | Why |
| --- | --- | --- |
| Drive | 2× 25GA-370 12 V encoder gear motors, 65 mm wheels, 2 casters | Encoders for odometry; plug-and-play 6-pin |
| Motor driver | Cytron MDD3A (3 A cont., 4–16 V) | TB6612FNG's 1.2 A is marginal for 370-size motor stall current |
| Real-time controller | ESP32-S3 running micro-ROS | Ties into ROS 2; dual-core, enough PWM and pulse counters |
| On-board computer | Raspberry Pi 5 4 GB (Phase 4) | Runs lidar driver, SLAM Toolbox, Nav2 |
| Power | 3S Li-ion 11.1 V pack with BMS | Matches 12 V motors and pump |
| Gripper A | Parallel-jaw, 1× MG996R on a 4-bar linkage | Fingers stay parallel; one actuator |
| Gripper B | 12 V mini vacuum pump + release valve + 30 mm cup | Same mount plate as gripper A |
| Printing | PETG via a Bengaluru/online service | Stronger and more heat-tolerant than PLA for brackets |

## End-product looks

All three are the same 250 mm two-deck base with a different top module, so you build once and reconfigure. These are concept blocks to scale, not CAD: they fix proportions and layout, not part geometry.

&#91;image: Concept A, Sentinel patrol rover\]

**A — Sentinel (security and monitoring).** Lidar raised on a mast so it sees over the deck clutter, a pan-tilt Pi camera at the front, an LED ring for status. This is the end state of Phase 4 and the closest match to your home-security goal.

&#91;image: Concept B, Fetcher with 2-finger gripper\]

**B — Fetcher (2-finger gripper).** One servo raises a short arm; a second servo closes a parallel-jaw gripper that reaches below the front bumper to pick objects up to \~60 mm wide off the floor. Lidar moves to the deck, slightly occluded at the front.

&#91;image: Concept C, Picker-V vacuum end-effector\]

**C — Picker-V (vacuum).** The 12 V pump and release valve sit on the top deck; a boom lowers a 30 mm suction cup onto flat items (paper, cards, packets). Smooth, non-porous surfaces only; that limit is real, not a design flaw.

## System architecture

The ESP32 owns everything with a deadline — wheel PID, encoder counting, servo and pump control — so a dropped Wi-Fi packet stops the robot rather than crashing it. ROS 2 lives on the Pi once it arrives; until then the micro-ROS agent runs on your Ubuntu PC.

&#91;embedded content: system architecture · 3 compute tiers\]

The dashed link is temporary: in Phase 4 the ESP32 moves from Wi-Fi to a USB serial link with the Pi, which is lower-latency and doesn't depend on your router.

## Mechanical design

The base is two 250 mm round decks on 60 mm standoffs, with the wheels on the centre line so it turns in place; every module bolts to one shared mount plate on the top deck.

### Base

- **Decks:** 2× 250 mm discs, 5 mm acrylic or 6 mm birch ply, laser-cut locally. Round + centred wheels = it can spin out of any corner it drives into.
- **Wheels:** 65 mm, on the deck's centre line, motors clamped under the lower deck. Two ball casters, front and rear, 1–2 mm shorter than wheel contact so the drive wheels never lift.
- **Sanity check, drive:** at an assumed \~2.5 kg all-up, accelerating at 0.5 m/s² needs about 0.03 N·m per wheel. A 12 V 25GA-370 in the \~200 RPM range has many times that, and gives \~0.68 m/s top speed on 65 mm wheels. Pick the \~150–200 RPM gearing, not the 12–60 RPM ones.
- **Layout:** battery low and central on the lower deck (centre of mass inside the wheel/caster footprint); ESP32, MDD3A and bucks beside it; Pi 5 and lidar on the top deck.

### Gripper A — parallel jaw

- One MG996R drives a gear pair; each gear carries a 4-bar parallelogram so the finger pads stay parallel as they close. Opening \~0–60 mm.
- TPU finger pads (or a strip of silicone) — hard PETG fingers drop smooth objects.
- Shoulder: a second MG996R lifts the arm. **Torque check:** a 150 mm arm holding the \~175 g gripper plus a 200 g object needs roughly 6 kg·cm, about 55–65% of the MG996R's 9–11 kg·cm stall. That works but runs hot; keep the arm ≤ 150 mm or add a tension spring as counterbalance.

### Gripper B — vacuum

- 12 V mini pump (−30 to −40 kPa class) → T-fitting → 30 mm bellows cup, with a 12 V normally-open solenoid to vent and release.
- **Holding force:** −30 kPa on a 30 mm cup is \~21 N in theory; with a 4× safety factor for leaks and peel, plan on \~0.5 kg on smooth surfaces. Fabric, cardboard edges and textured plastic will leak.
- Same mount plate and shoulder servo as gripper A, so swapping modules is 4 screws and one connector.

### Printed parts (PETG unless noted)

| Part | Qty | Est. weight (g) | Notes |
| --- | --- | --- | --- |
| Tolerance test coupon | 1 | 30 | Print FIRST: M3 holes, heat-set insert bosses, motor D-shaft bore, servo spline fit |
| Motor clamps | 2 | 40 | Split clamp around the 25 mm gearbox |
| Caster mounts | 2 | 20 | Shim slots for height tuning |
| Battery tray + strap anchors | 1 | 60 | Velcro-strap slots |
| Electronics plate | 1 | 50 | ESP32, MDD3A, 2 bucks, terminal block |
| Lidar mast base + top plate | 1 set | 70 | Mast itself = 10 mm aluminium tube or M8 threaded rod |
| Camera pan-tilt bracket | 1 | 40 | Two SG90 or one MG90S + fixed tilt |
| Module mount plate (dovetail) | 1 | 60 | Shared by both grippers |
| Shoulder bracket + arm link | 1 set | 70 |  |
| Gripper palm, gears, 4-bar links, fingers | 1 set | 110 | Pads in TPU, \~10 g |
| Vacuum boom, cup holder, pump clamp | 1 set | 70 |  |
| Bumper ring segments | 3 | 90 | Optional; protects furniture |
| **Total, first pass** |  | **\~720** | Budget \~50% more for reprints → \~1.1 kg |

Use heat-set M3 inserts in every printed part that gets unscrewed more than once; screws threaded directly into PETG strip after a few cycles.

## Electronics & power

One 3S Li-ion pack feeds three separate rails — motors at battery voltage, 5 V for the Pi, 6 V for servos — so a stalled servo can never brown out the Pi or the ESP32.

### Power rails

| Rail | Source | Feeds | Notes |
| --- | --- | --- | --- |
| Battery, 9.0–12.6 V | 3S Li-ion + BMS → 10 A fuse → main switch | MDD3A (motors), vacuum pump, solenoid valve | Pump and valve switched by logic-level MOSFETs with flyback diodes |
| 5.1 V, 5 A | Buck converter (XL4015 class) | Raspberry Pi 5 → lidar (USB), ESP32 (USB) | Pi 5 limits USB current below 5 A; lidar draws \~230 mA |
| 6 V, ≥ 3 A | UBEC or second buck | Shoulder + gripper MG996R, camera pan-tilt servo | 1000 µF capacitor at the servo header; MG996R stall can pass 2.5 A |
| 3.3 V | ESP32 on-board regulator | IMU, encoder Hall sensors | Powering encoders at 3.3 V keeps their outputs safe for ESP32 pins |

All grounds meet at one star point on the electronics plate. Before the Pi arrives (Phases 0–3), the ESP32 runs off the 5 V buck and talks to the Ubuntu PC over Wi-Fi.

### ESP32-S3 pin plan (DevKitC-1 N16R8)

| Function | GPIO | Peripheral |
| --- | --- | --- |
| MDD3A M1A / M1B (left motor) | 4 / 5 | LEDC PWM, 20 kHz |
| MDD3A M2A / M2B (right motor) | 6 / 7 | LEDC PWM, 20 kHz |
| Left encoder A / B | 15 / 16 | PCNT quadrature |
| Right encoder A / B | 17 / 18 | PCNT quadrature |
| IMU SDA / SCL | 8 / 9 | I2C |
| Shoulder servo / gripper servo | 10 / 11 | LEDC 50 Hz |
| Pump MOSFET / valve MOSFET | 12 / 13 | GPIO |
| Battery voltage (divider 100k/22k) | 1 | ADC1 |

Avoid GPIO 0, 3, 45, 46 (boot strapping), 19/20 (native USB) and 35–37 (octal PSRAM on N16R8 boards).

### Runtime

A 3S 2600 mAh pack holds \~29 Wh. With the Pi 5, lidar and motors running (\~15 W, estimated), expect a little over 1.5 hours. For the Sentinel's patrol use, plan on a 3S2P (\~5200 mAh) pack from Phase 4.

## Phased build plan

Seven phases over about 34 weeks (\~155 hours at 4–5 hrs/week), each closed by a measurable gate; the gripper starts only after the base passes its Phase 2 gate, which is how "both in parallel" stays one robot.

&#91;embedded content: build roadmap · 6 phases, 6 gates\]

The Phase 3 gate is also the spending gate: the Pi 5 and lidar (₹13,250) are bought only once the base and gripper work.

### Tasks

**Phase 0 — Setup (weeks 1–2)**

- [ ] Install ROS 2 Jazzy on the Ubuntu PC; run the turtlesim and teleop tutorials
- [ ] Flash micro-ROS on the ESP32-S3 (PlatformIO); publish an Int32 over Wi-Fi to the agent
- [ ] Generate and order the tolerance coupon and motor clamps
- [ ] Order Phase 0–1 electronics (BOM lines 1–5, 7–9, 11–13)

**Phase 1 — Drive base (weeks 3–6)**

- [ ] Laser-cut decks; mount motors, casters, standoffs
- [ ] Wire battery, fuse, switch, MDD3A and 5 V buck
- [ ] Read both encoders with PCNT; confirm counts per wheel revolution
- [ ] Tune a per-wheel speed PID; drive by keyboard

**Phase 2 — ROS 2 base (weeks 7–10)**

- [ ] Subscribe /cmd\_vel on the ESP32; publish wheel ticks and /imu
- [ ] Odometry node and TF (odom to base\_link); URDF with measured wheel radius and track width
- [ ] Fuse IMU yaw with robot\_localization; run the 1 m square test

**Phase 3 — 2-finger gripper (weeks 11–15)**

- [ ] Generate gripper, shoulder and mount plate; one print order
- [ ] Add the 6 V servo rail; drive both MG996R from the ESP32
- [ ] ROS 2 service for open/close/lift/lower; grab test on 3 objects

**Phase 4 — Navigation (weeks 16–19)**

- [ ] Pi 5 with Ubuntu and ROS 2 Jazzy; move the micro-ROS agent to it over USB serial
- [ ] Mount the RPLIDAR C1 on the mast; run the sllidar\_ros2 driver
- [ ] Map one room with SLAM Toolbox; save the map
- [ ] Nav2 on the saved map; send goals from RViz on the PC

**Phase 5 — Vacuum + demo (weeks 20–22)**

- [ ] Generate the vacuum boom and pump clamp; wire pump and valve MOSFETs
- [ ] Pick-and-place test on cards, packets, paper
- [ ] Record a 2–3 minute demo: map, navigate, pick, swap modules

## Phase 6: Fetch mission (weeks 23–34)

By week 34 you can ask the robot, in plain words, to fetch a tagged object from another room off any surface up to 60 cm (2 ft) high and bring it back to you, avoiding furniture and people on the way. It adds about 12 weeks and about ₹11,700, taking the project to roughly ₹41,500 in total.

### What it can and can't fetch

| Constraint | Limit | Why |
| --- | --- | --- |
| Surface height | Floor to 60 cm | Lift travel; fingertips reach about 3–73 cm |
| Object | 20–60 mm wide, at least 40 mm tall, at most 250 g | Gripper opening and a safe load for the MG996R |
| Position | On a printed AprilTag pad, within 10 cm of the surface edge | The camera finds the tag, not the object; reach past the bumper is about 12 cm |
| Route | Mapped rooms, door thresholds under 10 mm | 65 mm wheels |
| Driving | 0.3 m/s, carriage lowered | The robot is about 95 cm tall with the lift up; driving with it raised risks tipping |

### Hardware changes

- **The Phase 3 servo shoulder is replaced by a vertical lift.** A 2020 aluminium column at the front of the top deck carries a carriage on V-wheels, driven by a NEMA17 stepper turning an 800 mm T8 lead screw. The lead screw self-locks, so the carriage holds its height with power off. The parallel-jaw gripper and its MG996R move onto a fixed 150 mm arm on the carriage.
- **A USB camera on the carriage** (eye-in-hand) reads the AprilTag on each pickup pad and gives the gripper's exact offset from it.
- **Three VL53L1X distance sensors** low on the front bumper catch what the lidar's scan plane misses: cables, slippers, toys.
- **A hardware e-stop** that cuts every actuator, and a **3S2P battery** for the extra load.
- The column blocks about 7° of the lidar's view to the front; mask that sector in the lidar filter.

Circuits for all of this are in the companion electronics doc.

### How a fetch runs

1. You type or say: "bring the red box from the bedroom shelf".
2. An LLM turns the request into a mission (pickup: bedroom\_shelf, tag: 3, drop-off: sofa). It may only choose from places and tags you've taught it; anything else gets a clarifying question.
3. Nav2 drives to the pickup waypoint, re-planning around people and pets. Nav2's collision monitor slows and stops the robot inside set distances.
4. At the pad, the camera finds the tag; the base creeps forward and the lift rises until the gripper lines up.
5. Grip, lower to carry height, drive back, raise to hand-over height and open.
6. A behaviour tree runs these steps with retries. If the tag can't be found or a grip fails twice, the robot comes back and says so instead of trying forever.

The LLM layer is the most portfolio-relevant part of this phase for AI backend roles: a constrained natural-language interface driving ROS 2 actions, with guardrails on what it's allowed to request.

**Gate:** 8 of 10 fetches succeed across 3 tagged objects (floor, 45 cm and 60 cm surfaces) in 2 rooms, with someone walking across the path once per run and no collisions.

### Tasks

- [ ] Generate and print the lift column brackets, carriage, arm and gripper mount; assemble the lift with its home switch
- [ ] Wire the TMC2209 and e-stop; ROS 2 action server for lift home and move-to-height
- [ ] Mount 3 ToF sensors; publish ranges; add a range layer to both Nav2 costmaps and enable the collision monitor
- [ ] Calibrate the carriage camera; run apriltag\_ros; print tag pads
- [ ] Teach pickup and drop-off waypoints in each room; store them in YAML
- [ ] Build the mission behaviour tree: navigate, align, lift, grip, carry, hand over, with retry and give-up rules
- [ ] Natural-language front end: request to mission JSON, limited to known places and tags
- [ ] Run the 10-fetch gate and log every result

### Phase 6 parts

| Item | Qty | Approx. ₹ | Source |
| --- | --- | --- | --- |
| NEMA17 stepper, 4.2 kg·cm, 1.6 A | 1 | 649 | [Probots](https://probots.co.in/nema17-stepper-motor-4-2-kg-cm-single-shaft-1-8-degree.html) |
| TMC2209 stepper driver | 1 | 639 | [Robu](https://st.robu.in/product/tmc2209-stepper-motor-driver) |
| T8 lead screw 800 mm + brass nut, coupler, 2 bearings | 1 set | 1,200 | *est.* |
| 2020 V-slot extrusion 900 mm + carriage plate + 4 V-wheels | 1 set | 1,300 | *est.* |
| VL53L1X ToF module | 3 | 2,397 | [Probots](https://probots.co.in/vl53l1x-tof-laser-ranging-sensor-module.html) (₹799 each) |
| USB camera, 1080p, wide-angle | 1 | 1,500 | *est.* |
| E-stop, 2-pole latching, 10 A DC | 1 | 350 | *est.* |
| Microswitches (home, spare) | 2 | 60 | *est.* |
| Drag chain, high-flex USB and servo cable | 1 lot | 400 | *est.* |
| 3S2P pack upgrade (\~5,200 mAh) | 1 | 1,500 | *est.*; same line as the Sentinel extra, don't buy twice |
| 3D printing, \~400 g PETG | 1 lot | 1,600 | at ₹2.5–6/g |
| Capacitors, tag pad printing | 1 lot | 100 | *est.* |
| **Phase 6 total** |  | **11,695** |  |

Two cheaper options: drop to 2 ToF sensors (−₹799), and use the Sentinel's Pi Camera on a 1 m ribbon instead of a USB camera (−₹1,500), at the cost of a ribbon that may crack from flexing.

## Bill of materials

The full build through the vacuum gripper comes to about ₹29,800, roughly ₹5,000 over your ₹25,000 ceiling; the Raspberry Pi 5 and lidar together are ₹13,250 of it. Spending is staged by phase, so nothing past ₹14,300 is needed until week 16.

Prices are approximate, India, incl. GST where the listing showed it, checked October 2026. Lines marked *est.* had no listing in my searches and are typical hobby-store figures — verify before ordering.

| # | Item | Qty | Approx. ₹ | Phase | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | 25GA-370 12 V gear motor with Hall encoder (\~150–200 RPM) | 2 | 1,180 | 1 | [Zbotic](https://zbotic.in/product/25ga-370-12v-26rpm-dc-reducer-gear-motor-with-encoder/) (₹590 ea; ₹320–450 elsewhere per [Zbotic guide](https://zbotic.in/geared-motor-with-encoder-buy-vs-diy-for-robot-wheels-india/)) |
| 2 | 65 mm wheels with 4 mm hubs | 2 | 300 | 1 | *est.* |
| 3 | Ball casters | 2 | 150 | 1 | *est.* |
| 4 | Cytron MDD3A dual motor driver, 3 A | 1 | 615 | 1 | [Robu](https://robu.in/product-tag/cytron-mdd3a) (₹521 + 18% GST) |
| 5 | ESP32-S3-DevKitC-1 N16R8 | 1 | 1,100 | 0 | [price-history.in](https://price-history.in/product/esp32-s3-devkit-n16r8-board-otg-CCNl0LIm) (₹945–1,549) |
| 6 | BNO085 9-axis IMU breakout | 1 | 1,800 | 2 | *est.* for a breakout; bare chip ₹1,216 at [Mouser India](https://www.mouser.in/c/sensors/?m=CEVA) |
| 7 | 3S 18650 pack, 2600 mAh, with BMS | 1 | 1,500 | 1 | *est.*; 3S BMS alone \~₹399 ([price-history.in](https://price-history.in/product/ug-land-india-s-0a-bms-32r0mBce)) |
| 8 | 12.6 V Li-ion charger | 1 | 450 | 1 | *est.* |
| 9 | 5.1 V 5 A buck converter | 1 | 350 | 1 | *est.* |
| 10 | 6 V ≥3 A UBEC for servos | 1 | 350 | 3 | *est.* |
| 11 | Fuse, switch, XT60, silicone wire, terminal block | 1 lot | 600 | 1 | *est.* |
| 12 | Laser-cut decks, 250 mm, acrylic or ply | 2 | 600 | 1 | *est.* |
| 13 | M3 screws, heat-set inserts, 60 mm standoffs | 1 lot | 600 | 1 | *est.* |
| 14 | 3D printing, \~1.1 kg PETG incl. reprints | 1 lot | 4,000 | 1–5 | ₹2.5–6/g: [TechEnclave](https://techenclave.com/t/3d-printing-service-pan-india/385629), [Zbotic comparison](https://zbotic.in/3d-printing-service-comparison-india-2026-zbotic-vs-a3dxyz-vs-3ding-and-more/) |
| 15 | MG996R metal-gear servo | 2 | 680 | 3 | [Probots](https://probots.co.in/mg996r-high-torque-servo-motor-180-degree-9kg-servo.html) (₹339 ea) |
| 16 | Raspberry Pi 5, 4 GB | 1 | 6,500 | 4 | [Zbotic](https://zbotic.in/raspberry-pi-5-vs-raspberry-pi-4-complete-upgrade-guide-india-2026/) (₹6,500–7,500); [Think Robotics](https://thinkrobotics.com/blogs/product-reviews-buying-guides/raspberry-pi-5-price-india-complete-cost-analysis-and-buying-guide) (₹5,500–6,200) |
| 17 | Pi 5 active cooler | 1 | 500 | 4 | *est.* |
| 18 | microSD 64 GB A2 | 1 | 600 | 4 | *est.* |
| 19 | Slamtec RPLIDAR C1 | 1 | 6,749 | 4 | [Robu](https://st.robu.in/?p=1840849) |
| 20 | 12 V mini vacuum pump, 1.2 L/min, −30 kPa | 1 | 586 | 5 | [Robu](https://aws.robu.in/product/12v-dc-1-2l-m-mini-vacuum-pump) |
| 21 | 12 V solenoid valve, 30 mm bellows cups, tubing, 2 MOSFET modules | 1 lot | 600 | 5 | *est.* |
|  | **Total through Phase 5** |  | **29,810** |  |  |
| 22 | Pi Camera Module 3 *(Sentinel, optional)* | 1 | 3,005 | 6 | [ThingBits](https://thingbits.in/products/raspberry-pi-camera-module-3) |
| 23 | SG90 servos for pan-tilt *(optional)* | 2 | 180 | 6 | [Zbotic](https://zbotic.in/mini-servo-motor-under-100-rupees-best-budget-picks-india/) (₹60–90 ea) |
| 24 | Upgrade to 3S2P \~5200 mAh pack *(optional)* | 1 | 1,500 | 6 | *est.* |
|  | **Total with Sentinel extras** |  | **34,495** |  |  |

To get under \~₹25,200 without losing navigation: swap the BNO085 for an MPU-6050 (−₹1,650, noisier heading), use a ₹2.5/g hobbyist print service (−₹1,250, slower turnaround) and buy the Pi 5 2 GB (−₹1,750, tight for Nav2 + SLAM). I would cut the first two and keep the 4 GB Pi.

By phase: Phases 0–3 (base + 2-finger gripper) ≈ **₹14,300**; Phase 4 adds ≈ ₹14,350; Phase 5 adds ≈ ₹1,190.

## CAD workflow and connectors

You don't need a CAD connector to get print-ready files: I can write each part as a parametric CadQuery script here, export STEP + STL, and render a preview for you to check. The connectors below are for storing, versioning and laying out, not for the modelling itself.

| Connector | Status in your account | What it's for here | Verdict |
| --- | --- | --- | --- |
| GitHub | Available — I can attach a repo | One repo holding CAD scripts, STL/STEP exports, ESP32 firmware and ROS 2 packages; every tolerance change is a commit | **Connect: most useful** |
| Google Drive | Already connected | Drop final STLs in a folder and share one link with the print service | **Use as-is** |
| Trimble SketchUp | Installed, needs reconnecting | Whole-robot layout mockups (where the lidar mast sits, module clearance) | Optional. It is a surface modeller; don't use it for toleranced parts like the gripper gears or motor clamps |
| Onshape / Fusion 360 | No connector exists | If you want to hand-edit parts, import my STEP files there | Manual only |

How a part goes from idea to printed:

1. I write a CadQuery script per part from datasheet dimensions (25GA-370 gearbox, MG996R body, RPLIDAR C1 — Slamtec publishes a [C1 STEP model](https://core-electronics.com.au/rplidar-c1-dtof-lidar-360-laser-range-scanner-12m-ip54.html)). Shared values like hole clearance and insert bore live in one `params.py`.
2. I export STL + STEP and send a rendered preview; you check fit against the real part with calipers.
3. Print the 30 g tolerance coupon first. Measure it, change one number in `params.py`, regenerate every part. This is what keeps a print-service loop from costing you a week per mistake.
4. Batch parts per order — most services charge a per-order fee (e.g. ₹100 at the TechEnclave service), so 6 parts in one order beats 6 orders.
5. Commit scripts and exports to GitHub; put the order's STLs in a Drive folder for the service.

To start: tell me the GitHub repo name you want (or let me create the structure in a new one), and reconnect SketchUp only if you want layout mockups.

## Risks and failure modes

The biggest risk is schedule, not hardware: 22 weeks at 4–5 hrs/week assumes few dead ends, and first-time micro-ROS and Nav2 setups routinely eat a few evenings each.

| Risk | Likelihood | What happens | Fallback |
| --- | --- | --- | --- |
| micro-ROS over Wi-Fi drops or lags | High | Jerky teleop, odometry gaps | Switch the ESP32 to serial transport once the Pi is on board; keep the PID loop on the ESP32 so a lost link just stops the robot |
| Print-service turnaround (3–7 days) stalls a phase | High | A wrong hole = a lost week | Tolerance coupon first; batch orders; keep a hand drill and files for small fixes |
| Odometry drift | Medium | Maps smear, Nav2 gets lost | Measure wheel diameter and track width precisely; fuse IMU yaw via robot\_localization |
| Shoulder servo overheats | Medium | Gripper sags or servo dies | Arm ≤ 150 mm, add spring counterbalance, cut servo power when parked |
| Vacuum won't hold | Medium | Items drop | Expected on porous items; test on cards/packets only; larger cup |
| Li-ion pack damaged | Low, severe | Fire risk | Packs only with a BMS, a fuse at the pack, charge off the robot on a non-flammable surface |
| Budget overshoot | Certain at full spec | \~₹30k vs ₹25k | Phase-gated buying (BOM section); don't buy lidar/Pi until Phase 3's gate is passed |
| Scope creep from 'both in parallel' | High | Two half-built robots | The gripper only starts after the base passes its Phase 2 gate |

## Sources

- [Zbotic — 25GA-370 12 V encoder motor](https://zbotic.in/product/25ga-370-12v-26rpm-dc-reducer-gear-motor-with-encoder/)
- [Zbotic — geared encoder motor buy vs DIY, India](https://zbotic.in/geared-motor-with-encoder-buy-vs-diy-for-robot-wheels-india/)
- [Robu — Cytron MDD3A](https://robu.in/product-tag/cytron-mdd3a)
- [ThingBits — Cytron MDD3A specs](https://www.thingbits.in/products/4-16v-3a-dual-channel-dc-motor-driver)
- [Zbotic — motor driver alternatives (TB6612FNG ratings)](https://zbotic.in/low-cost-motor-driver-alternatives-to-l298n-under-200-rupees/)
- [price-history.in — ESP32-S3 N16R8](https://price-history.in/product/esp32-s3-devkit-n16r8-board-otg-CCNl0LIm)
- [Mouser India — CEVA BNO085](https://www.mouser.in/c/sensors/?m=CEVA)
- [price-history.in — 3S BMS](https://price-history.in/product/ug-land-india-s-0a-bms-32r0mBce)
- [Robu — RPLIDAR C1M1-R2](https://st.robu.in/?p=1840849)
- [Core Electronics — RPLIDAR C1 specs and STEP model](https://core-electronics.com.au/rplidar-c1-dtof-lidar-360-laser-range-scanner-12m-ip54.html)
- [Zbotic — Raspberry Pi 5 India pricing 2026](https://zbotic.in/raspberry-pi-5-vs-raspberry-pi-4-complete-upgrade-guide-india-2026/)
- [Think Robotics — Raspberry Pi 5 price India](https://thinkrobotics.com/blogs/product-reviews-buying-guides/raspberry-pi-5-price-india-complete-cost-analysis-and-buying-guide)
- [Probots — MG996R servo](https://probots.co.in/mg996r-high-torque-servo-motor-180-degree-9kg-servo.html)
- [Robu — 12 V 1.2 L/min vacuum pump](https://aws.robu.in/product/12v-dc-1-2l-m-mini-vacuum-pump)
- [ThingBits — Pi Camera Module 3](https://thingbits.in/products/raspberry-pi-camera-module-3)
- [Zbotic — SG90 budget servos](https://zbotic.in/mini-servo-motor-under-100-rupees-best-budget-picks-india/)
- [TechEnclave — pan-India 3D printing service rates](https://techenclave.com/t/3d-printing-service-pan-india/385629)
- [Zbotic — 3D printing service comparison India 2026](https://zbotic.in/3d-printing-service-comparison-india-2026-zbotic-vs-a3dxyz-vs-3ding-and-more/)
- [Zbotic — custom 3D printing pricing by material](https://zbotic.in/custom-3d-printing-service-india-guide/)
