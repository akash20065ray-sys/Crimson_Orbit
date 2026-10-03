"""
==============================================================================
CRIMSON ORBIT :: SEQUENTIAL PIPELINE WALKTHROUGH VIDEO GENERATOR
Generates a 1080p 30-FPS cinematic sequential walkthrough video showing:
Scene 1: Introduction & Architectural Problem (0.0s - 4.5s)
Scene 2: Tier 1 - 16-Bit Bare-Metal 8086 Engine (4.5s - 9.5s)
Scene 3: Tier 2 - Targeted Bus Interception & 4-Byte Packet (9.5s - 14.5s)
Scene 4: Tier 3 - AudioWorklet DSP & Acoustic Resynthesis (14.5s - 19.5s)
Scene 5: Empirical Benchmarks & Academic Telemetry (19.5s - 24.0s)
==============================================================================
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import shutil

WIDTH = 1920
HEIGHT = 1080
FPS = 30
TOTAL_FRAMES = 720  # 24 seconds total

BASE_DIR = r"c:\FOIDS_CP"
VIDEOS_DIR = os.path.join(BASE_DIR, "Assets", "Videos")
os.makedirs(VIDEOS_DIR, exist_ok=True)

output_mp4 = os.path.join(VIDEOS_DIR, "CrimsonOrbit_Sequential_Pipeline_Walkthrough.mp4")
desktop_mp4 = r"C:\Users\akash\Desktop\CrimsonOrbit_Sequential_Pipeline_Walkthrough.mp4"
downloads_mp4 = r"C:\Users\akash\Downloads\CrimsonOrbit_Sequential_Pipeline_Walkthrough.mp4"

# Load standard Windows fonts
try:
    font_hero = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 52)
    font_title = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 40)
    font_subtitle = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 24)
    font_section = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 32)
    font_mono_xl = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 32)
    font_mono_lg = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 26)
    font_mono = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 21)
    font_mono_sm = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 17)
    font_body = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 22)
    font_bold = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)
    font_byte_title = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 20)
    font_byte_val = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 19)
    font_small = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 18)
except Exception:
    font_hero = font_title = font_subtitle = font_section = font_mono_xl = font_mono_lg = font_mono = font_mono_sm = font_body = font_bold = font_byte_title = font_byte_val = font_small = ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_header_and_progress(draw, current_scene_idx, t):
    # Persistent Top Navigation Bar
    draw_rounded_rect(draw, [50, 25, WIDTH - 50, 105], 12, fill=(18, 24, 38), outline=(37, 48, 72), width=2)
    draw.text((75, 42), "CRIMSON ORBIT :: PIPELINE", font=font_title, fill=(248, 113, 113))

    # Stepper Tabs
    scenes = [
        ("1. ARCHITECTURE", (251, 113, 133)),
        ("2. TIER 1: 8086 KERNEL", (244, 63, 94)),
        ("3. TIER 2: BUS TRAP", (245, 158, 11)),
        ("4. TIER 3: AUDIOWORKLET", (16, 185, 129)),
        ("5. BENCHMARKS", (56, 189, 248))
    ]
    tab_w = 205
    start_tab_x = WIDTH - 1130
    for idx, (sname, scolor) in enumerate(scenes):
        tx = start_tab_x + idx * (tab_w + 10)
        is_active = (idx == current_scene_idx)
        bg_col = (30, 41, 59) if is_active else (15, 23, 42)
        border_col = scolor if is_active else (51, 65, 85)
        text_col = (255, 255, 255) if is_active else (100, 116, 139)
        draw_rounded_rect(draw, [tx, 40, tx + tab_w, 90], 6, fill=bg_col, outline=border_col, width=2 if is_active else 1)
        
        # Center tab text
        tb = draw.textbbox((0, 0), sname, font=font_small)
        tw = tb[2] - tb[0]
        draw.text((tx + (tab_w - tw) // 2, 54), sname, font=font_small, fill=text_col)

    # Bottom Progress Bar
    p_pct = min(1.0, max(0.0, t / 24.0))
    draw_rounded_rect(draw, [50, HEIGHT - 35, WIDTH - 50, HEIGHT - 20], 6, fill=(23, 31, 48), outline=(51, 65, 85))
    fill_w = int((WIDTH - 100) * p_pct)
    if fill_w > 12:
        draw_rounded_rect(draw, [50, HEIGHT - 35, 50 + fill_w, HEIGHT - 20], 6, fill=(239, 68, 68))

def render_scene_1(draw, t):
    # Scene 1: Introduction & Architectural Problem (0.0s - 4.5s)
    draw.text((80, 145), "Eliminating the 'Virtualization Tax' of Monolithic Emulators", font=font_hero, fill=(255, 255, 255))
    draw.text((80, 215), "Targeted Bus-Cycle Interception bridges 16-Bit Bare-Metal Assembly to WebAudio DSP", font=font_subtitle, fill=(148, 163, 184))

    # Left Box: The Problem (Traditional Emulators)
    draw_rounded_rect(draw, [80, 275, 930, 980], 14, fill=(16, 22, 34), outline=(239, 68, 68), width=2)
    draw.text((115, 305), "THE PROBLEM: MONOLITHIC VIRTUALIZATION", font=font_section, fill=(239, 68, 68))
    draw.text((115, 350), "Examples: v86 (Hemmer et al.), DOSBox-Wasm (Cai et al.)", font=font_body, fill=(148, 163, 184))

    prob_items = [
        ("Simulates Full Motherboard:", "Floppy motors, IDE controllers, DMA, VGA."),
        ("Contiguous Memory Bloat:", "Over 140 MB RAM to run a 15 KB assembly kernel."),
        ("Audio Latency Lag (88 ms):", "Sound generation is quantized to 60 FPS video loops."),
        ("Timing Jitter (±22 ms):", "Browser GC pauses cause music to stutter and drift.")
    ]
    y_p = 410
    for ptitle, pdesc in prob_items:
        draw_rounded_rect(draw, [115, y_p, 895, y_p + 105], 8, fill=(23, 31, 48), outline=(51, 65, 85))
        draw.text((135, y_p + 18), "❌ " + ptitle, font=font_bold, fill=(248, 113, 113))
        draw.text((135, y_p + 58), pdesc, font=font_body, fill=(203, 213, 225))
        y_p += 135

    # Right Box: The Crimson Orbit Solution
    draw_rounded_rect(draw, [990, 275, WIDTH - 80, 980], 14, fill=(16, 22, 34), outline=(16, 185, 129), width=2)
    draw.text((1025, 305), "THE SOLUTION: TARGETED MICRO-INTERCEPTION", font=font_section, fill=(52, 211, 153))
    draw.text((1025, 350), "Architectural Innovation: Control-Plane vs Synthesis-Plane Split", font=font_body, fill=(148, 163, 184))

    sol_items = [
        ("Targeted Bus Trapping (0.889 µs):", "Traps ONLY I/O writes to Port 42h & 61h."),
        ("Ultra-Low Memory (12.4 MB):", "91.3% RAM reduction by discarding simulated video/drives."),
        ("Sub-15ms Latency (11.8 ms):", "Pipes 4-byte micro-packets directly into AudioWorklet."),
        ("Sub-Perceptual Jitter (±0.35 ms):", "Lock-free SharedArrayBuffer ring buffer immune to GC.")
    ]
    y_s = 410
    for stitle, sdesc in sol_items:
        draw_rounded_rect(draw, [1025, y_s, WIDTH - 115, y_s + 105], 8, fill=(23, 31, 48), outline=(51, 65, 85))
        draw.text((1045, y_s + 18), "✅ " + stitle, font=font_bold, fill=(52, 211, 153))
        draw.text((1045, y_s + 58), sdesc, font=font_body, fill=(203, 213, 225))
        y_s += 135

def render_scene_2(draw, t):
    # Scene 2: Tier 1 - 16-Bit Bare-Metal 8086 Engine (4.5s - 9.5s)
    local_t = t - 4.5
    cycle_idx = int(local_t * 2) % 4
    notes = ["A4 (440 Hz)", "C5 (523 Hz)", "E5 (659 Hz)", "G5 (784 Hz)"]
    divisors = [2711, 2281, 1810, 1522]
    hex_divs = ["0A97h", "08E9h", "0712h", "05F2h"]

    cur_n = notes[cycle_idx]
    cur_d = divisors[cycle_idx]
    cur_h = hex_divs[cycle_idx]

    draw.text((80, 135), "TIER 1: 16-BIT BARE-METAL 8086 ASSEMBLY ENGINE", font=font_hero, fill=(244, 63, 94))
    draw.text((80, 200), "Autonomous Real-Mode MBR Kernel executing without operating system or DOS interrupts", font=font_subtitle, fill=(148, 163, 184))

    # Left Column: Disassembly & Port Programming
    draw_rounded_rect(draw, [80, 255, 1080, 980], 14, fill=(16, 22, 34), outline=(244, 63, 94), width=2)
    draw.text((115, 280), "ACTIVE CODE: Source/speaker.asm (PIT 8253 / PPI 61h Driver)", font=font_section, fill=(251, 113, 133))

    code_lines = [
        ("; 1. Calculate PIT Timer 2 countdown divisor from target frequency", False),
        ("mov dx, 0012h       ; High word of 1,193,180 Hz", False),
        ("mov ax, 34DCh       ; Low word of 1,193,180 Hz", False),
        (f"div bx              ; Divisor = 1,193,180 / BX -> AX={cur_h} ({cur_d})", True),
        ("", False),
        ("; 2. Initialize PIT Timer 2 for Square Wave mode", False),
        ("mov al, 0B6h        ; Channel 2, Mode 3 (Square Wave), LSB/MSB", False),
        ("out 43h, al         ; Send Control Word to PIT Command Register", False),
        ("", False),
        ("; 3. Send 16-bit divisor to Port 42h (LSB then MSB)", False),
        (f"mov al, {cur_h[2:4]}h         ; Divisor Low Byte (LSB)", False),
        (f"out 42h, al         ; >> WRITE TO PORT 42h (Captured by Bus Trap) >>", True),
        (f"mov al, {cur_h[:2]}h         ; Divisor High Byte (MSB)", False),
        (f"out 42h, al         ; >> WRITE TO PORT 42h (Captured by Bus Trap) >>", True),
        ("", False),
        ("; 4. Assert Port 61h Bits 0 & 1 to gate the speaker cone", False),
        ("in  al, 61h         ; Read current PPI Port B register", False),
        ("or  al, 03h         ; Set Bit 0 (Gate 2) and Bit 1 (Speaker Data)", True),
        ("out 61h, al         ; >> WRITE TO PORT 61h (Speaker Vibrates) >>", True)
    ]
    y_c = 330
    for cl, is_hi in code_lines:
        col = (250, 204, 21) if is_hi else ((100, 116, 139) if cl.startswith(";") else (226, 232, 240))
        draw.text((115, y_c), cl, font=font_mono, fill=col)
        y_c += 32

    # Right Column: CPU State, Memory Segmentation & Floppy Deliverable
    draw_rounded_rect(draw, [1120, 255, WIDTH - 80, 980], 14, fill=(16, 22, 34), outline=(56, 189, 248), width=2)
    draw.text((1155, 280), "HARDWARE STATE & REGISTERS", font=font_section, fill=(56, 189, 248))

    # CPU Register Grid
    reg_rows = [
        ("AX (Accumulator)", cur_h, f"Divisor = {cur_d}"),
        ("BX (Base / Freq)", f"{int(1193180/cur_d):04d}", f"Pitch = {cur_n}"),
        ("CX (Count / Dur)", "012Ch", "Step Duration = 300 ms"),
        ("DX (High Product)", "0012h", "Crystal Base = 1,193,180 Hz")
    ]
    y_r = 340
    for rname, rval, rdesc in reg_rows:
        draw_rounded_rect(draw, [1155, y_r, WIDTH - 115, y_r + 75], 8, fill=(23, 31, 48), outline=(51, 65, 85))
        draw.text((1175, y_r + 14), rname, font=font_bold, fill=(148, 163, 184))
        draw.text((1175, y_r + 42), f"VALUE: {rval}", font=font_mono, fill=(56, 189, 248))
        draw.text((1380, y_r + 42), f"({rdesc})", font=font_body, fill=(52, 211, 153))
        y_r += 95

    # Memory Layout Card
    draw_rounded_rect(draw, [1155, y_r + 20, WIDTH - 115, 950], 8, fill=(10, 14, 22), outline=(51, 65, 85))
    draw.text((1175, y_r + 38), "MEMORY SEGMENTATION MODEL (Builds/new2.flp):", font=font_bold, fill=(244, 63, 94))
    draw.text((1175, y_r + 72), "• 0000:7C00h - 0000:7DFFh: 512-Byte MBR Bootloader", font=font_mono_sm, fill=(226, 232, 240))
    draw.text((1175, y_r + 102), "• 1000:0000h - 1000:3ABFh: Autonomous Flat Assembly Kernel", font=font_mono_sm, fill=(226, 232, 240))
    draw.text((1175, y_r + 132), "• 1000:2000h - 1000:23FFh: In-RAM Tape Sequencer (composer.asm)", font=font_mono_sm, fill=(226, 232, 240))
    draw.text((1175, y_r + 162), "• Exact Floppy Disk Size: 1,474,560 Bytes (Verified Standard)", font=font_mono_sm, fill=(52, 211, 153))

def render_scene_3(draw, t):
    # Scene 3: Tier 2 - Targeted Bus Interception & 4-Byte Packet (9.5s - 14.5s)
    local_t = t - 9.5
    cycle_idx = int(local_t * 2) % 4
    divisors = [2711, 2281, 1810, 1522]
    hex_divs = ["0A97h", "08E9h", "0712h", "05F2h"]
    cur_d = divisors[cycle_idx]
    cur_h = hex_divs[cycle_idx]
    div_lsb = cur_h[2:4]
    div_msb = cur_h[:2]

    draw.text((80, 135), "TIER 2: TARGETED WEBASSEMBLY BUS INTERCEPTOR", font=font_hero, fill=(245, 158, 11))
    draw.text((80, 200), "Microsecond bus trapping (0.889 µs) and 4-byte hardware micro-packet serialization", font=font_subtitle, fill=(148, 163, 184))

    # Top Section: Bus Cycle Interception Mechanism
    draw_rounded_rect(draw, [80, 255, WIDTH - 80, 480], 14, fill=(16, 22, 34), outline=(245, 158, 11), width=2)
    draw.text((115, 280), "BUS-CYCLE INSTRUCTION TRAP (Opcodes 0xEE, 0xE7, 0xEF)", font=font_section, fill=(251, 191, 36))
    
    trap_bullets = [
        f"• Machine Cycle Hook: Sits directly on CPU execution loop; checks if I/O port address == 0x42 (PIT) or 0x61 (PPI).",
        f"• Microsecond Dispatch: Mean interception execution time = 0.889 µs (Measured via nanosecond hardware clocks).",
        f"• State Capture: Latches Divisor LSB (0x{div_lsb}) and MSB (0x{div_msb}) -> Reconstructs Divisor: (0x{div_msb} << 8) | 0x{div_lsb} = {cur_d}.",
        f"• Frequency Synthesis Formula: f = 1,193,180 / {cur_d} = {int(1193180/cur_d)} Hz (Mathematically Cycle-Accurate)."
    ]
    y_tb = 330
    for tb_text in trap_bullets:
        draw.text((115, y_tb), tb_text, font=font_body, fill=(226, 232, 240))
        y_tb += 34

    # Middle Section: 4-Byte Micro-Packet Architecture (BIG, BOLD, CENTERED CARDS)
    draw_rounded_rect(draw, [80, 510, WIDTH - 80, 750], 14, fill=(10, 14, 22), outline=(56, 189, 248), width=2)
    draw.text((115, 535), "IMMUTABLE 4-BYTE HARDWARE MICRO-PACKET SPECIFICATION (32 BITS TOTAL):", font=font_section, fill=(56, 189, 248))

    cards = [
        ("BYTE 0: COMMAND", "0x01 (NOTE_ON)", "Opcode: Tone Active", (239, 68, 68)),
        ("BYTE 1: DIV_LO", f"0x{div_lsb} (LSB)", f"Divisor Low: {int(div_lsb, 16)}", (245, 158, 11)),
        ("BYTE 2: DIV_HI", f"0x{div_msb} (MSB)", f"Divisor High: {int(div_msb, 16)}", (59, 130, 246)),
        ("BYTE 3: DURATION", "0x02 (300 ms)", "Quantized Step Code", (16, 185, 129))
    ]
    card_w = 410
    card_h = 135
    start_cx = 115
    for idx, (ctitle, cval, cdesc, ccolor) in enumerate(cards):
        cx = start_cx + idx * (card_w + 14)
        cy = 585
        draw_rounded_rect(draw, [cx, cy, cx + card_w, cy + card_h], 8, fill=(18, 24, 38), outline=ccolor, width=2)
        
        # Center Title
        tb = draw.textbbox((0, 0), ctitle, font=font_byte_title)
        draw.text((cx + (card_w - (tb[2] - tb[0])) // 2, cy + 18), ctitle, font=font_byte_title, fill=ccolor)
        
        # Center Value
        vb = draw.textbbox((0, 0), cval, font=font_mono_xl)
        draw.text((cx + (card_w - (vb[2] - vb[0])) // 2, cy + 54), cval, font=font_mono_xl, fill=(255, 255, 255))
        
        # Center Desc
        db = draw.textbbox((0, 0), cdesc, font=font_small)
        draw.text((cx + (card_w - (db[2] - db[0])) // 2, cy + 98), cdesc, font=font_small, fill=(148, 163, 184))

    # Bottom Section: Lock-Free SharedArrayBuffer Ring Buffer
    draw_rounded_rect(draw, [80, 780, WIDTH - 80, 980], 14, fill=(16, 22, 34), outline=(16, 185, 129), width=2)
    draw.text((115, 805), "LOCK-FREE CIRCULAR RING BUFFER (SharedArrayBuffer)", font=font_section, fill=(52, 211, 153))
    
    rb_bullets = [
        "• True Multithreaded Concurrency: Wasm execution thread posts 4-byte packets into SharedArrayBuffer with zero heap memory allocation.",
        "• Thread Synchronization: Governed by atomic primitives (Atomics.wait() & Atomics.notify()) with sub-microsecond response time.",
        "• 100% Garbage Collection Immunity: Zero object allocations in the audio dispatch loop eliminates browser frame drops."
    ]
    y_rb = 855
    for rb_t in rb_bullets:
        draw.text((115, y_rb), rb_t, font=font_body, fill=(226, 232, 240))
        y_rb += 34

def render_scene_4(draw, t):
    # Scene 4: Tier 3 - AudioWorklet DSP & Acoustic Resynthesis (14.5s - 19.5s)
    local_t = t - 14.5
    is_mode_b = (int(local_t) % 4) >= 2
    cur_freq = 440 if not is_mode_b else 523

    draw.text((80, 135), "TIER 3: AUDIOWORKLET DSP & ACOUSTIC RESYNTHESIS", font=font_hero, fill=(52, 211, 153))
    draw.text((80, 200), "Dedicated real-time audio thread executing at 44.1 kHz, completely isolated from DOM & UI event loops", font=font_subtitle, fill=(148, 163, 184))

    # Left Column: Dual Synthesis Modes
    draw_rounded_rect(draw, [80, 255, 930, 980], 14, fill=(16, 22, 34), outline=(52, 211, 153), width=2)
    draw.text((115, 280), "DUAL-ENGINE RESYNTHESIS ARCHITECTURE", font=font_section, fill=(52, 211, 153))

    # Mode A Card
    is_a_active = not is_mode_b
    border_a = (248, 113, 113) if is_a_active else (51, 65, 85)
    bg_a = (28, 20, 28) if is_a_active else (23, 31, 48)
    draw_rounded_rect(draw, [115, 330, 895, 600], 10, fill=bg_a, outline=border_a, width=2 if is_a_active else 1)
    draw.text((140, 350), "MODE A: AUTHENTIC 1-BIT RETRO PC (RAW 8086)", font=font_bold, fill=(248, 113, 113))
    draw.text((140, 390), "• Zero Audio Samples / Zero SoundFonts loaded.", font=font_body, fill=(226, 232, 240))
    draw.text((140, 425), "• Pure Fourier Odd-Harmonic Square Wave (1/n distribution).", font=font_body, fill=(226, 232, 240))
    draw.text((140, 460), "• 16-Bit Galois LFSR Noise: P(x) = x^16 + x^14 + x^13 + x^11 + 1.", font=font_body, fill=(226, 232, 240))
    draw.text((140, 495), "• Replicates exact physical buzzer of the original IBM 5150.", font=font_body, fill=(148, 163, 184))
    draw.text((140, 545), "STATUS: " + ("ACTIVE (Pure Math Waveform)" if is_a_active else "Standby"), font=font_bold, fill=(52, 211, 153) if is_a_active else (100, 116, 139))

    # Mode B Card
    is_b_active = is_mode_b
    border_b = (56, 189, 248) if is_b_active else (51, 65, 85)
    bg_b = (18, 30, 45) if is_b_active else (23, 31, 48)
    draw_rounded_rect(draw, [115, 630, 895, 940], 10, fill=bg_b, outline=border_b, width=2 if is_b_active else 1)
    draw.text((140, 650), "MODE B: MULTI-TIMBRAL ACOUSTIC RESYNTHESIS", font=font_bold, fill=(56, 189, 248))
    draw.text((140, 690), "• Steinway Model D Concert Grand Piano (Hammer noise & decay).", font=font_body, fill=(226, 232, 240))
    draw.text((140, 725), "• Martin D-28 Acoustic Dreadnought Guitar (Plucked resonance).", font=font_body, fill=(226, 232, 240))
    draw.text((140, 760), "• Ludwig Super Classic Drum Kit (Transmuted LFSR bursts).", font=font_body, fill=(226, 232, 240))
    draw.text((140, 795), "• 28 Studio-Recorded 44.1 kHz PCM Acoustic Sample Banks.", font=font_body, fill=(148, 163, 184))
    draw.text((140, 885), "STATUS: " + ("ACTIVE (Acoustic Transduction)" if is_b_active else "Standby"), font=font_bold, fill=(52, 211, 153) if is_b_active else (100, 116, 139))

    # Right Column: Oscilloscope & 24-Band FFT Spectrum Visualizer
    draw_rounded_rect(draw, [960, 255, WIDTH - 80, 980], 14, fill=(16, 22, 34), outline=(56, 189, 248), width=2)
    draw.text((995, 280), "REAL-TIME DSP OSCILLOSCOPE & FFT SPECTRUM", font=font_section, fill=(56, 189, 248))

    # Oscilloscope Display Window
    draw_rounded_rect(draw, [995, 330, WIDTH - 115, 570], 10, fill=(10, 14, 22), outline=(51, 65, 85))
    draw.text((1020, 348), f"TIME-DOMAIN WAVEFORM ({('Acoustic Piano Decay' if is_mode_b else '1-Bit TTL Square Wave')})", font=font_bold, fill=(52, 211, 153) if is_mode_b else (248, 113, 113))

    wave_pts = []
    w_start_x = 1020
    w_end_x = WIDTH - 140
    w_center_y = 460
    phase = local_t * cur_freq * 0.08
    
    for px in range(w_start_x, w_end_x, 3):
        rel_x = (px - w_start_x) / 35.0
        if is_mode_b:
            val = np.sin(rel_x * 2.0 + phase) * 0.65 + np.sin(rel_x * 4.0 + phase) * 0.25 + np.sin(rel_x * 6.0 + phase) * 0.15
        else:
            val = 0.85 if (np.sin(rel_x * 2.0 + phase) > 0) else -0.85
        py = int(w_center_y - val * 65)
        wave_pts.append((px, py))
    
    if len(wave_pts) > 1:
        wave_col = (56, 189, 248) if is_mode_b else (248, 113, 113)
        draw.line(wave_pts, fill=wave_col, width=3)

    # 24-Band FFT Spectrum Analyzer
    draw_rounded_rect(draw, [995, 600, WIDTH - 115, 940], 10, fill=(10, 14, 22), outline=(51, 65, 85))
    draw.text((1020, 618), "2048-POINT FFT SPECTRUM ANALYZER (60 FPS)", font=font_bold, fill=(251, 191, 36))

    num_bars = 24
    bar_w = 26
    bar_gap = 7
    bx_start = 1025
    by_bottom = 910
    max_h = 240

    for bi in range(num_bars):
        b_phase = (local_t * 6.0) + (bi * 0.35)
        if is_mode_b:
            decay = np.exp(-bi * 0.14)
            h = int((np.sin(b_phase) * 0.35 + 0.65) * max_h * decay)
        else:
            if bi % 2 == 0:
                h = int((max_h / (bi + 1)) * (np.sin(b_phase) * 0.2 + 0.8))
            else:
                h = int(max_h * 0.05)
        h = max(10, min(max_h, h))
        
        bx1 = bx_start + bi * (bar_w + bar_gap)
        by1 = by_bottom - h
        bx2 = bx1 + bar_w
        by2 = by_bottom
        
        r_c = int(248 - bi * 6)
        g_c = int(113 + bi * 6)
        b_c = int(113 + bi * 6)
        draw_rounded_rect(draw, [bx1, by1, bx2, by2], 4, fill=(r_c, g_c, b_c))

def render_scene_5(draw, t):
    # Scene 5: Empirical Benchmarks & Academic Telemetry (19.5s - 24.0s)
    draw.text((80, 135), "EMPIRICAL BENCHMARKS & VERIFIED TELEMETRY", font=font_hero, fill=(56, 189, 248))
    draw.text((80, 200), "Averaged across 1,000 continuous bus-trapping iterations tested against monolithic emulators", font=font_subtitle, fill=(148, 163, 184))

    # 4 Giant Metric Hero Cards
    cards_data = [
        ("END-TO-END AUDIO LATENCY", "11.8 ms", "6.3x Lower than DOSBox (88.5 ms)", "PASS: Sub-15ms Perceptual Limit", (52, 211, 153)),
        ("ACTIVE MEMORY FOOTPRINT", "12.4 MB", "91.3% Lower than v86 (142.6 MB)", "PASS: Near-Zero Memory Tax", (56, 189, 248)),
        ("BUS TRAP SERIALIZATION", "0.889 µs", "Sub-Microsecond Port 42h Intercept", "PASS: Cycle-Accurate Capture", (251, 191, 36)),
        ("DISPATCH TIMING JITTER", "±0.35 ms", "vs ±22.1 ms in DOSBox-Wasm", "PASS: Sub-Perceptual Precision", (244, 63, 94))
    ]
    card_w = (WIDTH - 160 - 45) // 4
    for idx, (mtitle, mval, msub1, msub2, mcol) in enumerate(cards_data):
        cx = 80 + idx * (card_w + 15)
        draw_rounded_rect(draw, [cx, 260, cx + card_w, 540], 12, fill=(16, 22, 34), outline=mcol, width=2)
        draw.text((cx + 20, 285), mtitle, font=font_bold, fill=(148, 163, 184))
        draw.text((cx + 20, 335), mval, font=font_hero, fill=mcol)
        draw.text((cx + 20, 430), msub1, font=font_body, fill=(203, 213, 225))
        draw.text((cx + 20, 480), "• " + msub2, font=font_bold, fill=mcol)

    # Bottom Deliverables Grid
    draw_rounded_rect(draw, [80, 580, WIDTH - 80, 980], 14, fill=(16, 22, 34), outline=(37, 48, 72), width=2)
    draw.text((115, 605), "OFFICIAL RESEARCH ARTIFACTS & DELIVERABLES", font=font_section, fill=(255, 255, 255))

    deliv_items = [
        ("• IEEE Conference Paper:", "6-Page Camera-Ready IEEE Manuscript with complete architectural figures and benchmarks."),
        ("• Turnitin Clearance Report:", "Certified 3.8% lexical similarity, 0.0% AI text, officially verified academic originality."),
        ("• Bootable Floppy Image:", "Exact 1,474,560-byte binary (Builds/new2.flp) ready for BIOS, VMware, or QEMU."),
        ("• Web Audio Studio:", "Live on GitHub Pages (https://akash20065ray-sys.github.io/Crimson_Orbit/) zero setup."),
        ("• Group 9 Authors:", "Krishna Aher, Sanskar Bhargude, Ghansham Agaldare, Hari Birare, Akash Kumar (VIT Pune).")
    ]
    y_d = 660
    for dtitle, ddesc in deliv_items:
        draw_rounded_rect(draw, [115, y_d, WIDTH - 115, y_d + 50], 6, fill=(23, 31, 48), outline=(51, 65, 85))
        draw.text((135, y_d + 13), dtitle, font=font_bold, fill=(248, 113, 113))
        draw.text((470, y_d + 13), ddesc, font=font_body, fill=(226, 232, 240))
        y_d += 60

def render_frame(frame_idx):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(11, 15, 23))
    draw = ImageDraw.Draw(img)

    t = frame_idx / FPS  # Current time (0.0 to 24.0)

    # Scene boundaries:
    # Scene 1: 0.0s - 4.5s  (Frames 0 - 134)
    # Scene 2: 4.5s - 9.5s  (Frames 135 - 284)
    # Scene 3: 9.5s - 14.5s (Frames 285 - 434)
    # Scene 4: 14.5s - 19.5s (Frames 435 - 584)
    # Scene 5: 19.5s - 24.0s (Frames 585 - 719)
    if t < 4.5:
        scene_idx = 0
        draw_header_and_progress(draw, scene_idx, t)
        render_scene_1(draw, t)
    elif t < 9.5:
        scene_idx = 1
        draw_header_and_progress(draw, scene_idx, t)
        render_scene_2(draw, t)
    elif t < 14.5:
        scene_idx = 2
        draw_header_and_progress(draw, scene_idx, t)
        render_scene_3(draw, t)
    elif t < 19.5:
        scene_idx = 3
        draw_header_and_progress(draw, scene_idx, t)
        render_scene_4(draw, t)
    else:
        scene_idx = 4
        draw_header_and_progress(draw, scene_idx, t)
        render_scene_5(draw, t)

    frame_rgb = np.array(img)
    return cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

def generate_video():
    print(f"Initializing Sequential VideoWriter: {WIDTH}x{HEIGHT} @ {FPS} FPS...")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_mp4, fourcc, float(FPS), (WIDTH, HEIGHT))

    print(f"Rendering {TOTAL_FRAMES} frames ({TOTAL_FRAMES // FPS} seconds across 5 scenes)...")
    for f in range(TOTAL_FRAMES):
        frame = render_frame(f)
        out.write(frame)
        if f % 120 == 0 or f == TOTAL_FRAMES - 1:
            print(f"  Rendered Frame {f + 1} / {TOTAL_FRAMES} ({(f + 1) / TOTAL_FRAMES * 100:.1f}%)")

    out.release()
    file_size = os.path.getsize(output_mp4)
    print(f"\n[Sequential Video Generated Successfully!]")
    print(f"  Target File: {output_mp4} ({file_size:,} bytes)")

    # Copy to Desktop and Downloads
    try:
        shutil.copy2(output_mp4, desktop_mp4)
        print(f"  Desktop Copy: {desktop_mp4}")
    except Exception as e:
        print(f"  Desktop Warning: {e}")

    try:
        shutil.copy2(output_mp4, downloads_mp4)
        print(f"  Downloads Copy: {downloads_mp4}")
    except Exception as e:
        print(f"  Downloads Warning: {e}")

if __name__ == "__main__":
    generate_video()
