#!/usr/bin/env python3
"""
CRIMSON ORBIT – MUSICAL BAND & REAL SOUND STUDIO
Final Unified Presentation Generator (generate_presentation.py)
Theme:
- Full Presentation in unified Crimson Orbit Dark Slate & Crimson Theme across ALL slides.
- Slide 1: Vishwakarma Institute of Technology, Pune • Crimson Orbit Musical Band • Group - 9 • Prof. Gopal Upadhye.
- Slide 2: TEAM MEMBERS table with Roll No, Name, and PRN styled in Dark Slate, Crimson Header & Gold Accents.
- Slides 3-12: Simple, clean content with zero student names on headers/body, emu8086 focus, and workflow.
"""

import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Unified Theme Colors
COLOR_BG = RGBColor(15, 18, 25)           # Dark Slate Background
COLOR_CARD = RGBColor(25, 30, 42)         # Clean Card Background
COLOR_CARD_ALT = RGBColor(20, 24, 34)     # Alternating Card Background
COLOR_CRIMSON = RGBColor(235, 60, 60)     # Bright Crimson
COLOR_GOLD = RGBColor(255, 185, 20)       # Amber Gold
COLOR_WHITE = RGBColor(245, 245, 248)     # Bright White Text
COLOR_MUTED = RGBColor(170, 175, 190)     # Light Gray Text
COLOR_BORDER = RGBColor(70, 30, 42)       # Card Border
COLOR_GREEN = RGBColor(0, 230, 120)       # Friendly Green Accent
COLOR_CYAN = RGBColor(0, 215, 255)        # Friendly Blue Accent

