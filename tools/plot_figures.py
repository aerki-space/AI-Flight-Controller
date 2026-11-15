#!/usr/bin/env python3
"""Regenerate the figures in docs/img from the planning tools.

    python3 tools/plot_figures.py
"""
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'docs', 'img')
sys.path.insert(0, HERE)
import can_bus_load as cbl  # noqa: E402
import power_budget as pb  # noqa: E402

INK, MUTED, GRID = '#1f2328', '#656d76', '#d0d7de'
PALETTE = ['#0969da', '#1a7f37', '#8250df', '#bf8700', '#cf222e', '#57606a']
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.edgecolor': GRID, 'axes.labelcolor': INK,
    'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.grid': True, 'grid.color': GRID,
    'grid.linewidth': 0.6, 'axes.spines.top': False, 'axes.spines.right': False,
    'figure.facecolor': 'white', 'axes.titleweight': 'bold', 'axes.titlesize': 11,
})


def chip(ax, x, y, w, h, label, fc='#1c1f24', fs=7, tc='white'):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle='round,pad=0,rounding_size=0.4',
                                fc=fc, ec='#0d0f12', lw=0.6, zorder=3))
    ax.text(x, y, label, ha='center', va='center', color=tc, fontsize=fs, zorder=4, linespacing=1.1)


def connector(ax, x, y, w, h, label, rot=0):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc='#f6f8fa', ec='#8c959f', lw=0.7, zorder=3))
    ax.text(x, y, label, ha='center', va='center', fontsize=6, color=INK, rotation=rot, zorder=4)


def fig_board():
    fig, ax = plt.subplots(figsize=(6.6, 6.9))
    ax.grid(False)
    ax.add_patch(FancyBboxPatch((-18, -18), 36, 36, boxstyle='round,pad=0,rounding_size=3',
                                fc='#16271d', ec='#0b1610', lw=1.5))
    for sx in (-1, 1):
        for sy in (-1, 1):
            ax.add_patch(Circle((sx * 15.25, sy * 15.25), 2.4, fc='#c9a227', ec='none', zorder=2))
            ax.add_patch(Circle((sx * 15.25, sy * 15.25), 1.6, fc='white', ec='none', zorder=2))
    chip(ax, 0, 1.5, 10, 10, 'STM32H7\nCortex-M7\n480 MHz', fs=8)
    chip(ax, -8.7, 5.0, 3.0, 2.6, 'IMU 1', fs=6)
    chip(ax, -8.7, 0.8, 3.0, 4.0, 'IMU 2', fs=6)
    chip(ax, -8.7, -3.6, 2.6, 2.4, 'baro', fs=6)
    chip(ax, 8.3, 4.6, 4.0, 4.0, 'ETH\nPHY', fs=6)
    chip(ax, 8.3, -0.6, 4.0, 3.2, 'CAN FD\n×2', fs=6)
    # onboard receiver under its shield can
    ax.add_patch(FancyBboxPatch((2.2, -14.0), 9.6, 7.2, boxstyle='round,pad=0,rounding_size=0.6',
                                fc='#aeb6bf', ec='#6e7781', lw=0.8, zorder=3, hatch='////'))
    ax.text(7.0, -10.4, 'ExpressLRS\n2 × LR1121\n(shield can)', ha='center', va='center', fontsize=6.5,
            color=INK, zorder=4, bbox=dict(fc='#aeb6bf', ec='none', pad=0.5))
    chip(ax, -7.8, -10.6, 6.5, 4.5, '5 V buck\nJetson, 6 A', fc='#2b3036', fs=6)
    chip(ax, -1.6, -10.6, 4.6, 4.5, '5 V buck\nperiph.', fc='#2b3036', fs=6)
    chip(ax, 0.0, -5.0, 3.0, 2.0, 'SD', fc='#2b3036', fs=6)
    # edge connectors (JST-GH)
    connector(ax, -6.5, 16.6, 6.0, 2.2, 'CAN1  CAN1')
    connector(ax, 1.5, 16.6, 6.0, 2.2, 'CAN2  CAN2')
    connector(ax, 16.6, 6.5, 2.2, 6.5, 'ETH (Jetson)', rot=90)
    connector(ax, 16.6, -2.6, 2.2, 7.5, 'TELEM  TELEM', rot=90)
    connector(ax, -16.6, 6.0, 2.2, 7.0, 'GNSS', rot=90)
    connector(ax, -16.6, -3.0, 2.2, 6.0, 'RC in', rot=90)
    connector(ax, -3.5, -16.6, 4.0, 2.2, 'USB-C')
    connector(ax, 7.0, -16.4, 3.0, 1.8, 'u.FL')
    for i in range(8):
        ax.add_patch(Rectangle((-11.0 + i * 1.3, 12.6), 0.9, 1.6, fc='#c9a227', ec='none', zorder=3))
    ax.text(-6.4, 11.6, 'M1 – M8 (PWM / DShot)', ha='center', va='top', fontsize=6, color='#c9d1d9', zorder=4)
    ax.annotate('', xy=(-18, -21), xytext=(18, -21), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.9))
    ax.text(0, -22.2, '36 mm  ·  30.5 mm M3 mounting', ha='center', va='top', fontsize=9, color=INK)
    ax.text(-18, 23.5, 'AERKI flight controller: top-side concept', fontsize=12, fontweight='bold', color=INK)
    ax.text(-18, 21.3, 'Concept placement for planning, not a PCB layout. Power-in pads and the Jetson 5 V '
            'output are on the back.', fontsize=7.5, color=MUTED)
    ax.set_xlim(-20, 20)
    ax.set_ylim(-25, 25)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig


