# AI-Flight-Controller: contributor notes

STM32H7 flight controller for small drones, paired with a Jetson Orin Nano Super, with DroneCAN peripherals.
Design stage: docs and planning scripts. No schematic or PCB yet.

## Where things live
- `docs/`: design decisions and the numbers behind them. Numbers come from `tools/*.py`; when assumptions change,
  change them in the script, rerun it and update the doc from its output.
- `hardware/`: board outline, connectors, power tree. Schematic and layout files will go here.
- `tools/`: planning scripts. `can_bus_load.py` reads the radar's DSDL from `../drone-can-radar/dsdl/aerki` when
  that repository is checked out next to this one.

## Conventions
- The flight controller must stay safe without the companion computer; never make stable flight depend on it.
- Keep pin choices compatible with both ArduPilot and PX4 board definitions.
- New DroneCAN vendor IDs must not collide with the standard and known vendor sets. Check them with the radar
  repository's `tools/validate_dsdl.py`.
- Mark planning estimates as estimates.

## Checks before committing
```sh
python3 -m unittest discover -s tests
python3 tools/can_bus_load.py && python3 tools/power_budget.py
```