def create_presentation_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()

    def add_header(slide, title, category="MICROPROCESSOR PROJECT • GROUP - 9"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
        p_cat = cat_box.text_frame.paragraphs[0]
        p_cat.text = category
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_GOLD

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.65))
        p_title = title_box.text_frame.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(25)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE

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

        t_box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.18), width - Inches(0.5), Inches(0.4))
        p_t = t_box.text_frame.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(17)
        p_t.font.bold = True
        p_t.font.color.rgb = accent_color

        start_top = 0.62
        if subtitle:
            sub_box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.55), width - Inches(0.5), Inches(0.3))
            p_sub = sub_box.text_frame.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = COLOR_MUTED
            start_top = 0.85

        c_box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(start_top), width - Inches(0.5), height - Inches(start_top + 0.15))
        tf_c = c_box.text_frame
        tf_c.word_wrap = True
        for i, item in enumerate(items):
            p = tf_c.add_paragraph() if i > 0 else tf_c.paragraphs[0]
            p.text = "•  " + item
            p.font.size = Pt(13)
            p.font.color.rgb = COLOR_WHITE
            p.space_after = Pt(7)

    # ==========================================================================
    # SLIDE 1: Title Slide (In Our Unified Theme)
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    # Main Frame Card
    frame1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.8), Inches(11.333), Inches(5.9))
    frame1.fill.solid()
    frame1.fill.fore_color.rgb = COLOR_CARD
    frame1.line.color.rgb = COLOR_CRIMSON
    frame1.line.width = Pt(2.5)

    # College Name
    tb_inst = s1.shapes.add_textbox(Inches(1.5), Inches(1.15), Inches(10.333), Inches(0.45))
    p_inst = tb_inst.text_frame.paragraphs[0]
    p_inst.alignment = PP_ALIGN.CENTER
    p_inst.text = "VISHWAKARMA INSTITUTE OF TECHNOLOGY, PUNE"
    p_inst.font.size = Pt(14)
    p_inst.font.bold = True
    p_inst.font.color.rgb = COLOR_GOLD

    # Project Title
    tb_main = s1.shapes.add_textbox(Inches(1.5), Inches(1.65), Inches(10.333), Inches(1.1))
    p_main = tb_main.text_frame.paragraphs[0]
    p_main.alignment = PP_ALIGN.CENTER
    p_main.text = "CRIMSON ORBIT"
    p_main.font.size = Pt(48)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_CRIMSON

    # Subtitle
    tb_sub = s1.shapes.add_textbox(Inches(1.5), Inches(2.75), Inches(10.333), Inches(0.7))
    p_sub = tb_sub.text_frame.paragraphs[0]
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.text = "MUSICAL BAND"
    p_sub.font.size = Pt(26)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_GOLD

    # Description
    tb_desc = s1.shapes.add_textbox(Inches(1.5), Inches(3.55), Inches(10.333), Inches(0.7))
    p_desc = tb_desc.text_frame.paragraphs[0]
    p_desc.alignment = PP_ALIGN.CENTER
    p_desc.text = "A Complete Musical Band Built in 8086 Assembly Language"
    p_desc.font.size = Pt(16)
    p_desc.font.color.rgb = COLOR_WHITE

    # Badges / Details: Group - 9 and Guide
    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), Inches(4.5), Inches(3.9), Inches(0.75))
    b1.fill.solid()
    b1.fill.fore_color.rgb = COLOR_CARD_ALT
    b1.line.color.rgb = COLOR_CRIMSON
    b1.line.width = Pt(1.5)
    p_b1 = b1.text_frame.paragraphs[0]
    p_b1.alignment = PP_ALIGN.CENTER
    p_b1.text = "Presented By: GROUP - 9"
    p_b1.font.size = Pt(15)
    p_b1.font.bold = True
    p_b1.font.color.rgb = COLOR_WHITE
    b1.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

    b2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(4.5), Inches(3.9), Inches(0.75))
    b2.fill.solid()
    b2.fill.fore_color.rgb = COLOR_CARD_ALT
    b2.line.color.rgb = COLOR_CRIMSON
    b2.line.width = Pt(1.5)
    p_b2 = b2.text_frame.paragraphs[0]
    p_b2.alignment = PP_ALIGN.CENTER
    p_b2.text = "Guide: Prof. Gopal Upadhye"
    p_b2.font.size = Pt(15)
    p_b2.font.bold = True
    p_b2.font.color.rgb = COLOR_GOLD
    b2.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

    # Footer Metadata
    tb_foot = s1.shapes.add_textbox(Inches(1.5), Inches(5.65), Inches(10.333), Inches(0.5))
    p_foot = tb_foot.text_frame.paragraphs[0]
    p_foot.alignment = PP_ALIGN.CENTER
    p_foot.text = "07/09/2026   •   Primary Platform: emu8086   •   Audio Extension: HTML/CSS/JS Studio"
    p_foot.font.size = Pt(11)
    p_foot.font.color.rgb = COLOR_MUTED

    # ==========================================================================
    # SLIDE 2: Team Members Table Slide (In Our Unified Theme)
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "TEAM MEMBERS", "VISHWAKARMA INSTITUTE OF TECHNOLOGY, PUNE • GROUP - 9")

    # Table Data from Image
    team_rows = [
        ("4", "Agaldare Ghansham Dilip", "1251010321"),
        ("7", "Aher Krishna Gorakh", "1251010727"),
        ("9", "Akash Kumar", "1251010761"),
        ("38", "Bhargude Sanskar Sandip", "1251010716"),
        ("49", "Hari Ratnakar Birare", "1251010693"),
    ]

    t_left = Inches(1.4)
    t_top = Inches(1.8)
    t_width = Inches(10.533)
    t_height = Inches(4.8)

    t_shape = s2.shapes.add_table(6, 3, t_left, t_top, t_width, t_height)
    tbl = t_shape.table
    tbl.columns[0].width = Inches(2.2)
    tbl.columns[1].width = Inches(5.5)
    tbl.columns[2].width = Inches(2.833)

    headers = ["ROLL NO.", "NAME", "PRN"]
    for col_idx, h_text in enumerate(headers):
        c = tbl.cell(0, col_idx)
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CRIMSON
        p = c.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER
        c.vertical_anchor = MSO_ANCHOR.MIDDLE

    for row_idx, (roll, name, prn) in enumerate(team_rows, start=1):
        row_bg = COLOR_CARD if (row_idx % 2 == 1) else COLOR_CARD_ALT

        # Cell 0: Roll No
        c0 = tbl.cell(row_idx, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = row_bg
        p0 = c0.text_frame.paragraphs[0]
        p0.text = roll
        p0.font.name = "Arial"
        p0.font.size = Pt(15)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_GOLD
        p0.alignment = PP_ALIGN.CENTER
        c0.vertical_anchor = MSO_ANCHOR.MIDDLE

        # Cell 1: Name
        c1 = tbl.cell(row_idx, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = row_bg
        p1 = c1.text_frame.paragraphs[0]
        p1.text = name
        p1.font.name = "Arial"
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_WHITE
        p1.alignment = PP_ALIGN.LEFT
        c1.vertical_anchor = MSO_ANCHOR.MIDDLE

        # Cell 2: PRN
        c2 = tbl.cell(row_idx, 2)
        c2.fill.solid()
        c2.fill.fore_color.rgb = row_bg
        p2 = c2.text_frame.paragraphs[0]
        p2.text = prn
        p2.font.name = "Arial"
        p2.font.size = Pt(15)
        p2.font.bold = False
        p2.font.color.rgb = COLOR_CYAN
        p2.alignment = PP_ALIGN.CENTER
        c2.vertical_anchor = MSO_ANCHOR.MIDDLE

    # ==========================================================================
    # SLIDE 3: Project Workflow (How We Planned & Built It)
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "Project Workflow — How We Planned & Built It")

    w4 = Inches(2.75)
    gap4 = Inches(0.2)
    top_wf = Inches(1.6)
    h_wf = Inches(5.3)

    add_card(s3, Inches(0.8), top_wf, w4, h_wf,
             "Step 1: Idea & Research", [
                 "Wanted to make an interactive musical project instead of a simple calculator.",
                 "Researched computer PC speaker sound in emu8086: confirmed it can play sound frequencies through computer speakers.",
                 "Identified key limitation: the PC speaker in emu8086 only makes electronic beeps, not realistic instruments.",
                 "Project Strategy: Build BOTH the assembly code in emu8086 AND a realistic studio in HTML/CSS/JS."
             ], COLOR_CRIMSON, "Concept & Discovery")

    add_card(s3, Inches(0.8) + (w4 + gap4), top_wf, w4, h_wf,
             "Step 2: Coding in emu8086", [
                 "Wrote the entire assembly code directly for emu8086 emulator.",
                 "Divided the band into independent modules:",
                 "• Concert Piano keys and sustain logic.",
                 "• 6-string Guitar tuning and strumming.",
                 "• Drum kit white noise and percussion.",
                 "• Classical songs repertoire and timing loops.",
                 "Tested everything using emu8086 'Emulate' and 'Run'."
             ], COLOR_GOLD, "Modular Assembly Development")

    add_card(s3, Inches(0.8) + (w4 + gap4)*2, top_wf, w4, h_wf,
             "Step 3: Finding Real Sounds", [
                 "Searched online for genuine studio-recorded instrument sound archives.",
                 "Sourced 28 authentic audio files:",
                 "• Real Steinway Grand Piano notes.",
                 "• Real Martin Acoustic Guitar strings & chords.",
                 "• Real Ludwig Studio Drums (Kick, Snare, Hi-Hat, Crash).",
                 "Saved all sounds cleanly inside our project."
             ], COLOR_CYAN, "Online Sound Sourcing")

    add_card(s3, Inches(0.8) + (w4 + gap4)*3, top_wf, w4, h_wf,
             "Step 4: Assembling & Web Studio", [
                 "Built the web studio interface using HTML, CSS, and JavaScript to play the real sounds.",
                 "Connected the same keys and songs from emu8086 to the real sound studio.",
                 "Added moving animations: keys press down, guitar strings vibrate, and drum pads show shockwaves.",
                 "Assembled all files together for final presentation."
             ], COLOR_GREEN, "Final Assembling & Web Studio")

    # ==========================================================================
    # SLIDE 4: System Architecture (3-Tier Layered Architecture)
    # ==========================================================================
    s_arch = prs.slides.add_slide(blank_layout)
    set_bg(s_arch)
    add_header(s_arch, "System Architecture — 3-Tier Layered Design")

    w_arch = Inches(3.7)
    gap_arch = Inches(0.3)
    top_arch = Inches(1.6)
    h_arch = Inches(5.3)

    # Layer 1: Input Layer
    add_card(s_arch, Inches(0.8), top_arch, w_arch, h_arch,
             "1. Input & Controls Layer", [
                 "Keyboard Inputs: Q..I (Piano), Q..Y & [S] (Guitar), Q, W, E, R, T (Drums), 1..4 (Menu).",
                 "BIOS Keyboard Interrupt (INT 16h): Reads key scan codes non-destructively in emu8086.",
                 "Instant Stop [ESC]: Non-blocking keyboard polling halts playback and silences audio immediately.",
                 "Web Event Listeners: JavaScript keydown and mouse click events mirror the exact same controls."
             ], COLOR_CYAN, "User Actions & Keyboard Detection")

    # Vector Arrow 1 -> 2
    arr1 = s_arch.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.52), Inches(3.9), Inches(0.24), Inches(0.36))
    arr1.fill.solid()
    arr1.fill.fore_color.rgb = COLOR_GOLD
    arr1.line.fill.background()

    # Layer 2: Processing Engine
    add_card(s_arch, Inches(4.8), top_arch, w_arch, h_arch,
             "2. emu8086 Assembly Engine", [
                 "Kernel Controller (kernel.asm): Coordinates module switching, memory segments, and screen views.",
                 "Piano Module (piano.asm): Note frequency math, octave register shifting, and sustain pedal logic.",
                 "Guitar Module (guitar.asm): Plectrum chirp transients, singing vibrato, and chord sweeps.",
                 "Drums Module (drums.asm): 8086 random white noise generator and kick drum frequency drops.",
                 "Songs Sequencer (songs.asm): Word-encoded note tables and calibrated BIOS timer delay loops."
             ], COLOR_CRIMSON, "Core 16-Bit Processing (kernel.asm)")

    # Vector Arrow 2 -> 3
    arr2 = s_arch.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(8.52), Inches(3.9), Inches(0.24), Inches(0.36))
    arr2.fill.solid()
    arr2.fill.fore_color.rgb = COLOR_GOLD
    arr2.line.fill.background()

    # Layer 3: Dual Output Engine
    add_card(s_arch, Inches(8.8), top_arch, w_arch, h_arch,
             "3. Dual Output Audio Engine", [
                 "Output A (emu8086 PC Speaker): Direct port output produces 1-bit timer sound through computer speakers.",
                 "Output B (Web Audio Studio): Maps identical note data to 28 real studio recordings (Steinway, Martin, Ludwig).",
                 "Zero-Latency Buffering: Pre-decoded AudioBuffers allow instant response on key press.",
                 "Dual Visualizers: 8-channel text equalizer in emu8086 + 60 FPS dynamic Canvas spectrum analyzer in Web Studio."
             ], COLOR_GOLD, "Hardware Speaker & Studio Sound")

    # ==========================================================================
    # SLIDE 5: Module Work Division (No student names - purely role-based)
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Module Work Division — Core Responsibilities")

    w_card = Inches(2.2)
    gap = Inches(0.18)
    top_pos = Inches(1.6)
    h_card = Inches(5.3)

    add_card(s4, Inches(0.8), top_pos, w_card, h_card,
             "1. CONCERT PIANO", [
                 "Project Conception & Architecture Research.",
                 "Researched how emu8086 plays sound through PC speaker.",
                 "Built the Piano module in emu8086 (3D keys, sustain pedal).",
                 "Integrated real Steinway piano sound to Web Studio.",
                 "Assembled the full project and created the final build files."
             ], COLOR_CRIMSON, "Piano & Project Lead")

    add_card(s4, Inches(0.8) + (w_card + gap), top_pos, w_card, h_card,
             "2. ACOUSTIC GUITAR", [
                 "Acoustic Guitar specialist module.",
                 "Built Guitar module in emu8086 (guitar.asm).",
                 "Coded 6 strings from Low E to High E.",
                 "Added guitar vibrato and chord strumming on key [S].",
                 "Created the guitar fretboard and Martin acoustic plucks in Web Studio."
             ], COLOR_GOLD, "Guitar (emu8086 & Web)")

    add_card(s4, Inches(0.8) + (w_card + gap)*2, top_pos, w_card, h_card,
             "3. STUDIO DRUMS", [
                 "Drums & Percussion specialist module.",
                 "Built Drum Kit in emu8086 (drums.asm).",
                 "Created white noise in assembly for snare and crash cymbals.",
                 "Coded 5 drum sounds (Kick, Snare, Hi-Hat, Tom, Crash).",
                 "Built the 3D drum kit stage with shockwave effects in Web Studio."
             ], COLOR_CRIMSON, "Drums (emu8086 & Web)")

    add_card(s4, Inches(0.8) + (w_card + gap)*3, top_pos, w_card, h_card,
             "4. MUSIC REPERTOIRE", [
                 "Songs & Music data specialist module.",
                 "Built Song Repertoire in emu8086 (songs.asm).",
                 "Stored musical notes and delay timing for 6 famous songs.",
                 "Synchronized tempo so songs play at steady speed.",
                 "Mapped the same song notes into Web Studio so they sound real."
             ], COLOR_GOLD, "Songs Data & Timing")

    add_card(s4, Inches(0.8) + (w_card + gap)*4, top_pos, w_card, h_card,
             "5. JUKEBOX PLAYER", [
                 "Song Player & Visualizer specialist module.",
                 "Built the Jukebox player that plays songs automatically in emu8086.",
                 "Added 8 animated equalizer bars on screen.",
                 "Added [ESC] button support to stop song anytime.",
                 "Created the colorful live sound visualizer in Web Studio."
             ], COLOR_GREEN, "Jukebox Player & Visualizer")

    # ==========================================================================
    # SLIDE 5: Two Parts of Our Project (emu8086 + Web Studio)
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Two Parts of Our Project")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Part 1: emu8086 Assembly Application", [
                 "Our core project written completely in 8086 Assembly Language.",
                 "Runs natively inside emu8086 emulator software.",
                 "Controls the computer's PC speaker directly using assembly instructions (IN and OUT).",
                 "Interactive menu in text mode: press 1 for Piano, 2 for Guitar, 3 for Drums, 4 for Songs.",
                 "Demonstrates 8086 registers, loops, delay timers, and keyboard inputs.",
                 "Runs directly with 1 click on 'Emulate' and 'Run' in emu8086."
             ], COLOR_CRIMSON, "Core Assembly Engine (emu8086)")

    add_card(s5, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.3),
             "Part 2: Real Sound Studio (HTML/CSS/JS)", [
                 "Why we made it: The PC speaker in emu8086 can only make beeps, not real instruments.",
                 "To show what our project sounds like in real life, we built a modern Studio companion.",
                 "Built with HTML for layout, CSS for 3D design, and JavaScript for sound playback.",
                 "Uses 28 real recorded instrument sounds (Steinway piano, Martin guitar, Ludwig drums).",
                 "Features a real-time moving music visualizer with live frequency numbers.",
                 "Runs with 1 double-click in any browser without needing any installation."
             ], COLOR_GOLD, "Modern Realistic Sound Extension")

    # ==========================================================================
    # SLIDE 6: Where We Got the Real Sounds
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Where We Got the Real Sounds Online")

    w3 = Inches(3.7)
    gap3 = Inches(0.25)
    top_snd = Inches(1.6)
    h_snd = Inches(5.3)

    add_card(s6, Inches(0.8), top_snd, w3, h_snd,
             "Real Grand Piano Sounds", [
                 "Where we got it: Downloaded from a professional studio recording of a Steinway & Sons Grand Piano.",
                 "Notes included: 13 individual notes (C4, D4, E4, F4, G4, A4, B4, C5, plus all black sharp keys).",
                 "Sound quality: Crystal-clear acoustic recordings with real wooden piano body resonance.",
                 "How it plays: Keys Q to I play real piano notes with natural sustain pedal release on [SPACE]."
             ], COLOR_CRIMSON, "Steinway & Sons Grand Piano")

    add_card(s6, Inches(0.8) + (w3 + gap3), top_snd, w3, h_snd,
             "Real Acoustic Guitar Sounds", [
                 "Where we got it: Downloaded from an acoustic guitar recording session of a Martin D-28 guitar.",
                 "Sounds included: All 6 individual strings (Low E, A, D, G, B, High E) plus strummed acoustic chords.",
                 "Sound quality: Real bronze and steel strings with genuine acoustic warmth.",
                 "How it plays: Plucking strings triggers real acoustic notes and visible string vibrations on screen."
             ], COLOR_GOLD, "Martin Acoustic Guitar")

    add_card(s6, Inches(0.8) + (w3 + gap3)*2, top_snd, w3, h_snd,
             "Real Studio Drum Sounds", [
                 "Where we got it: Downloaded from high-quality studio mic recordings of a Ludwig Drum Kit.",
                 "Sounds included:",
                 "• Deep acoustic Bass Kick drum",
                 "• Snappy Snare drum with metal wire sound",
                 "• Metallic brass Hi-Hats",
                 "• Deep Tom-Toms and explosive Crash Cymbal",
                 "How it plays: Clicking drums triggers punchy studio hits with visual shockwaves."
             ], COLOR_GREEN, "Ludwig Studio Drum Kit")

    # ==========================================================================
    # SLIDE 7: Piano Module
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Concert Piano Module")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "In emu8086 Assembly (piano.asm)", [
                 "Drew 3D white and black piano keys using text characters on screen.",
                 "Keys light up and press down when you type on your keyboard.",
                 "Play notes using keys Q, W, E, R, T, Y, U, I (white keys) and 2, 3, 5, 6, 7 (black keys).",
                 "Added [TAB] button to switch between Octave 4 and high Concert Octave 5.",
                 "Added [SPACE] button to turn on Sustain Pedal so notes ring longer.",
                 "Formula: Divides sound clock by note frequency to generate the exact tone."
             ], COLOR_CRIMSON, "Assembly Code in emu8086")

    add_card(s7, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.3),
             "In Web Studio (HTML/CSS/JS)", [
                 "Built a realistic piano interface with ivory white keys and ebony black keys.",
                 "When a key is clicked or typed, it smoothly sinks down with realistic 3D shadows.",
                 "Plays genuine 44.1 kHz Steinway Grand Piano audio samples.",
                 "Sustain pedal button lets notes ring naturally just like a real concert piano.",
                 "Octave selector lets you play 3 complete octaves cleanly."
             ], COLOR_GOLD, "Realistic Studio Interface")

    # ==========================================================================
    # SLIDE 8: Acoustic Guitar Module
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "Acoustic Guitar Module")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "In emu8086 Assembly (guitar.asm)", [
                 "Drew a 12-fret guitar fretboard with 6 strings and fret dots on screen.",
                 "Tuned all 6 strings from Low E to High E just like a real guitar.",
                 "Added pick scratch effect: a quick chirp sound when you pluck a string.",
                 "Added finger vibrato effect: note gently wobbles for a natural singing sound.",
                 "Added [S] button to strum a full acoustic chord across all strings."
             ], COLOR_GOLD, "Assembly Code in emu8086")

    add_card(s8, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.3),
             "In Web Studio (HTML/CSS/JS)", [
                 "Built a photorealistic guitar neck with soundhole and nickel frets.",
                 "When you pluck strings Q, W, E, R, T, Y, strings physically vibrate on screen.",
                 "Plays real Martin acoustic guitar recordings for every string.",
                 "Includes instant chord buttons for E Minor, G Major, C Major, and D Major.",
                 "In song mode, the guitar plucks out the melody notes automatically."
             ], COLOR_CRIMSON, "Realistic Studio Interface")

    # ==========================================================================
    # SLIDE 9: Drum Kit Module
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "Studio Drum Kit Module")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "In emu8086 Assembly (drums.asm)", [
                 "The Challenge: PC speaker only makes tones, but drums need unpitched noise.",
                 "Solution: Created an assembly random number noise generator to make real white noise.",
                 "Snare Drum: Blends white noise with a wooden thump sound.",
                 "Kick Drum: Rapidly drops frequency from 420 Hz to 42 Hz for a punchy boom.",
                 "Hi-Hats & Crash: Short crisp noise for hi-hats, long shimmering noise for crash cymbals."
             ], COLOR_CRIMSON, "Assembly Code in emu8086")

    add_card(s9, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.3),
             "In Web Studio (HTML/CSS/JS)", [
                 "Built a 3D stage drum kit layout with Kick, Snare, Toms, Hi-Hat, and Crash.",
                 "Pads pulse and show animated shockwave rings when hit.",
                 "Plays genuine Ludwig acoustic drum kit recordings with punchy acoustic impact.",
                 "Play with keys: Q (Kick), W (Snare), E (Hi-Hat), R (Tom), T (Crash).",
                 "In song mode, plays a real rock drum beat in time with the music."
             ], COLOR_GOLD, "Realistic Studio Interface")

    # ==========================================================================
    # SLIDE 10: Songs & Visualizer
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, "Songs & Equalizer Module")

    add_card(s10, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Song Notes & Timing (songs.asm)", [
                 "Stored musical notes and timings for 6 classic songs:",
                 "1. Happy Birthday",
                 "2. Twinkle Twinkle Little Star",
                 "3. Beethoven's Ode to Joy",
                 "4. Jingle Bells",
                 "5. Mary Had a Little Lamb",
                 "6. London Bridge Is Falling Down",
                 "Used timer delay loops so each song plays at the right tempo.",
                 "Connected the same song notes into Web Studio."
             ], COLOR_GOLD, "Songs Data & Timing")

    add_card(s10, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.3),
             "Jukebox Player & Visualizer", [
                 "Built the automatic jukebox in emu8086 that plays through the songs.",
                 "Animated 8 equalizer bars jumping up and down to the music.",
                 "Added [ESC] button support so the user can stop playback anytime without crashing.",
                 "In Web Studio, built a colorful 60 FPS moving music spectrum equalizer.",
                 "Users can choose to hear songs played on Grand Piano, Acoustic Guitar, or Drum Groove."
             ], COLOR_GREEN, "Jukebox Player & Visualizer")

    # ==========================================================================
    # SLIDE 11: User Music Creation — Custom Song Composer & Sequencer
    # ==========================================================================
    s_comp = prs.slides.add_slide(blank_layout)
    set_bg(s_comp)
    add_header(s_comp, "User Music Creation — Custom Song Composer & Sequencer")

    add_card(s_comp, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "In emu8086 Assembly (composer.asm)", [
                 "Requested Feature: Allows users to compose, record, and play their own music.",
                 "Direct RAM Recording: Up to 60 notes stored dynamically in 8086 memory as [Frequency, Duration] pairs.",
                 "Live Track Tape: On-screen visual tape displays notes as you compose (e.g. [C5] [E5] [G5] [C6]...).",
                 "Full Editing Controls:",
                 "• [1..4] Note Lengths (Eighth, Quarter, Half, Whole)",
                 "• [B / Bksp] Undo last note, [C] Clear song, [L] Load starter melody",
                 "• [P] Live Playback: Plays user song with audible notes!",
                 "Jukebox Integration: Appears as Option 7 in Demo Songs Repertoire — playable on Piano, Guitar, or Drums!"
             ], COLOR_CRIMSON, "Live 8086 RAM Track Recorder")

    add_card(s_comp, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.3),
             "In Web Studio (HTML/CSS/JS)", [
                 "16-Step Multi-Track Sequencer: Digital Audio Workstation (DAW) matrix.",
                 "8 Interactive Tracks: Piano (C5, G4, E4, C4), Guitar Chord, Drum Crash, Snare, and Kick.",
                 "Live Moving Sweep Cursor: Glowing sweep bar scans across all 16 steps in real time with the beat.",
                 "Tempo & Controls: Real-time BPM slider (60 to 180 BPM), Load Starter Beat, and Clear Grid.",
                 "Live Tape & Storage: Saves custom compositions to browser memory and logs notes to the tape.",
                 "Runs seamlessly offline in any browser with authentic studio audio samples."
             ], COLOR_GOLD, "16-Step Multi-Track Studio Sequencer")

    # ==========================================================================
    # SLIDE 12: How to Run & Live Demo
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_header(s11, "How to Run Our Project & Live Demo")

    add_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "1. Running in emu8086 (Assembly)", [
                 "Step 1: Open emu8086 software on the computer.",
                 "Step 2: Open file 'kernel.asm' from the project folder.",
                 "Step 3: Click the green 'Emulate' button on the toolbar.",
                 "Step 4: Click 'Run' in the emulator window.",
                 "Result: The Crimson Orbit Band starts instantly! You can play Piano (1), Guitar (2), Drums (3), or Songs (4) through the PC speaker."
             ], COLOR_CRIMSON, "Assembly Emulation Demo")

    add_card(s11, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.3),
             "2. Running Real Sound Studio (Web)", [
                 "Step 1: Go to your Desktop or Downloads folder.",
                 "Step 2: Double-click 'CrimsonOrbit_RealStudio.html'.",
                 "Step 3: It opens instantly in Chrome or Edge without needing any server.",
                 "Step 4: Click 'Audio Engine Ready' or play keys Q to I.",
                 "Result: You will hear real Steinway grand piano, real Martin guitar, and real Ludwig drums with a moving visualizer!"
             ], COLOR_GOLD, "Realistic Sound Demo")

    # ==========================================================================
    # SLIDE 12: Technical Defense Guide
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12)
    add_header(s12, "Technical Defense Guide — Questions & Answers")

    w_qa = Inches(5.6)
    add_card(s12, Inches(0.8), Inches(1.6), w_qa, Inches(2.55),
             "Piano & System Architecture", [
                 "Q: How does sound work in emu8086?",
                 "A: We program the sound ports by calculating note divisor values and sending them to the timer, then turn on the PC speaker gate.",
                 "Q: Why did we build the web studio too?",
                 "A: The PC speaker in emu8086 only makes electronic beeps. We built the web studio to show how our assembly music sounds on real instruments."
             ], COLOR_CRIMSON)

    add_card(s12, Inches(6.9), Inches(1.6), w_qa, Inches(2.55),
             "Guitar & Drums Modules", [
                 "Guitar: We coded the 6 strings, added pick strike sound effects, singing vibrato, and full chord strumming on key [S], paired with Martin acoustic guitar sounds.",
                 "Drums: We wrote a random noise generator in assembly to create white noise for snares and cymbals, paired with real Ludwig acoustic drum recordings."
             ], COLOR_GOLD)

    add_card(s12, Inches(0.8), Inches(4.3), w_qa, Inches(2.6),
             "Songs & Music Visualizer", [
                 "Songs: We stored the notes and delay timers for 6 classic songs in assembly and mapped them to the web studio.",
                 "Visualizer: We built the automatic song player in emu8086, added animated equalizer bars, and made sure pressing [ESC] stops the song anytime."
             ], COLOR_GREEN)

    add_card(s12, Inches(6.9), Inches(4.3), w_qa, Inches(2.6),
             "Project Summary Statement", [
                 "\"Professor, this project shows we learned 8086 assembly language in emu8086 to control hardware and keyboard inputs, and we also showed how our music sounds on real acoustic instruments in modern studio quality!\""
             ], COLOR_WHITE)

    # Save to Project, Desktop, and Downloads
    out_project = r"c:\FOIDS_CP\Assets\Documentation\CrimsonOrbit_Presentation.pptx"
    out_desktop = r"C:\Users\akash\Desktop\CrimsonOrbit_Presentation.pptx"
    out_desktop_final = r"C:\Users\akash\Desktop\CrimsonOrbit_Final_Presentation.pptx"
    out_downloads_main = r"C:\Users\akash\Downloads\CrimsonOrbit_Presentation.pptx"
    out_downloads_final = r"C:\Users\akash\Downloads\CrimsonOrbit_Final_Presentation.pptx"

    prs.save(out_project)
    print(f"Saved PPTX to Project: {out_project}")

    for p in [out_desktop, out_desktop_final]:
        try:
            prs.save(p)
            print(f"Saved to Desktop: {p}")
        except Exception as e:
            print(f"Desktop save note ({p}): {e}")

    for p in [out_downloads_final, out_downloads_main]:
        try:
            prs.save(p)
            print(f"Saved to Downloads: {p}")
        except Exception as e:
            print(f"Downloads save note ({p}): {e}")

if __name__ == "__main__":
    create_presentation_deck()