def fig_power():
    modes = list(pb.JETSON_MODES_W.items())
    labels = [m.replace(' (MAXN super)', '\n(MAXN super)') for m, _ in modes]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.0), gridspec_kw=dict(width_ratios=[1.5, 1]))
    left = np.zeros(len(modes))
    parts = list(pb.AVIONICS_W.items()) + [('Jetson Orin Nano Super', None)]
    for (name, w), col in zip(parts, PALETTE):
        vals = np.array([jw if w is None else w for _, jw in modes])
        a1.barh(labels, vals, left=left, color=col, height=0.6, label=name.split(' (')[0])
        left += vals
    for i, v in enumerate(left):
        a1.text(v + 0.5, i, f'{v:.0f} W', va='center', fontsize=9, color=INK)
    a1.invert_yaxis()
    a1.set_xlabel('electrical load (W)')
    a1.set_title('Avionics load by Jetson power mode')
    a1.legend(frameon=False, fontsize=8, loc='upper center', bbox_to_anchor=(0.5, -0.17), ncol=3)
    a1.set_xlim(0, 38)
    a1.grid(axis='y', visible=False)

    base = pb.BATTERY_WH * pb.USABLE / pb.HOVER_W * 60
    mins = [pb.budget(jw)[2] for _, jw in modes]
    a2.barh(labels, mins, color='#0969da', height=0.6)
    a2.axvline(base, color=MUTED, ls='--', lw=1)
    a2.text(base + 0.06, 1.5, f'{base:.1f} min with no avionics', rotation=90, ha='left', va='center', fontsize=8, color=MUTED)
    for i, m in enumerate(mins):
        a2.text(m - 0.15, i, f'{m:.1f} min', va='center', ha='right', fontsize=9, color='white')
    a2.invert_yaxis()
    a2.set_xlim(8, 12.4)
    a2.set_xlabel('hover time (min)')
    a2.set_title('Hover time, 4S 3000 mAh, 180 W hover')
    a2.set_yticklabels([])
    a2.grid(axis='y', visible=False)
    fig.text(0.01, -0.07, 'Planning assumptions from tools/power_budget.py. The Jetson\'s mass is not included.',
             fontsize=7.5, color=MUTED)
    fig.tight_layout()
    return fig


def fig_canload():
    here = os.path.join(ROOT, '..', 'drone-can-radar', 'dsdl', 'aerki')
    radar = os.path.isdir(here)
    if radar:
        import dronecan
        dronecan.load_dsdl(here)
    rows = []
    for label, msg, hz, count in cbl.traffic(radar):
        if msg is None:
            c_frames, f_frames = [8] * 26, [64, 64, 64]
        else:
            c_frames, f_frames = cbl.frame_bytes(msg, False), cbl.frame_bytes(msg, True)
        per_s = hz * count
        lc = per_s * sum(cbl.classic_frame_bits(n) for n in c_frames) / 1e6 * 1e2
        lf = per_s * sum(cbl.fd_frame_time_us(n, 1e6, 5e6) for n in f_frames) / 1e4
        rows.append((label, lc, lf))
    rows.sort(key=lambda r: r[1])
    y = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.barh(y + 0.2, [r[1] for r in rows], height=0.38, color='#bf8700', label='classic CAN, 1 Mbit/s')
    ax.barh(y - 0.2, [r[2] for r in rows], height=0.38, color='#0969da', label='CAN FD, 1 / 5 Mbit/s')
    ax.set_yticks(y, [r[0] for r in rows], fontsize=8.5)
    ax.set_xlabel('share of bus time (%)')
    tc, tf = sum(r[1] for r in rows), sum(r[2] for r in rows)
    ax.set_title(f'DroneCAN bus load: {tc:.0f} % on classic CAN, {tf:.0f} % on CAN FD')
    ax.legend(frameon=False, loc='lower right')
    ax.grid(axis='y', visible=False)
    fig.text(0.01, -0.01, 'Frame counts from pydronecan\'s own encoder; worst-case bit stuffing, so these are upper '
             'bounds. tools/can_bus_load.py', fontsize=7.5, color=MUTED)
    fig.tight_layout()
    return fig


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, make in (('board.png', fig_board), ('power.png', fig_power), ('can-load.png', fig_canload)):
        fig = make()
        fig.savefig(os.path.join(OUT, name), dpi=160, bbox_inches='tight')
        plt.close(fig)
        print('wrote', os.path.join('docs', 'img', name))


if __name__ == '__main__':
    main()
