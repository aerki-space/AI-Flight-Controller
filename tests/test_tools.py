"""Checks for the planning scripts:  python3 -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

import dronecan  # noqa: E402

import can_bus_load as cbl  # noqa: E402
import power_budget as pb  # noqa: E402


class FrameBits(unittest.TestCase):
    def test_classic_full_frame(self):
        # 29-bit ID, 8 data bytes: 131 bits before stuffing, 29 worst-case stuff bits
        self.assertEqual(cbl.classic_frame_bits(8), 160)

    def test_fd_faster_than_classic_for_large_payloads(self):
        classic_us = 9 * cbl.classic_frame_bits(8)          # 9 classic frames ~ 63 payload bytes
        fd_us = cbl.fd_frame_time_us(64, 1e6, 5e6)
        self.assertLess(fd_us, classic_us / 4)


class DroneCanFraming(unittest.TestCase):
    def test_esc_command_for_four_motors_is_single_frame(self):
        msg = dronecan.uavcan.equipment.esc.RawCommand(cmd=[0] * 4)
        self.assertEqual(cbl.frame_bytes(msg, canfd=False), [8])

    def test_gnss_fix_needs_multiframe_on_classic_but_not_fd(self):
        msg = dronecan.uavcan.equipment.gnss.Fix2()
        self.assertGreater(len(cbl.frame_bytes(msg, canfd=False)), 1)
        self.assertEqual(len(cbl.frame_bytes(msg, canfd=True)), 1)


class PowerBudget(unittest.TestCase):
    def test_more_jetson_power_means_less_hover_time(self):
        times = [pb.budget(w)[2] for w in sorted(pb.JETSON_MODES_W.values())]
        self.assertEqual(times, sorted(times, reverse=True))


if __name__ == '__main__':
    unittest.main()
