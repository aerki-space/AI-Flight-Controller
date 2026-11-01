# Companion computer: Jetson Orin Nano Super

NVIDIA rates the Orin Nano module at up to 67 TOPS (sparse INT8) in its 25 W "super" mode. It runs perception
(detection, segmentation, depth), mapping and planning, and sends commands to the flight controller.

## Links

| Link | Use | Notes |
|---|---|---|
| Ethernet (100 Mbit, RMII on the flight controller) | Primary: MAVLink over UDP, and/or DDS (ROS 2) | ArduPilot's DDS interface and PX4's uXRCE-DDS both run over UDP. Plenty of bandwidth for telemetry and setpoints. |
| UART (MAVLink 2, 921600 baud or higher) | Fallback and bring-up | Independent of the network stack. Keep it connected even when Ethernet is in use. |
| CAN (optional) | Listening on DroneCAN traffic directly, for example radar detections | Through a CAN interface on the Jetson carrier |

**Connectors:**
- **Ethernet:** a 4-pin JST-GH in the Pixhawk-standard layout, with a short twisted pair. No magnetics on the
  flight controller side; use capacitive coupling for short runs, and confirm it with the PHY vendor's guidance.
- **UART:** 6-pin JST-GH (TX, RX, CTS, RTS, GND, plus an unused pin).

## Software

- **ArduPilot:**
  - set the companion serial port, or a networking port, to MAVLink 2;
  - use Guided mode for position, velocity and attitude setpoints;
  - `AP_DDS` gives native ROS 2 topics;
  - Lua scripts can run small on-board behaviours without the companion.
- **PX4:**
  - uXRCE-DDS gives ROS 2;
  - offboard mode takes setpoints from the companion.
- **Time:** synchronise the two clocks (MAVLink `TIMESYNC`, or the DDS time-sync), so the companion's camera frames
  and the flight controller's estimator agree on time.

## Failsafe

- **Companion heartbeat:** the companion sends a heartbeat. If setpoints stop arriving, the flight controller
  times out (ArduPilot: Guided-mode timeout; PX4: offboard-loss action) and holds position or lands.
- **Commands are bounded:** every companion command is checked against the flight controller's own geofence and
  speed and altitude limits.
- **Boot order:** the flight controller boots in seconds, the Jetson in tens of seconds. The vehicle must be safe
  and disarmed until the companion reports ready, or must be able to fly a basic mission without it.

## Power

Peak draw in 25 W mode needs a dedicated 5 V supply of 5 A or more, with low ripple, on its own connector. Brown-outs
on the Jetson during motor transients are the most common integration failure. Measure the 5 V rail with the motors
at full throttle. See [architecture.md](architecture.md) for the effect on hover time.
