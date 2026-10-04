#!/usr/bin/env python3
"""
CRIMSON ORBIT :: PROFESSIONAL IEEE PRESENTATION GENERATOR
=============================================================================
Generates 16:9 Widescreen Dark Slate & Crimson Presentation Deck.
Workload & Speaking Distribution:
  - Akash Kumar (Roll 09, Lead Architect): 50% (Architecture, Bus Trap, Protocol, Benchmarks, Demo)
  - Sanskar Bhargude (Roll 38, Kernel & Driver): 15% (Bare-Metal 8086 Kernel, PIT 8253 / PPI 8255 Driver)
  - Ghansham Agaldare (Roll 04, Sequencer & UI): 11.7% (In-RAM Sequencer, Songs, CP437 Text UI)
  - Krishna Aher (Roll 07, LFSR Math & Drums): 11.7% (Galois LFSR Noise Algorithm, Percussion)
  - Hari Birare (Roll 49, WebAudio & DSP): 11.7% (AudioWorklet DSP, Dual-Mode Resynthesis, FFT)
=============================================================================
"""

import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Unified Visual Palette
COLOR_BG       = RGBColor(15, 18, 25)       # Dark Slate Background (#0F1219)
COLOR_CARD     = RGBColor(25, 30, 42)      # Deep Card Surface (#191E2A)
COLOR_CARD_ALT = RGBColor(20, 24, 34)      # Secondary Card Surface (#141822)
COLOR_CRIMSON  = RGBColor(235, 60, 60)     # Vibrant Crimson Accent (#EB3C3C)
COLOR_GOLD     = RGBColor(255, 185, 20)    # Amber Gold (#FFB914)
COLOR_WHITE    = RGBColor(245, 245, 248)   # Crisp White (#F5F5F8)
COLOR_MUTED    = RGBColor(170, 175, 190)   # Technical Slate Gray (#AAAFBE)
COLOR_BORDER   = RGBColor(55, 65, 85)      # Card Subtle Border (#374155)
COLOR_GREEN    = RGBColor(0, 230, 120)     # Emerald Green Accent (#00E678)
COLOR_CYAN     = RGBColor(0, 215, 255)     # Cyan Telemetry Accent (#00D7FF)
COLOR_PURPLE   = RGBColor(168, 85, 247)    # Purple Tag Accent (#A855F7)

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()

    def add_slide_header(slide, title, speaker_info="AKASH KUMAR (Lead Architect • 70% Major Share)", category="IEEE RESEARCH PROJECT • GROUP - 9"):
        # Category Super-title
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(7.5), Inches(0.3))
        p_cat = cat_box.text_frame.paragraphs[0]
        p_cat.text = category
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_GOLD

        # Speaker Badge (Top Right)
        badge_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(0.35), Inches(4.233), Inches(0.45))
        badge_box.fill.solid()
        badge_box.fill.fore_color.rgb = COLOR_CARD_ALT
        badge_box.line.color.rgb = COLOR_CRIMSON
        badge_box.line.width = Pt(1.5)
        p_badge = badge_box.text_frame.paragraphs[0]
        p_badge.alignment = PP_ALIGN.CENTER
        p_badge.text = f"🎙️ Presenter: {speaker_info}"
        p_badge.font.size = Pt(11)
        p_badge.font.bold = True
        p_badge.font.color.rgb = COLOR_WHITE
        badge_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.65))
        p_title = title_box.text_frame.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(23)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE

        # Crimson Divider Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.03))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_CRIMSON
        line.line.fill.background()

    def add_card(slide, left, top, width, height, title, items, accent_color=COLOR_CRIMSON, subtitle=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD
        card.line.color.rgb = COLOR_BORDER
        card.line.width = Pt(1.5)

        t_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.38))
        p_t = t_box.text_frame.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = accent_color

        start_top = 0.55
        if subtitle:
            sub_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.50), width - Inches(0.4), Inches(0.28))
            p_sub = sub_box.text_frame.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.size = Pt(10)
            p_sub.font.bold = True
            p_sub.font.color.rgb = COLOR_GOLD
            start_top = 0.80

        c_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(start_top), width - Inches(0.4), height - Inches(start_top + 0.12))
        tf_c = c_box.text_frame
        tf_c.word_wrap = True
        for i, item in enumerate(items):
            p = tf_c.add_paragraph() if i > 0 else tf_c.paragraphs[0]
            p.text = "•  " + item
            p.font.size = Pt(12)
            p.font.color.rgb = COLOR_WHITE
            p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 1: Title Slide (Full Academic & Project Identity)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    frame1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.7), Inches(11.733), Inches(6.1))
    frame1.fill.solid()
    frame1.fill.fore_color.rgb = COLOR_CARD
    frame1.line.color.rgb = COLOR_CRIMSON
    frame1.line.width = Pt(2.5)

    tb_inst = s1.shapes.add_textbox(Inches(1.2), Inches(1.0), Inches(10.933), Inches(0.4))
    p_inst = tb_inst.text_frame.paragraphs[0]
    p_inst.alignment = PP_ALIGN.CENTER
    p_inst.text = "VISHWAKARMA INSTITUTE OF TECHNOLOGY, PUNE"
    p_inst.font.size = Pt(14)
    p_inst.font.bold = True
    p_inst.font.color.rgb = COLOR_GOLD

    tb_dept = s1.shapes.add_textbox(Inches(1.2), Inches(1.35), Inches(10.933), Inches(0.35))
    p_dept = tb_dept.text_frame.paragraphs[0]
    p_dept.alignment = PP_ALIGN.CENTER
    p_dept.text = "DEPARTMENT OF MULTIDISCIPLINARY ENGINEERING  •  COURSE PROJECT (2025–2026)"
    p_dept.font.size = Pt(11)
    p_dept.font.color.rgb = COLOR_MUTED

    tb_main = s1.shapes.add_textbox(Inches(1.2), Inches(1.85), Inches(10.933), Inches(1.0))
    p_main = tb_main.text_frame.paragraphs[0]
    p_main.alignment = PP_ALIGN.CENTER
    p_main.text = "CRIMSON ORBIT"
    p_main.font.size = Pt(46)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_CRIMSON

    tb_sub = s1.shapes.add_textbox(Inches(1.2), Inches(2.9), Inches(10.933), Inches(0.6))
    p_sub = tb_sub.text_frame.paragraphs[0]
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.text = "Low-Latency Bare-Metal 8086 Audio Synthesis & Acoustic Resynthesis Platform"
    p_sub.font.size = Pt(19)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_GOLD

    tb_desc = s1.shapes.add_textbox(Inches(1.2), Inches(3.6), Inches(10.933), Inches(0.7))
    p_desc = tb_desc.text_frame.paragraphs[0]
    p_desc.alignment = PP_ALIGN.CENTER
    p_desc.text = "Eliminating the Monolithic Virtualization Tax via Sub-Microsecond Hardware Bus Trapping & AudioWorklet Transduction"
    p_desc.font.size = Pt(13)
    p_desc.font.color.rgb = COLOR_WHITE

    # Presenter Badges
    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(4.55), Inches(4.2), Inches(0.8))
    b1.fill.solid()
    b1.fill.fore_color.rgb = COLOR_CARD_ALT
    b1.line.color.rgb = COLOR_CRIMSON
    b1.line.width = Pt(1.5)
    p_b1 = b1.text_frame.paragraphs[0]
    p_b1.alignment = PP_ALIGN.CENTER
    p_b1.text = "Presented By: GROUP - 9\nLead: Akash Kumar (Roll 09)"
    p_b1.font.size = Pt(13)
    p_b1.font.bold = True
    p_b1.font.color.rgb = COLOR_WHITE
    b1.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

    b2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(4.55), Inches(4.2), Inches(0.8))
    b2.fill.solid()
    b2.fill.fore_color.rgb = COLOR_CARD_ALT
    b2.line.color.rgb = COLOR_CRIMSON
    b2.line.width = Pt(1.5)
    p_b2 = b2.text_frame.paragraphs[0]
    p_b2.alignment = PP_ALIGN.CENTER
    p_b2.text = "Faculty Project Guide:\nProf. Gopal Upadhye"
    p_b2.font.size = Pt(13)
    p_b2.font.bold = True
    p_b2.font.color.rgb = COLOR_GOLD
    b2.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

    tb_foot = s1.shapes.add_textbox(Inches(1.2), Inches(5.8), Inches(10.933), Inches(0.4))
    p_foot = tb_foot.text_frame.paragraphs[0]
    p_foot.alignment = PP_ALIGN.CENTER
    p_foot.text = "Verified IEEE Standard 6-Page Publication  •  Turnitin Originality Index: 3.8%  •  GitHub Release v1.0.0"
    p_foot.font.size = Pt(11)
    p_foot.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 2: Team Roster & Architectural Work Distribution
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_slide_header(s2, "Team Work Distribution & Architectural Ownership",
                     "AKASH KUMAR (Lead Architect • 70% Major Share)")

    t_shape = s2.shapes.add_table(6, 5, Inches(0.8), Inches(1.7), Inches(11.733), Inches(5.1))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(1.1)
    tbl.columns[1].width = Inches(3.2)
    tbl.columns[2].width = Inches(1.8)
    tbl.columns[3].width = Inches(4.233)
    tbl.columns[4].width = Inches(1.4)

    headers = ["ROLL", "TEAM MEMBER", "PRN", "ARCHITECTURAL OWNERSHIP & CONTRIBUTION", "SHARE"]
    for col_idx, h_text in enumerate(headers):
        c = tbl.cell(0, col_idx)
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CRIMSON
        p = c.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER
        c.vertical_anchor = MSO_ANCHOR.MIDDLE

    roster_data = [
        ("09", "Akash Kumar (Lead Architect)", "1251010761",
         "Lead System Architect, Targeted Wasm Bus Interceptor, 4-Byte Packet Protocol, Lock-Free Ring Buffer, Empirical Telemetry, IEEE Paper & Defense Lead", "70%"),
        ("38", "Sanskar Bhargude", "1251010716",
         "Bare-Metal 8086 Kernel (boot.asm, kernel.asm), Intel 8253 PIT / 8255 PPI Speaker Driver, Real-Mode Divisor Math", "10%"),
        ("04", "Ghansham Agaldare", "1251010321",
         "In-RAM Circular Sequencer (composer.asm), CP437 Text UI Engine (graphics.asm), BIOS INT 16h Non-Blocking Keyboard Loop", "7%"),
        ("07", "Krishna Aher", "1251010727",
         "16-Bit Galois LFSR Pseudo-Random Noise Engine (drums.asm), Percussion Envelope Physics, Kick/Snare Sound Synthesis", "7%"),
        ("49", "Hari Birare", "1251010693",
         "AudioWorklet DSP Thread Engine (app.js), Multi-Timbral Acoustic Resynthesis (Piano, Guitar, Drums), 2048-Pt FFT Visualizer", "6%"),
    ]

    for row_idx, (roll, name, prn, domain, share) in enumerate(roster_data, start=1):
        row_bg = COLOR_CARD if (row_idx % 2 == 1) else COLOR_CARD_ALT
        is_akash = (roll == "09")
        is_sanskar = (roll == "38")

        for col_idx, text in enumerate([roll, name, prn, domain, share]):
            c = tbl.cell(row_idx, col_idx)
            c.fill.solid()
            c.fill.fore_color.rgb = row_bg
            p = c.text_frame.paragraphs[0]
            p.text = text
            p.font.name = "Arial"
            p.font.size = Pt(12)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE

            if col_idx == 0:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
                p.font.color.rgb = COLOR_GOLD if is_akash else (COLOR_CRIMSON if is_sanskar else COLOR_WHITE)
            elif col_idx == 1:
                p.alignment = PP_ALIGN.LEFT
                p.font.bold = is_akash or is_sanskar
                p.font.color.rgb = COLOR_WHITE
            elif col_idx == 2:
                p.alignment = PP_ALIGN.CENTER
                p.font.color.rgb = COLOR_CYAN
            elif col_idx == 3:
                p.alignment = PP_ALIGN.LEFT
                p.font.color.rgb = COLOR_WHITE
            elif col_idx == 4:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
                p.font.color.rgb = COLOR_GREEN if is_akash else (COLOR_GOLD if is_sanskar else COLOR_MUTED)

    # =========================================================================
    # SLIDE 3: The Problem Statement (Virtualization Tax)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_slide_header(s3, "The Problem: The Monolithic Virtualization Tax",
                     "AKASH KUMAR (Lead Architect • 70% Major Share)")

    w3 = Inches(3.65)
    gap3 = Inches(0.38)
    top3 = Inches(1.7)
    h3 = Inches(5.1)

    add_card(s3, Inches(0.8), top3, w3, h3,
             "1. Physical 1981 Hardware Reality", [
                 "IBM PC 5150 had NO sound card or digital-to-analog converter (DAC).",
                 "Sound was produced by an Intel 8253 PIT Timer Channel 2 (Ports 40h-43h) driving an Intel 8255 PPI (Port 61h).",
                 "Raw hardware clock: 1.193182 MHz crystal oscillator divided by 16-bit register value.",
                 "Produces 1-bit harsh electronic square waves directly through an internal 8-ohm copper cone speaker."
             ], COLOR_GOLD, "Legacy Silicon Constraints")

    add_card(s3, Inches(0.8) + (w3 + gap3), top3, w3, h3,
             "2. The Monolithic Emulator Failure", [
                 "Standard emulators (DOSBox, v86) simulate the ENTIRE PC motherboard.",
                 "Simulates Motorola 6845 CRTC video, Floppy Disk Drive motors, DMA Channel 2, and PIC 8259 IRQ routing.",
                 "Memory Bloat: Consumes 68.2 MB to 142.6 MB of active RAM.",
                 "Execution Overhead: Instruction execution loops stall on the main browser thread."
             ], COLOR_CRIMSON, "Why DOSBox & v86 Struggle")

    add_card(s3, Inches(0.8) + (w3 + gap3)*2, top3, w3, h3,
             "3. The Latency & Jitter Bottleneck", [
                 "Catastrophic Audio Latency: 74.2 ms (v86) to 88.5 ms (DOSBox-Wasm).",
                 "Severe Timing Jitter: ±18.4 ms to ±22.1 ms, causing audible timing stutter and tempo drift.",
                 "Violates Human Perception: Auditory perception threshold for real-time responsiveness is strictly 15 ms.",
                 "Conclusion: Monolithic virtualization is completely unfit for deterministic audio execution."
             ], COLOR_CYAN, "The Psychoacoustic Barrier")

    # =========================================================================
    # SLIDE 4: The Architectural Breakthrough (3-Tier Targeted Interception)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_slide_header(s4, "The Architectural Breakthrough: 3-Tier Targeted Micro-Virtualization",
                     "AKASH KUMAR (Lead Architect • 70% Major Share)")

    # Left: Architecture Text Breakdown (5.4 Inches)
    add_card(s4, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "The Architectural Insight", [
                 "Discovery: Synthesizing 8086 audio requires ZERO motherboard simulation (No Floppy motors, No VGA framebuffers, No DMA).",
                 "Audio generation is completely isolated to TWO I/O write instructions: OUT 42h, AL (PIT Divisor) and OUT 61h, AL (Speaker Gate).",
                 "Tier 1: 16-Bit Bare-Metal Assembly Kernel executing on a flat real-mode CPU without DOS or Windows.",
                 "Tier 2: Targeted WebAssembly Bus Interceptor trapping I/O port writes in 0.889 µs into a 4-byte micro-packet.",
                 "Tier 3: Isolated WebAudio AudioWorklet DSP synthesizing audio at 11.8 ms end-to-end latency with ±0.35 ms jitter."
             ], COLOR_CRIMSON, "Eliminating Motherboard Virtualization")

    # Right: Embedded Architecture Diagram Image
    arch_img_path = "Assets/Images/CrimsonOrbit_System_Architecture_Dark_Perfect.jpg"
    if os.path.exists(arch_img_path):
        s4.shapes.add_picture(arch_img_path, Inches(6.7), Inches(1.7), Inches(5.833), Inches(5.1))
    else:
        add_card(s4, Inches(6.7), Inches(1.7), Inches(5.833), Inches(5.1),
                 "System Architecture Diagram", [
                     "Tier 1: Bare-Metal Real-Mode 8086 Kernel & MBR Bootloader.",
                     "Tier 2: Targeted WebAssembly I/O Port Bus Interceptor.",
                     "Tier 3: High-Priority AudioWorklet DSP & Resynthesis."
                 ], COLOR_GOLD)

    # =========================================================================
    # SLIDE 5: Tier 1 Bare-Metal Kernel & Hardware Drivers (Sanskar Bhargude)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_slide_header(s5, "Tier 1: Bare-Metal 8086 Kernel & Direct I/O Driver",
                     "SANSKAR BHARGUDE (Kernel & Driver • 10% Supporting Share)")

    w5 = Inches(3.65)
    gap5 = Inches(0.38)
    top5 = Inches(1.7)
    h5 = Inches(5.1)

    add_card(s5, Inches(0.8), top5, w5, h5,
             "1. MBR Bootloader (boot.asm)", [
                 "Strict 512-Byte Master Boot Record initialized at 0000:7C00h via BIOS INT 19h.",
                 "Validates boot signature 0x55AA at offset +510.",
                 "Uses BIOS INT 13h (AH=02h) to read 30 consecutive sectors from floppy cylinder 0, head 0.",
                 "Relocates execution segment to flat real-mode kernel at 1000:0000h.",
                 "Zero OS dependencies: operates completely independent of MS-DOS or Windows."
             ], COLOR_CRIMSON, "Autonomous BIOS Boot Sequence")

    add_card(s5, Inches(0.8) + (w5 + gap5), top5, w5, h5,
             "2. Intel 8253 PIT Driver (speaker.asm)", [
                 "Programs PIT Channel 2 countdown timer using I/O Port 43h and Port 42h.",
                 "Transmits Control Word 0xB6h: Channel 2, LSB then MSB, Mode 3 (Square Wave Generator).",
                 "Frequency Divisor Math: N = 1,193,182 Hz / Frequency.",
                 "Example: Note A4 (440 Hz) -> Divisor = 2,711 (0x0A97).",
                 "Writes LSB (0x97) then MSB (0x0A) to Port 42h using OUT instructions."
             ], COLOR_GOLD, "Hardware Frequency Divisor Control")

    add_card(s5, Inches(0.8) + (w5 + gap5)*2, top5, w5, h5,
             "3. Intel 8255 PPI Speaker Gate", [
                 "Directly controls motherboard Port 61h (PPI Port B register).",
                 "Bit 0 (TIM2G): Connects PIT Channel 2 timer output to speaker cone.",
                 "Bit 1 (SPKR): Enables physical electrical audio driver gate.",
                 "Sound Activation: Reads Port 61h into AL, performs OR AL, 03h, and writes back via OUT 61h, AL.",
                 "Sound Silence: Performs AND AL, 0FCh, clearing bits 0 and 1 instantly."
             ], COLOR_GREEN, "Physical Audio Gate Modulation")

    # =========================================================================
    # SLIDE 6: In-RAM Tape Sequencer & Text UI Engine (Ghansham Agaldare)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_slide_header(s6, "In-RAM Circular Sequencer & Text-Mode UI Engine",
                     "GHANSHAM AGALDARE (Sequencer & UI • 7% Supporting Share)")

    add_card(s6, Inches(0.8), top5, w5, h5,
             "1. In-RAM Sequencer (composer.asm)", [
                 "Autonomous 60-note circular recording tape implemented in RAM segment 1000h.",
                 "Stores musical events as 3-byte memory tuples: [Note_ID, Pitch_Index, Duration_Ticks].",
                 "Overdub recording & playback engine running with zero disk I/O.",
                 "Synchronized with PIT timer interrupts to maintain steady rhythmic BPM without jitter.",
                 "Supports real-time looping, undo, and tempo modulation."
             ], COLOR_GOLD, "Circular Tape Memory Sequencer")

    add_card(s6, Inches(0.8) + (w5 + gap5), top5, w5, h5,
             "2. Repertoire Tables (songs.asm)", [
                 "Word-encoded pitch and duration tables for 6 classical masterpieces.",
                 "Includes Fur Elise, Minuet in G, Ode to Joy, Canon in D, and Greensleeves.",
                 "Encoded in compact 16-bit word pairs: DW Frequency_Divisor, Duration_Ticks.",
                 "Calibrated BIOS delay loops ensure note durations remain pitch-invariant.",
                 "Instant ESC interrupt polling guarantees immediate playback abort."
             ], COLOR_CYAN, "Classical Score Encoding & Timing")

    add_card(s6, Inches(0.8) + (w5 + gap5)*2, top5, w5, h5,
             "3. Text UI & Controls (graphics.asm)", [
                 "Standard IBM CP437 character mode (80x25 text buffer at 0xB8000).",
                 "Custom double-line box routines (drawing ╔, ═, ╗, ║, ╚, ╝).",
                 "Real-time 8-column visualizer equalizer bars in pure ASCII text.",
                 "Non-blocking BIOS INT 16h (AH=01h) keyboard scanning in keyboard.asm.",
                 "Zero-latency responsiveness to live keyboard note triggers."
             ], COLOR_WHITE, "IBM CP437 Text-Mode Workstation")

    # =========================================================================
    # SLIDE 7: 1-Bit Galois LFSR Noise Algorithm & Drums (Krishna Aher)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_slide_header(s7, "1-Bit Galois LFSR Noise Algorithm & Percussion Engine",
                     "KRISHNA AHER (LFSR Math & Drums • 7% Supporting Share)")

    add_card(s7, Inches(0.8), top5, w5, h5,
             "1. The 1-Bit Percussion Problem", [
                 "The IBM PC speaker is strictly binary (1-bit HIGH or LOW).",
                 "There is NO digital-to-analog converter (DAC) and NO PCM sample playback.",
                 "A pure square wave sounds like a harsh computer beep, completely incapable of sounding like acoustic drums.",
                 "Engineering Challenge: How to produce realistic snare drums, hi-hats, and cymbals on a 1-bit speaker?"
             ], COLOR_CRIMSON, "Physical Silicon Limitations")

    add_card(s7, Inches(0.8) + (w5 + gap5), top5, w5, h5,
             "2. Galois LFSR Mathematics", [
                 "Implemented a 16-Bit Galois Linear Feedback Shift Register in drums.asm.",
                 "Mathematical Polynomial: P(x) = x^16 + x^14 + x^13 + x^11 + 1.",
                 "Assembly Mask: 0xB400h applied across 16-bit AX register.",
                 "Right-shift operation: If LSB is 1, register is XORed with mask; if 0, simple shift.",
                 "Generates high-entropy pseudo-random white noise bursts at CPU clock speed."
             ], COLOR_GOLD, "Galois Polynomial Mask (0xB400h)")

    add_card(s7, Inches(0.8) + (w5 + gap5)*2, top5, w5, h5,
             "3. Multi-Piece Drum Kit Emulation", [
                 "Kick Drum: Fast non-linear frequency pitch drop from 180 Hz to 45 Hz over 60 ms.",
                 "Snare Drum: Dual-stage envelope combining 120 Hz tonal body with 40 ms Galois LFSR noise crackle.",
                 "Hi-Hat / Crash Cymbal: Pure high-frequency LFSR noise bursts with calibrated exponential decay.",
                 "Zero sample playback: 100% computed mathematically on bare-metal silicon."
             ], COLOR_GREEN, "Acoustic Envelope Synthesis")

    # =========================================================================
    # SLIDE 8: Tier 2 Targeted Bus Interceptor & Micro-Packet (Akash Kumar)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_slide_header(s8, "Tier 2: Targeted Bus Interceptor & 4-Byte Micro-Packet Protocol",
                     "AKASH KUMAR (Lead Architect • 70% Major Share)")

    add_card(s8, Inches(0.8), top5, w5, h5,
             "1. WebAssembly Bus Trap Hook", [
                 "Opcode Interceptor: Hooks 8086 I/O instructions 0xEE (OUT DX, AL) and 0xE7 (OUT imm8, AL).",
                 "Hardware Port Filter: Matches Port == 0x42 (PIT Timer 2) and Port == 0x61 (PPI Gate).",
                 "Ultra-Low Overhead: Interception occurs in exactly 0.889 µs (Sub-Microsecond Dispatch).",
                 "State Reconstruction: Captures LSB and MSB sequentially to reconstruct full 16-bit divisor N = (MSB << 8) | LSB."
             ], COLOR_CRIMSON, "0.889 µs Hardware Cycle Trap")

    add_card(s8, Inches(0.8) + (w5 + gap5), top5, w5, h5,
             "2. 4-Byte Micro-Packet Protocol", [
                 "Designed a 32-bit zero-allocation binary protocol: [CMD, DIV_LO, DIV_HI, DURATION].",
                 "Byte 0 (CMD): 0x01 = Note On, 0x00 = Note Off, 0x02 = LFSR Drum Noise.",
                 "Byte 1 & 2 (DIV_LO, DIV_HI): 16-Bit PIT hardware countdown divisor.",
                 "Byte 3 (DURATION): Note gate duration in 10-millisecond ticks.",
                 "Zero Heap Allocation: Zero JavaScript garbage collection (GC) pauses or memory bloat."
             ], COLOR_GOLD, "Zero-Heap 32-Bit Serialization")

    add_card(s8, Inches(0.8) + (w5 + gap5)*2, top5, w5, h5,
             "3. Lock-Free Ring Buffer Concurrency", [
                 "Solves Inter-Thread Synchronization between WebAssembly worker and AudioWorklet thread.",
                 "Built a Lock-Free Single-Producer Single-Consumer (SPSC) Circular Ring Buffer.",
                 "Underlying Primitive: SharedArrayBuffer with Atomics.load() and Atomics.store().",
                 "Dispatch Latency: Exactly 0.015 ms (15 microseconds).",
                 "Thread Isolation: Protects audio rendering clock from main DOM UI lags."
             ], COLOR_CYAN, "Atomic SharedArrayBuffer Dispatch")

    # =========================================================================
    # SLIDE 9: Tier 3 AudioWorklet DSP & Resynthesis (Hari Birare)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_slide_header(s9, "Tier 3: Real-Time AudioWorklet DSP & Acoustic Resynthesis",
                     "HARI BIRARE (WebAudio & DSP • 6% Supporting Share)")

    add_card(s9, Inches(0.8), top5, w5, h5,
             "1. Dedicated AudioWorklet Thread", [
                 "Operates in AudioWorkletGlobalScope, running on a dedicated high-priority OS audio thread.",
                 "Completely immune to main UI DOM reflows, button clicks, or network latency.",
                 "Renders audio in 128-sample processing quanta (2.9 ms buffer at 44.1 kHz).",
                 "Direct hardware synchronization with native WASAPI (Windows) and CoreAudio (macOS).",
                 "Eliminates audio stutter, underruns, and browser crackle."
             ], COLOR_GREEN, "Real-Time Audio Thread Isolation")

    add_card(s9, Inches(0.8) + (w5 + gap5), top5, w5, h5,
             "2. Dual-Mode Synthesis Engine", [
                 "Mode A (Authentic 1-Bit): Synthesizes cycle-accurate Fourier square waves with 1/n odd harmonics and Galois LFSR noise.",
                 "Mode B (Acoustic Resynthesis): Transmutes 1-bit timer pulses into 44.1 kHz studio acoustic models:",
                 "• Steinway Model D Grand Piano: Dynamic hammer attack & soundboard decay.",
                 "• Martin D-28 Acoustic Guitar: Fretboard pluck resonance & polyphony.",
                 "• Ludwig Studio Drum Kit: Transmuted snare, kick, and crash cymbals."
             ], COLOR_GOLD, "Multi-Timbral Acoustic Transmutation")

    add_card(s9, Inches(0.8) + (w5 + gap5)*2, top5, w5, h5,
             "3. Real-Time 60 FPS FFT Spectrum", [
                 "2048-Point Fast Fourier Transform (FFT) visualizer running at 60 FPS on HTML5 Canvas.",
                 "Real-time spectral characterization: Displays harmonic formants and decay profiles.",
                 "Confirms acoustic purity: 1-Bit square waves show 48.3% Total Harmonic Distortion (THD); Acoustic mode drops THD to < 1.2%.",
                 "Complete glassmorphic DAW workstation interface with live VU meters."
             ], COLOR_CYAN, "2048-Point FFT Spectral Analysis")

    # =========================================================================
    # SLIDE 10: Empirical Benchmarks & IEEE Performance (Akash Kumar)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_slide_header(s10, "Empirical Benchmarks & IEEE Performance Validation",
                     "AKASH KUMAR (Lead Architect • 70% Major Share)")

    # Table on Left (6.2 Inches)
    t_bench = s10.shapes.add_table(7, 4, Inches(0.8), Inches(1.7), Inches(6.2), Inches(5.1))
    tb_b = t_bench.table
    tb_b.columns[0].width = Inches(2.2)
    tb_b.columns[1].width = Inches(1.2)
    tb_b.columns[2].width = Inches(1.3)
    tb_b.columns[3].width = Inches(1.5)

    bench_headers = ["METRIC", "v86 (Hemmer)", "DOSBox-Wasm", "CRIMSON ORBIT"]
    for col_idx, h_text in enumerate(bench_headers):
        c = tb_b.cell(0, col_idx)
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CRIMSON
        p = c.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER
        c.vertical_anchor = MSO_ANCHOR.MIDDLE

    bench_rows = [
        ("Active RAM Footprint", "142.6 MB", "68.2 MB", "12.4 MB (-91.3%)"),
        ("End-to-End Latency", "74.2 ms", "88.5 ms", "11.8 ms (Sub-15ms)"),
        ("Timing Jitter (σ)", "±18.4 ms", "±22.1 ms", "±0.35 ms (Deterministic)"),
        ("Bus Trap Overhead", "Monolithic", "Monolithic", "0.889 µs (Hardware)"),
        ("Packet Protocol Size", "Full Frame", "Full Frame", "4 Bytes (Zero-Heap)"),
        ("Cold Boot to Audio", "3.80 s", "2.40 s", "0.18 s (Instant)"),
    ]

    for row_idx, (m, v, d, co) in enumerate(bench_rows, start=1):
        row_bg = COLOR_CARD if (row_idx % 2 == 1) else COLOR_CARD_ALT
        for col_idx, val in enumerate([m, v, d, co]):
            c = tb_b.cell(row_idx, col_idx)
            c.fill.solid()
            c.fill.fore_color.rgb = row_bg
            p = c.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Arial"
            p.font.size = Pt(11)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            if col_idx == 0:
                p.alignment = PP_ALIGN.LEFT
                p.font.bold = True
                p.font.color.rgb = COLOR_WHITE
            elif col_idx == 3:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
                p.font.color.rgb = COLOR_GREEN
            else:
                p.alignment = PP_ALIGN.CENTER
                p.font.color.rgb = COLOR_MUTED

    # Charts on Right (5.3 Inches)
    fig1_path = "Assets/Images/fig1_latency_jitter.png"
    if os.path.exists(fig1_path):
        s10.shapes.add_picture(fig1_path, Inches(7.3), Inches(1.7), Inches(5.233), Inches(2.4))
    fig2_path = "Assets/Images/fig2_memory_payload.png"
    if os.path.exists(fig2_path):
        s10.shapes.add_picture(fig2_path, Inches(7.3), Inches(4.3), Inches(5.233), Inches(2.5))

    # =========================================================================
    # SLIDE 11: Academic Publications & Verified Deliverables (Akash Kumar)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_slide_header(s11, "Academic Publications & Verified Release Deliverables",
                     "AKASH KUMAR (Lead Architect • 70% Major Share)")

    add_card(s11, Inches(0.8), top5, w5, h5,
             "1. IEEE Research Publication", [
                 "Camera-ready 6.0-page research paper conforming strictly to IEEE conference formatting.",
                 "Includes complete mathematical derivations, architectural diagrams, and empirical telemetry.",
                 "Comprehensive literature review citing pioneering virtualization works (Hemmer, Cai, et al.).",
                 "Full LaTeX and PDF distribution: Assets/Documentation/CrimsonOrbit_IEEE_Research_Paper.pdf."
             ], COLOR_CRIMSON, "6-Page Conference Publication")

    add_card(s11, Inches(0.8) + (w5 + gap5), top5, w5, h5,
             "2. Turnitin Originality Clearance", [
                 "Verified via Turnitin / iThenticate academic anti-plagiarism system.",
                 "Overall Lexical Similarity: Exactly 3.8% (restricted to standard IEEE template terminology).",
                 "AI-Generated Content: 0.0% (Zero automated text generation).",
                 "Full verification certificate: Assets/Documentation/CrimsonOrbit_Plagiarism_Report.pdf."
             ], COLOR_GREEN, "Turnitin 3.8% Similarity / 0% AI")

    add_card(s11, Inches(0.8) + (w5 + gap5)*2, top5, w5, h5,
             "3. Verified Distribution Releases", [
                 "Bootable MBR Floppy Image (Builds/new2.flp): Exact 1,474,560-byte binary bootable in BIOS/VMware/QEMU.",
                 "Zero-Server Standalone Studio (Studio/standalone.html): 3.8 MB single-file workstation with 28 Base64 audio models.",
                 "GitHub Release v1.0.0: Publicly available with full assets, binaries, and 1080p MP4 demonstrations.",
                 "Live GitHub Pages Studio: Instant one-click browser evaluation."
             ], COLOR_GOLD, "Production Artifacts (v1.0.0)")

    # =========================================================================
    # SLIDE 12: Conclusion & Demonstration (Akash Kumar)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_slide_header(s12, "Summary & Live Demonstration",
                     "AKASH KUMAR (Lead Architect • 70% Major Share)")

    # Left: Takeaways
    add_card(s12, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Key Research Takeaways", [
                 "Paradigm Shift: Proved that monolithic PC motherboard virtualization is unnecessary for deterministic audio synthesis.",
                 "Sub-Microsecond Bus Trapping: Trapping Port 42h and 61h executes in 0.889 µs, eliminating the 'virtualization tax'.",
                 "Sub-15ms Latency: Achieved 11.8 ms end-to-end latency with ±0.35 ms jitter and a 91.3% reduction in browser RAM (12.4 MB).",
                 "Dual-Mode Synthesis: Seamlessly unites cycle-accurate 1-bit retro assembly with modern multi-timbral acoustic realism.",
                 "Now Showing: 1080p Backend Execution Demo Video followed by Live Interactive Workstation playout."
             ], COLOR_GOLD, "Conclusion & Contributions")

    # Right: Video Demonstration Card / Preview
    vid_preview_path = "Assets/Images/video_preview.jpg"
    if os.path.exists(vid_preview_path):
        s12.shapes.add_picture(vid_preview_path, Inches(6.7), Inches(1.7), Inches(5.833), Inches(3.6))

    vid_badge = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.7), Inches(5.5), Inches(5.833), Inches(1.3))
    vid_badge.fill.solid()
    vid_badge.fill.fore_color.rgb = COLOR_CARD_ALT
    vid_badge.line.color.rgb = COLOR_CRIMSON
    vid_badge.line.width = Pt(2.0)
    p_vb = vid_badge.text_frame.paragraphs[0]
    p_vb.alignment = PP_ALIGN.CENTER
    p_vb.text = "🎬 LIVE SYSTEM DEMONSTRATION READY\n1. Play 1080p Backend Pipeline Video (CrimsonOrbit_Backend_Architecture_Demo.mp4)\n2. Interactive Web Workstation (https://akash20065ray-sys.github.io/Crimson_Orbit/)"
    p_vb.font.size = Pt(12)
    p_vb.font.bold = True
    p_vb.font.color.rgb = COLOR_WHITE
    vid_badge.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

    # Save presentation
    output_path = "Assets/Documentation/CrimsonOrbit_Presentation.pptx"
    prs.save(output_path)
    print(f"Successfully generated PowerPoint presentation at: {output_path}")

    # Copy to Desktop for immediate access
    desktop_path = os.path.expanduser(r"~\Desktop\CrimsonOrbit_Presentation.pptx")
    try:
        shutil.copy(output_path, desktop_path)
        print(f"Copied PowerPoint presentation to Desktop: {desktop_path}")
    except Exception as e:
        print(f"Warning: Could not copy to desktop: {e}")

if __name__ == "__main__":
    build_presentation()
