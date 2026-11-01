# DroneCAN

## Buses

| Bus | Devices | Why |
|---|---|---|
| CAN1 (FD) | GNSS + compass, radar, battery monitor, airspeed, other sensors | Sensor traffic, including large radar messages |
| CAN2 (FD) | ESCs, plus redundant copies of critical sensors if fitted | Keeps propulsion commands off the busiest bus |

**Connectors and electrical:**
- **Connectors:** standard 4-pin JST-GH (5 V, CAN_H, CAN_L, GND), two per bus so devices can be daisy-chained.
- **Termination:** 120 Ω, switchable on the board.
- **Nominal rate:** 1 Mbit/s.
- **CAN FD data rate:** up to 5 Mbit/s once every node on the bus supports it. Classic-CAN nodes can't share a bus
  that is running in FD mode, so check every device before switching a bus to FD.

## Bus load

From `python3 tools/can_bus_load.py`, using real DroneCAN framing and worst-case bit stuffing. It covers a quad with
4 ESCs, GNSS, compass, barometer, a battery monitor and the AERKI radar, with all traffic on one bus as a worst case.

| | Classic CAN, 1 Mbit/s | CAN FD, 1 / 5 Mbit/s |
|---|---|---|
| ESC commands (400 Hz) | 6.4 % | 3.5 % |
| Radar detections (16 targets, 20 Hz) | 8.2 % | 1.1 % |
| **Total** | **~24 %** | **~7 %** |

Classic CAN works for this build. CAN FD leaves room for more sensors, higher ESC rates and a second radar. Splitting
the ESCs onto CAN2 halves the load on either bus.

## Radar integration (AERKI Drone-Can-Radar)

The radar is a DroneCAN node. It publishes:
- the standard `uavcan.equipment.range_sensor.Measurement` message (the nearest return);
- its own vendor-specific messages, `aerki.radar.Detections` (20400) and `aerki.radar.Status` (20401);
- a vendor-specific service, `aerki.radar.SetBeam` (230).

**ArduPilot:**
1. `CAN_P1_DRIVER = 1`, `CAN_D1_PROTOCOL = 1` (DroneCAN on bus 1).
2. Set a rangefinder to the DroneCAN type, with its address matching the radar's `SENSOR_ID`. The radar then works
   as a forward or downward rangefinder with no code changes.
3. Obstacle avoidance: map the radar's detections to proximity sectors. ArduPilot already defines a DroneCAN
   proximity message (`ardupilot.equipment.proximity_sensor.Proximity`, ID 21910). If the radar publishes it as
   well, there's no need for a custom driver. This is the preferred route, and it's tracked in the radar
   repository.

**PX4:** enable DroneCAN (`UAVCAN_ENABLE`) and the rangefinder subscription. Avoidance from `Detections` needs a
PX4 driver, or the Jetson can use the detections in its own planner.

**Jetson:** the companion can read the radar's detections through the flight controller (forwarded over
MAVLink/DDS). Alternatively, it can listen on the CAN bus directly through its own CAN interface, which gives
lower delay for perception that combines radar and camera.
