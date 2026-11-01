# Firmware

## Options compared

| | ArduPilot | PX4 | INAV | Custom |
|---|---|---|---|---|
| STM32H7 support | Mature, many boards | Mature (FMUv6 family) | Yes, for several H7 targets | Full control, everything from scratch |
| DroneCAN | Native, including CAN FD | Native (and Cyphal) | Limited / recent; verify for each device type | Write it yourself (libcanard) |
| Companion / AI link | MAVLink over UART or Ethernet, DDS (ROS 2), Lua scripting | MAVLink, uXRCE-DDS (ROS 2), offboard mode | Basic MAVLink only | Whatever you build |
| Autonomy features | Missions, guided mode, avoidance, terrain, precision landing | Missions, offboard, avoidance interfaces | Navigation for hobby flight | None out of the box |
| Porting effort | Low: one board definition (`hwdef.dat`) | Medium: board directory, NuttX config | Low to medium: target files | Very high |
| Licence | GPLv3 | BSD-3 | GPLv3 | Your choice |

## Plan

1. **ArduPilot first.** It's the shortest route to a flying board:
   - a `hwdef.dat` describing the pins, sensors and buses, plus a bootloader `hwdef-bl.dat`;
   - DroneCAN, CAN FD and Ethernet networking supported on H7 boards;
   - a guided mode and DDS interface that suit a Jetson companion;
   - an official board ID from the ArduPilot project, requested before release.
2. **PX4 second,** for users who prefer its offboard and ROS 2 workflow. Because both stacks use the same MCU
   families, keeping the pin choices compatible with ArduPilot's makes this mostly a configuration port.
3. **INAV: not targeted.** It's well suited to hobby and FPV flight, but lacks the companion-computer and DroneCAN
   depth this board is designed around.
4. **Custom firmware: no.** The value of this board is in the hardware and the integration, not in replacing a
   mature flight stack.

## Board definition: points to settle in the schematic

- One SPI bus per IMU, with data-ready interrupts routed to the MCU.
- FDCAN1 and FDCAN2 on pins that support CAN FD, each with its own transceiver and termination (enabled by a solder
  jumper).
- The Ethernet PHY on RMII, with its reference clock and reset line routed.
- The SDMMC 4-bit interface for logging.
- DShot-capable timers for the 8 motor outputs: they need DMA, so allocate DMA streams up front.
- A boot pin and USB DFU access for recovery.
