#!/usr/bin/env python3
"""Avionics power budget and its effect on hover time, for each Jetson power mode.

All figures are planning assumptions listed below; replace them with measurements.

    python3 tools/power_budget.py
"""

# --- assumptions (edit here) -------------------------------------------------
AVIONICS_W = {                  # continuous draw excluding the Jetson
    'flight controller (STM32H7, sensors)': 1.0,
    'GNSS + compass': 0.5,
    'radar (DroneCAN, scanning)': 3.0,
    'telemetry / RC receiver': 1.0,
    'camera': 1.5,
}
JETSON_MODES_W = {              # module power modes; actual draw depends on the workload
    'off': 0.0,
    '7 W mode': 7.0,
    '15 W mode': 15.0,
    '25 W mode (MAXN super)': 25.0,
}
REGULATOR_EFF = 0.90            # battery -> 5 V / 3.3 V converters
BATTERY_WH = 4 * 3.7 * 3.0      # 4S 3000 mAh
USABLE = 0.80                   # keep 20 % reserve
HOVER_W = 180.0                 # propulsion power in hover for the target airframe (~1.2 kg class)
# -----------------------------------------------------------------------------


def budget(jetson_w):
    load = sum(AVIONICS_W.values()) + jetson_w
    from_battery = load / REGULATOR_EFF
    total = HOVER_W + from_battery
    minutes = BATTERY_WH * USABLE / total * 60
    return load, from_battery, minutes


def main():
    base_min = BATTERY_WH * USABLE / HOVER_W * 60
    print(f'battery {BATTERY_WH:.0f} Wh ({USABLE:.0%} usable), hover propulsion {HOVER_W:.0f} W '
          f'-> {base_min:.1f} min with no avionics load')
    for k, v in AVIONICS_W.items():
        print(f'  {k:40s} {v:5.1f} W')
    print(f'{"Jetson mode":26s} {"avionics":>9s} {"from batt.":>10s} {"hover time":>10s} {"lost":>6s}')
    for mode, jw in JETSON_MODES_W.items():
        load, batt, minutes = budget(jw)
        print(f'{mode:26s} {load:7.1f} W {batt:8.1f} W {minutes:8.1f} min {base_min - minutes:4.1f} min')
    print(f'5 V rail sizing for the Jetson at 25 W: {25 / 5:.1f} A continuous, plus margin for transients')


if __name__ == '__main__':
    main()
