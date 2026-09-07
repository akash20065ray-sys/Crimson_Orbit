# Crimson Orbit – Musical Band
**Bare-Metal 8086 Assembly Interactive Audio Workstation**
*Designed for emu8086 Assembler & VMware Workstation*

---

## 1. Project Overview

**Crimson Orbit – Musical Band** is a standalone, bare-metal operating system and musical workstation written in 16-bit 8086 real-mode assembly language. It boots directly from a virtual 1.44 MB floppy disk image (`MusicalBand.flp`) without DOS or any underlying operating system.

### Core Highlights
- **Direct Hardware Sound Engine**: Real-time programming of the Intel 8254 Programmable Interval Timer (PIT, Ports 42h/43h) and Intel 8255 Programmable Peripheral Interface (PPI, Port 61h) to drive the PC Speaker.
- **Three Interactive Instruments**:
  - **8086 Concert Grand Piano**: Visual multi-octave keyboard layout with active key illumination and HUD.
  - **6-String Crimson Lead Guitar**: Simulated fretboard with vibrating string graphics and acoustic pluck attack dynamics.
  - **5-Piece Percussion Drum Kit**: Stage visual pads with hit animations and synthesized Kick, Snare, Hi-Hat, Tom-Tom, and Crash Cymbal effects.
- **Pre-installed Song Repertoire**: 6 complete songs playable in Piano, Guitar, or Drum percussion styles with a live animated spectrum visualizer.
- **Crimson Orbit Visual System**: Text-mode CP437 box drawing, borders, and a cohesive high-contrast palette (Crimson, Amber Gold, Bright White, and Deep Black).

---

## 2. System Architecture & Memory Map

```
+-------------------------------------------------------------+
| 0x00000 - 0x003FF : Interrupt Vector Table (IVT)            |
| 0x00400 - 0x004FF : BIOS Data Area (Timer Ticks at 0040:006C)|
| 0x07C00 - 0x07DFF : MBR Bootloader (boot.asm - Sector 1)    |
| 0x10000 - 0x1FFFF : Kernel & Soundstage (kernel.asm @ 1000h)|
| 0x1FFFE           : Kernel Stack Top (SS=1000h, SP=FFFEh)   |
| 0xB8000 - 0xBAF3F : CGA/VGA 80x25 Color Text Buffer (Mode 3)|
+-------------------------------------------------------------+
```

### Floppy Disk Organization (`MusicalBand.flp` - 1,474,560 Bytes)
- **Sector 1** (Cylinder 0, Head 0, Sector 1): `loader.bin` (512 bytes, MBR signature `0x55AA`).
- **Sectors 2 to 22** (Cylinder 0, Heads 0 & 1): `kernel.bin` (Kernel controller and all modular instruments).
- **Sectors 23 to 2,880**: Zero-padded to the exact 1.44 MB standard floppy geometry.

---

## 3. Directory Structure

```
CrimsonOrbit_MusicalBand/
├── Source/                     # Modular 8086 Assembly Source Code
│   ├── boot.asm                # Bare-metal MBR bootloader (BIOS INT 13h)
│   ├── kernel.asm              # Application entry, splash screen, coordinator
│   ├── menu.asm                # Main Menu, Help, About, Exit dialogs
│   ├── graphics.asm            # CP437 box-drawing, borders, headers, colors
│   ├── keyboard.asm            # Centralized BIOS INT 16h input handlers
│   ├── speaker.asm             # Hardware PIT 8254 & PPI 8255 sound engine
│   ├── piano.asm               # Interactive Concert Piano
│   ├── guitar.asm              # Simulated 6-String Lead Guitar
│   ├── drums.asm               # Simulated 5-Piece Drum Kit
│   ├── demo.asm                # Demo songs player with animated visualizer
│   ├── songs.asm               # 6 pre-installed song score data tables
│   └── utils.asm               # Screen, cursor, delay, and string routines
│
├── Builds/                     # Generated Executable Binaries
│   ├── loader.bin              # 512-byte boot sector binary
│   ├── kernel.bin              # Flat kernel binary (loaded at 1000:0000h)
│   └── MusicalBand.flp         # 1.44 MB bootable floppy disk image
│
├── Tools/                      # Automation Tools
│   ├── build_floppy.py         # Floppy disk image assembler
│   └── test_assemble.py        # Automated syntax & build verifier
│
├── VMware/                     # VMware Workstation Preconfigured VM
│   └── CrimsonOrbit.vmx        # VM configuration ready to boot MusicalBand.flp
│
├── Assets/
│   ├── Documentation/          # Detailed Guides
│   │   ├── README.md           # This document
│   │   ├── EMU8086_GUIDE.md    # Guide for assembling in emu8086 GUI
│   │   └── VMWARE_SETUP.md     # Guide for VMware Workstation configuration
│   └── Screenshots/            # Interface captures and artwork
│
└── build.ps1                   # One-click PowerShell build helper
```

