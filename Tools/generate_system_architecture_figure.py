"""
==============================================================================
CRIMSON ORBIT :: SYSTEM ARCHITECTURE PUBLICATION FIGURE GENERATOR
Generates a 100% crystal-clear, vector-precise, 300-DPI IEEE architecture diagram
Pure white background, professional academic colors, zero typos.
==============================================================================
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle

BASE_DIR = r"c:\FOIDS_CP"
IMAGES_DIR = os.path.join(BASE_DIR, "Assets", "Images")
os.makedirs(IMAGES_DIR, exist_ok=True)

out_png = os.path.join(IMAGES_DIR, "CrimsonOrbit_System_Architecture_Vector.png")
out_jpg = os.path.join(IMAGES_DIR, "CrimsonOrbit_System_Architecture.jpg")

print("Generating 300-DPI IEEE Academic System Architecture Diagram (White Background)...")

fig, ax = plt.subplots(figsize=(12, 6.6), dpi=300)
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#ffffff')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Font configuration
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# Helper to draw rounded box
def draw_box(ax, x, y, w, h, bg_color, border_color, border_width=1.2, radius=1.2):
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle=f"round,pad=0,rounding_size={radius}",
                          facecolor=bg_color, edgecolor=border_color,
                          linewidth=border_width, zorder=2)
    ax.add_patch(rect)
    return rect

# Helper to draw arrow
def draw_arrow(ax, x1, y1, x2, y2, color='#1e3a8a', width=1.8, style='-|>', zorder=5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=width,
                                shrinkA=2, shrinkB=2, mutation_scale=14),
                zorder=zorder)

# =============================================================================
# 1. THREE MAIN TIER CONTAINERS (White bg with subtle academic tint & borders)
# =============================================================================
# Tier 1: Left (x: 2 to 32)
draw_box(ax, 2, 4, 30, 92, '#f8fafc', '#94a3b8', border_width=1.5, radius=2)
# Tier 1 Header
draw_box(ax, 2, 88, 30, 8, '#0f172a', '#0f172a', border_width=1, radius=2)
ax.text(17, 92.5, "LAYER 1: BARE-METAL X86 KERNEL", color='#ffffff',
        fontsize=9.5, fontweight='bold', ha='center', va='center')
ax.text(17, 85.5, "16-Bit Real-Mode Hardware Control Plane", color='#334155',
        fontsize=8, fontweight='bold', fontstyle='italic', ha='center', va='center')

# Tier 2: Middle (x: 35 to 65)
draw_box(ax, 35, 4, 30, 92, '#fdfaf9', '#f87171', border_width=1.5, radius=2)
# Tier 2 Header
draw_box(ax, 35, 88, 30, 8, '#991b1b', '#991b1b', border_width=1, radius=2)
ax.text(50, 92.5, "LAYER 2: WASM INTERCEPTION BRIDGE", color='#ffffff',
        fontsize=9.5, fontweight='bold', ha='center', va='center')
ax.text(50, 85.5, "Targeted Bus-Cycle Trap & AudioWorklet", color='#7f1d1d',
        fontsize=8, fontweight='bold', fontstyle='italic', ha='center', va='center')

# Tier 3: Right (x: 68 to 98)
draw_box(ax, 68, 4, 30, 92, '#f0fdf4', '#86efac', border_width=1.5, radius=2)
# Tier 3 Header
draw_box(ax, 68, 88, 30, 8, '#14532d', '#14532d', border_width=1, radius=2)
ax.text(83, 92.5, "LAYER 3: MULTI-TIMBRAL WEB STUDIO", color='#ffffff',
        fontsize=9.5, fontweight='bold', ha='center', va='center')
ax.text(83, 85.5, "WebAudio DSP & Acoustic Resynthesis", color='#166534',
        fontsize=8, fontweight='bold', fontstyle='italic', ha='center', va='center')

# =============================================================================
# 2. LAYER 1 INTERNAL COMPONENTS
# =============================================================================
# MBR Bootloader Box
draw_box(ax, 4.5, 72, 25, 10, '#ffffff', '#cbd5e1', 1.2, 1)
ax.text(17, 78.5, "MBR Bootloader (Source/boot.asm)", color='#0f172a',
        fontsize=8.2, fontweight='bold', ha='center', va='center')
ax.text(17, 74.5, "BIOS INT 19h -> 0000:7C00h | 30 Sectors", color='#64748b',
        fontsize=7.2, ha='center', va='center')

# CPU Core & Registers
draw_box(ax, 4.5, 57, 25, 11, '#ffffff', '#cbd5e1', 1.2, 1)
ax.text(17, 64.5, "Intel 8086 CPU (1000:0000h)", color='#0f172a',
        fontsize=8.2, fontweight='bold', ha='center', va='center')
ax.text(17, 60, "AX: Divisor | BX: Freq | DX: Clock | CS/DS/SS", color='#475569',
        fontsize=7.2, fontfamily='monospace', ha='center', va='center')

# Hardware Timers & Peripheral Ports
draw_box(ax, 4.5, 41, 25, 12, '#f1f5f9', '#94a3b8', 1.2, 1)
ax.text(17, 49.5, "Intel 8253 PIT (Port 42h / 43h)", color='#0f172a',
        fontsize=8.2, fontweight='bold', ha='center', va='center')
ax.text(17, 45.5, "Channel 2 Mode 3 (Square Wave)", color='#334155', fontsize=7.2, ha='center', va='center')
ax.text(17, 42.5, "Divisor = round(1,193,180 / f)", color='#0369a1',
        fontsize=7.2, fontfamily='monospace', fontweight='bold', ha='center', va='center')

# PPI Port 61h Speaker Gate
draw_box(ax, 4.5, 26, 25, 11, '#f1f5f9', '#94a3b8', 1.2, 1)
ax.text(17, 33.5, "Intel 8255 PPI (Port 61h)", color='#0f172a',
        fontsize=8.2, fontweight='bold', ha='center', va='center')
ax.text(17, 29.5, "Bit 0: Gate 2 | Bit 1: Speaker Data", color='#334155', fontsize=7.2, ha='center', va='center')
ax.text(17, 27, "OR AL, 03h -> OUT 61h, AL", color='#0369a1',
        fontsize=7.2, fontfamily='monospace', fontweight='bold', ha='center', va='center')

# In-RAM Tape Sequencer
draw_box(ax, 4.5, 9, 25, 13, '#ffffff', '#cbd5e1', 1.2, 1)
ax.text(17, 18.5, "In-RAM Tape Buffer (composer.asm)", color='#0f172a',
        fontsize=8.2, fontweight='bold', ha='center', va='center')
ax.text(17, 14.5, "60-Note Array: dw Freq, dw Dur", color='#475569',
        fontsize=7.2, fontfamily='monospace', ha='center', va='center')
ax.text(17, 11, "Galois 16-Bit LFSR Noise (seed 0ACE1h)", color='#b91c1c',
        fontsize=7.2, fontweight='bold', ha='center', va='center')

# Internal Layer 1 Arrows
draw_arrow(ax, 17, 72, 17, 68, color='#64748b', width=1.4)
draw_arrow(ax, 17, 57, 17, 53, color='#64748b', width=1.4)
draw_arrow(ax, 17, 41, 17, 37, color='#64748b', width=1.4)
draw_arrow(ax, 17, 26, 17, 22, color='#64748b', width=1.4)

# =============================================================================
# 3. LAYER 2 INTERNAL COMPONENTS (Interception Bridge)
# =============================================================================
# Targeted Bus Trap
draw_box(ax, 37.5, 69, 25, 14, '#ffffff', '#fca5a5', 1.2, 1)
ax.text(50, 78.5, "Targeted Bus Trap (Opcode Intercept)", color='#991b1b',
        fontsize=8.2, fontweight='bold', ha='center', va='center')
ax.text(50, 74, "Traps OUT 42h & OUT 61h in 0.889 us", color='#1e293b',
        fontsize=7.5, fontweight='bold', ha='center', va='center')
ax.text(50, 71, "Zero Motherboard Emulation Tax", color='#64748b', fontsize=7.2, ha='center', va='center')

# 4-Byte Micro-Packet Protocol
draw_box(ax, 37.5, 47, 25, 18, '#fff1f2', '#f43f5e', 1.3, 1)
ax.text(50, 61, "4-Byte Micro-Packet Protocol", color='#9f1239',
        fontsize=8.5, fontweight='bold', ha='center', va='center')
# 4 Sub-blocks inside micro-packet
pkt_x = [38.5, 44.5, 50.5, 56.5]
pkt_lbl = ["CMD\n(1B)", "DIV_LO\n(1B)", "DIV_HI\n(1B)", "DUR\n(1B)"]
for px, plbl in zip(pkt_x, pkt_lbl):
    draw_box(ax, px, 50.5, 5.2, 8, '#ffffff', '#fda4af', 1, 0.6)
    ax.text(px+2.6, 54.5, plbl, color='#881337', fontsize=6.8,
            fontweight='bold', fontfamily='monospace', ha='center', va='center')

# SharedArrayBuffer Ring Buffer
draw_box(ax, 37.5, 27, 25, 15, '#ffffff', '#fca5a5', 1.2, 1)
ax.text(50, 37.5, "SharedArrayBuffer Ring Buffer", color='#991b1b',
        fontsize=8.2, fontweight='bold', ha='center', va='center')
ax.text(50, 33.5, "Lock-Free Atomic Synchronization", color='#334155', fontsize=7.2, ha='center', va='center')
ax.text(50, 29.5, "Zero-Copy Wasm-to-Audio Dispatch", color='#475569', fontsize=7.2, ha='center', va='center')

# AudioWorklet Thread & Specs
draw_box(ax, 37.5, 9, 25, 14, '#ffffff', '#fca5a5', 1.2, 1)
ax.text(50, 19, "AudioWorklet Real-Time Thread", color='#991b1b',
        fontsize=8.2, fontweight='bold', ha='center', va='center')
ax.text(50, 15, "128-Sample Processing Quanta (2.9 ms)", color='#334155', fontsize=7.2, ha='center', va='center')
ax.text(50, 11.5, "Total Latency: 11.8 ms | RAM: 12.4 MB", color='#b91c1c',
        fontsize=7.5, fontweight='bold', ha='center', va='center')

# Internal Layer 2 Arrows
draw_arrow(ax, 50, 69, 50, 65, color='#e11d48', width=1.4)
draw_arrow(ax, 50, 47, 50, 42, color='#e11d48', width=1.4)
draw_arrow(ax, 50, 27, 50, 23, color='#e11d48', width=1.4)

# =============================================================================
# 4. LAYER 3 INTERNAL COMPONENTS (Studio & Resynthesis)
# =============================================================================
# Dual-Engine Hardware Selector
draw_box(ax, 70.5, 71, 25, 12, '#ffffff', '#86efac', 1.2, 1)
ax.text(83, 79.5, "Hardware Dual-Engine Switch", color='#14532d',
        fontsize=8.2, fontweight='bold', ha='center', va='center')
ax.text(83, 75.5, "[Mode 1: Authentic 1-Bit] <--> [Mode 2: Resynth]", color='#15803d',
        fontsize=7.0, fontfamily='monospace', fontweight='bold', ha='center', va='center')
ax.text(83, 72.5, "Instant Dynamic Acoustic Mode Switch", color='#64748b', fontsize=7.0, ha='center', va='center')

# Multi-Timbral Acoustic Sound Models
draw_box(ax, 70.5, 45, 25, 22, '#f0fdf4', '#4ade80', 1.3, 1)
ax.text(83, 63, "Multi-Timbral Acoustic Engine (44.1 kHz)", color='#14532d',
        fontsize=8.2, fontweight='bold', ha='center', va='center')

# 3 Instrument badges
inst_y = [56.5, 50.5, 44.5]
inst_txt = ["Steinway Model D Concert Grand Piano",
            "Martin D-28 Acoustic Dreadnought Guitar",
            "Ludwig Super Classic Studio Drum Kit"]
inst_col = ["#065f46", "#047857", "#059669"]

for iy, itxt, icol in zip(inst_y, inst_txt, inst_col):
    draw_box(ax, 71.5, iy-2, 23, 5.2, '#ffffff', '#bbf7d0', 1, 0.8)
    ax.text(83, iy+0.6, itxt, color=icol, fontsize=7.1,
            fontweight='bold', ha='center', va='center')

# 16-Step Matrix DAW Sequencer
draw_box(ax, 70.5, 26, 25, 15, '#ffffff', '#86efac', 1.2, 1)
ax.text(83, 36.5, "16-Step DAW Matrix Sequencer", color='#14532d',
        fontsize=8.2, fontweight='bold', ha='center', va='center')
ax.text(83, 32.5, "8 Multi-Timbral Chromatic Tracks", color='#334155', fontsize=7.2, ha='center', va='center')
ax.text(83, 28.5, "Bidirectional RAM Tape Deserializer", color='#16a34a',
        fontsize=7.2, fontweight='bold', ha='center', va='center')

# FFT Spectrum Visualizer
draw_box(ax, 70.5, 9, 25, 13, '#ffffff', '#86efac', 1.2, 1)
ax.text(83, 18, "Real-Time FFT Spectrum Analyzer", color='#14532d',
        fontsize=8.2, fontweight='bold', ha='center', va='center')
ax.text(83, 14, "2048-Pt FFT @ 60 FPS | THD Telemetry", color='#334155', fontsize=7.2, ha='center', va='center')
ax.text(83, 11, "1-Bit Odd Harmonics vs. Acoustic Formants", color='#15803d',
        fontsize=7.2, fontstyle='italic', ha='center', va='center')

# Internal Layer 3 Arrows
draw_arrow(ax, 83, 71, 83, 67, color='#16a34a', width=1.4)
draw_arrow(ax, 83, 45, 83, 41, color='#16a34a', width=1.4)
draw_arrow(ax, 83, 26, 83, 22, color='#16a34a', width=1.4)

# =============================================================================
# 5. CROSS-TIER CONNECTING BUS ARROWS (Major Architectural Flow)
# =============================================================================
# Arrow 1: Layer 1 -> Layer 2 (Bus I/O writes OUT 42h, OUT 61h)
draw_arrow(ax, 29.5, 47, 37.5, 76, color='#dc2626', width=2.2, style='-|>')
ax.text(33.5, 64, "Port I/O Bus Trap\nOUT 42h, OUT 61h\n(0.889 us)", color='#b91c1c',
        fontsize=7.2, fontweight='bold', ha='center', va='center',
        bbox=dict(boxstyle="round,pad=0.25", fc="#ffffff", ec="#fca5a5", lw=1))

# Arrow 2: Layer 2 -> Layer 3 (Low-latency audio dispatch)
draw_arrow(ax, 62.5, 16, 70.5, 77, color='#059669', width=2.2, style='-|>')
ax.text(66.5, 48, "Real-Time Dispatch\nSharedArrayBuffer\n(11.8 ms Round-Trip)", color='#047857',
        fontsize=7.2, fontweight='bold', ha='center', va='center',
        bbox=dict(boxstyle="round,pad=0.25", fc="#ffffff", ec="#86efac", lw=1))

# Bidirectional sync arrow between Tape Buffer (Layer 1) and Sequencer (Layer 3)
ax.annotate('', xy=(70.5, 33), xytext=(29.5, 15),
            arrowprops=dict(arrowstyle='<|-|>', color='#2563eb', lw=1.6, ls='--',
                            shrinkA=2, shrinkB=2, mutation_scale=12),
            zorder=4)
ax.text(50, 22.5, "Bidirectional RAM Memory Synchronization (composer.asm <--> Web Sequencer)",
        color='#1d4ed8', fontsize=7.2, fontweight='bold', ha='center', va='center',
        bbox=dict(boxstyle="round,pad=0.25", fc="#eff6ff", ec="#bfdbfe", lw=1))

# =============================================================================
# 6. CAPTION & METRICS BANNER (Bottom)
# =============================================================================
ax.text(50, 1.2,
        "Figure 1: Three-Tier System Architecture of Crimson Orbit - Bare-Metal x86 Control Plane, Targeted Bus Interceptor, and Multi-Timbral Studio.",
        color='#0f172a', fontsize=8.2, fontweight='bold', ha='center', va='center')

plt.tight_layout()
fig.savefig(out_png, dpi=300, facecolor='#ffffff', edgecolor='none', bbox_inches='tight')
fig.savefig(out_jpg, dpi=300, facecolor='#ffffff', edgecolor='none', bbox_inches='tight')
plt.close(fig)

print(f"Saved Vector PNG: {out_png} ({os.path.getsize(out_png):,} bytes)")
print(f"Saved Paper JPG:  {out_jpg} ({os.path.getsize(out_jpg):,} bytes)")
