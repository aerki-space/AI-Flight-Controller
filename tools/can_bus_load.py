#!/usr/bin/env python3
"""DroneCAN bus-load estimate for a typical small-drone build, classic CAN vs CAN FD.

Frame counts come from pydronecan's own transfer encoder (real DroneCAN framing:
tail byte, multi-frame CRC, CAN FD DLC rounding). Bit times use worst-case stuffing,
so the percentages are upper bounds.

    python3 tools/can_bus_load.py
    python3 tools/can_bus_load.py --radar-dsdl ../drone-can-radar/dsdl/aerki
"""
import argparse
import math
import os

import dronecan
from dronecan import transport


def frame_bytes(msg, canfd):
    """Lengths (bytes, incl. tail byte) of the CAN frames one transfer of msg needs."""
    t = transport.Transfer(payload=msg, source_node_id=10, transfer_id=0, transfer_priority=20,
                           service_not_message=False, canfd=canfd)
    return [len(f.bytes) for f in t.to_frames()]


def classic_frame_bits(n):
    """29-bit-ID classic CAN frame with n data bytes, worst-case bit stuffing, incl. 3-bit IFS."""
    return 67 + 8 * n + (54 + 8 * n - 1) // 4


def fd_frame_time_us(n, nominal_bps, data_bps):
    """29-bit-ID CAN FD frame with BRS and n data bytes (n already a valid FD length)."""
    arb_bits = 43 + 13                       # SOF..BRS with stuffing, then CRC delim/ACK/EOF/IFS
    crc = 17 if n <= 16 else 21
    data_bits = (5 + 8 * n) + (5 + 8 * n) // 4 + 4 + crc + math.ceil((4 + crc) / 4)
    return arb_bits / nominal_bps * 1e6 + data_bits / data_bps * 1e6


def traffic(radar):
    """(label, message instance, rate Hz, count) for a quad with GNSS, mag, baro, battery monitor and the radar."""
    U = dronecan.uavcan.equipment
    rows = [
        ('ESC command (4 motors)', U.esc.RawCommand(cmd=[8191] * 4), 400, 1),
        ('ESC status', U.esc.Status(), 25, 4),
        ('GNSS fix', U.gnss.Fix2(), 10, 1),
        ('GNSS auxiliary', U.gnss.Auxiliary(), 5, 1),
        ('Magnetometer', U.ahrs.MagneticFieldStrength2(), 50, 1),
        ('Barometer pressure', U.air_data.StaticPressure(), 50, 1),
        ('Barometer temperature', U.air_data.StaticTemperature(), 5, 1),
        ('Battery monitor', U.power.BatteryInfo(), 10, 1),
        ('Radar range (standard)', U.range_sensor.Measurement(), 20, 1),
        ('Node status (all nodes)', dronecan.uavcan.protocol.NodeStatus(), 1, 9),
    ]
    if radar:
        R = dronecan.thirdparty.aerki.radar   # custom namespaces land under `thirdparty`
        t = R.Target()
        rows.append(('Radar detections (16 targets)', R.Detections(targets=[t] * 16), 20, 1))
        rows.append(('Radar status', R.Status(), 1, 1))
    else:
        rows.append(('Radar detections (16 targets)', None, 20, 1))
    return rows


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument('--radar-dsdl', default=os.path.join(here, '..', '..', 'drone-can-radar', 'dsdl', 'aerki'))
    ap.add_argument('--nominal', type=float, default=1e6, help='nominal / arbitration bit rate')
    ap.add_argument('--data', type=float, default=5e6, help='CAN FD data-phase bit rate')
    a = ap.parse_args()
    radar = os.path.isdir(a.radar_dsdl)
    if radar:
        dronecan.load_dsdl(a.radar_dsdl)

    print(f'{"traffic":32s} {"rate":>9s}  {"classic frames":>14s} {"classic %":>9s}  {"FD frames":>9s} {"FD %":>6s}')
    tot_c = tot_f = 0.0
    for label, msg, hz, count in traffic(radar):
        if msg is None:                      # radar DSDL not available: 175-byte payload from the radar repo
            c_frames = [8] * 26
            f_frames = [64, 64, 64]
        else:
            c_frames = frame_bytes(msg, False)
            f_frames = frame_bytes(msg, True)
        per_s = hz * count
        c_us = sum(classic_frame_bits(n) for n in c_frames) / a.nominal * 1e6
        f_us = sum(fd_frame_time_us(n, a.nominal, a.data) for n in f_frames)
        lc, lf = per_s * c_us / 1e4, per_s * f_us / 1e4   # percent of bus time
        tot_c += lc
        tot_f += lf
        print(f'{label:32s} {hz:>5g} Hz x{count:<2d} {len(c_frames):>8d} {lc:>9.1f}  {len(f_frames):>9d} {lf:>6.1f}')
    print(f'{"TOTAL (worst-case stuffing)":32s} {"":12s} {"":>8s} {tot_c:>9.1f}  {"":>9s} {tot_f:>6.1f}')
    if not radar:
        print('(radar DSDL not found; used its documented 175-byte maximum)')
    print(f'classic CAN at {a.nominal/1e6:g} Mbit/s, CAN FD at {a.nominal/1e6:g}/{a.data/1e6:g} Mbit/s')


if __name__ == '__main__':
    main()