---

## 4. Module Navigation Flow

```
BIOS Power-On
      ↓
Floppy Sector 1 (0000:7C00h)
[Source/boot.asm]
      ↓
Loads 36 sectors via INT 13h to 1000:0000h
      ↓
Jumps to 1000h:0000h
[Source/kernel.asm]
      ↓
Crimson Orbit Welcome Screen & Intro Fanfare
      ↓
Press [ENTER]
      ↓
[Source/menu.asm] Main Menu
  ├── [1] Interactive Piano       ──(ESC)──> Return to Menu
  ├── [2] 6-String Guitar         ──(ESC)──> Return to Menu
  ├── [3] Drum Kit                ──(ESC)──> Return to Menu
  ├── [4] Demo Songs & Visualizer ──(ESC)──> Return to Menu
  ├── [5] Help Screen             ──(Key)──> Return to Menu
  ├── [6] Architecture & About    ──(Key)──> Return to Menu
  └── [7] Exit / System Reboot    ──(ENTER)─> BIOS Warm Reboot (INT 19h)
```

---

## 5. Instrument Controls

### Piano Controls
- **White Keys**:
  - `Q` = C4 (262 Hz)
  - `W` = D4 (294 Hz)
  - `E` = E4 (330 Hz)
  - `R` = F4 (349 Hz)
  - `T` = G4 (392 Hz)
  - `Y` = A4 (440 Hz)
  - `U` = B4 (494 Hz)
  - `I` = C5 (523 Hz)
- **Black Keys**:
  - `2` = C#4 (277 Hz)
  - `3` = D#4 (311 Hz)
  - `5` = F#4 (370 Hz)
  - `6` = G#4 (415 Hz)
  - `7` = A#4 (466 Hz)
- `ESC` = Return to Main Menu

### Guitar Controls
- `Q` = String 1: High E4 (329 Hz)
- `W` = String 2: B3      (247 Hz)
- `E` = String 3: G3      (196 Hz)
- `R` = String 4: D3      (147 Hz)
- `T` = String 5: A2      (110 Hz)
- `Y` = String 6: Low E2  ( 82 Hz)
- `ESC` = Return to Main Menu

### Drum Kit Controls
- `Q` = Bass Kick Drum (Rapid downward pitch sweep: 160 Hz -> 32 Hz)
- `W` = Snare Drum (High-frequency noise crackle + 180 Hz body tone)
- `E` = Closed Hi-Hat (Ultra-fast metallic pulse: ~8ms)
- `R` = Tom-Tom (Resonant downward glide: 220 Hz -> 100 Hz)
- `T` = Crash Cymbal (High-energy noise splash with exponential ring-out decay)
- `ESC` = Return to Main Menu

### Demo Songs
1. *Happy Birthday*
2. *Twinkle Twinkle Little Star*
3. *Ode to Joy* (Beethoven)
4. *Jingle Bells*
5. *Mary Had a Little Lamb*
6. *London Bridge Is Falling Down*

Instrument Playback Styles:
- **Piano**: Pure melodic square wave with smooth phrasing.
- **Guitar**: Plucked attack transient envelope simulation.
- **Drums**: Percussive rhythm arrangement mapping notes to Kick, Snare, Tom, and Crash.
- `ESC`: Instant playback abort back to menu.
