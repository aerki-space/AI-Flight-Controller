# Hardware

No schematic or layout yet. This is the starting outline.

## Board

| | Target |
|---|---|
| Outline | 36 × 36 mm, 30.5 × 30.5 mm M3 mounting (soft-mount grommets) |
| Layers | 6 to 8, with solid ground under the IMUs and the RF-sensitive areas |
| Mass | < 10 g, excluding the cable harness |
| Operating temperature | −20 to +70 °C ambient (IMU heater helps below 0 °C) |

## Connectors (JST-GH, Pixhawk connector standard pinouts)

| Connector | Qty | Notes |
|---|---|---|
| CAN1, CAN2 | 2 + 2 | 4-pin, two per bus for daisy-chaining |
| Ethernet (Jetson) | 1 | 4-pin |
| Telemetry / companion UART | 2 | 6-pin with flow control |
| GNSS (UART + I2C) | 1 | 10-pin, for non-CAN GNSS modules |
| RC input | 1 | CRSF / SBUS |
| Motor / servo outputs | 8 | PWM / DShot, plus ESC telemetry input |
| Power in | 1 | 2S – 6S, with an analog voltage/current sense option |
| Jetson 5 V out | 1 | High-current, separate from the peripheral 5 V |
| USB | 1 | USB-C |
| Debug (SWD) | 1 | Small-pitch connector or test pads |

## Power tree

```
2S–6S battery
 ├─ buck → 5 V (≥ 3 A)  → peripherals (CAN, GNSS, RC, telemetry)
 │                       → LDO → 3.3 V → MCU, sensors (separate low-noise LDO for the IMUs)
 ├─ buck → 5 V (≥ 6 A)  → Jetson connector (separate, protected)
 └─ USB 5 V (bench)     → MCU and sensors only (diode-OR)
```

**Protection:**
- each 5 V output has its own current limit;
- reverse-polarity protection on the main input;
- TVS diodes on the CAN lines and power inputs.
