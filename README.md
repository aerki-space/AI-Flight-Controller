# AI-Flight-Controller

A compact flight controller for small drones, built to pair with an onboard AI computer and a DroneCAN
peripheral ecosystem.

> **Status:** In active development. Hardware design files, firmware and validation results will be
> published as they are completed. Specifications below are design targets and may change.

## Key specifications

| | |
|---|---|
| Processor | STM32H7 (Cortex-M7, 480 MHz); custom SoC planned for future revisions |
| Sensors | Dual redundant IMUs, barometer |
| RC link | Integrated nano ExpressLRS receiver (2.4 GHz) |
| AI companion | NVIDIA Jetson Orin Nano Super, via Ethernet and UART |
| Peripherals | DroneCAN over CAN FD (2 buses) |
| Firmware | ArduPilot (primary), PX4 |
| Form factor | 36 × 36 mm, 30.5 mm mounting pattern |
| Input power | 2S – 6S |

## Repository layout

```
docs/
  architecture.md   system overview, interfaces and power
  companion.md      pairing with the Jetson Orin Nano Super
  dronecan.md       CAN buses, peripherals, bus load, radar integration
  firmware.md       ArduPilot / PX4 / INAV / custom: comparison and plan
hardware/
  README.md         board outline, connectors, power tree
tools/
  can_bus_load.py   DroneCAN bus-load estimate (classic CAN vs CAN FD)
  power_budget.py   avionics power and hover-time impact
tests/              checks for the tools
```

## Quick start

```sh
pip install -r tools/requirements.txt
python3 tools/can_bus_load.py
python3 tools/power_budget.py
python3 -m unittest discover -s tests
```

## Roadmap

- Hardware design files
- ArduPilot board port
- Companion-computer integration guide
- Test and validation results
- Next-generation revision on a custom SoC

More details coming soon.

## License

MIT, see [LICENSE](LICENSE).
