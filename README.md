# 🎵 Crimson Orbit – Musical Band & Real Sound Studio

> **Interactive 8086 Assembly Audio Workstation & Modern Sound Studio**  
> *Course Project for Department of Multidisciplinary Engineering*  
> **Vishwakarma Institute of Technology, Pune** (An Autonomous Institute Affiliated to Savitribai Phule Pune University)

---

## 🏛️ Project & Academic Information

| Field | Details |
| :--- | :--- |
| **Institution** | Vishwakarma Institute of Technology, Pune |
| **Department** | Department of Multidisciplinary Engineering / AI & DS |
| **Academic Year** | 2025–2026 |
| **Course Project Group** | Group - 9 |
| **Faculty Guide** | **Prof. Gopal Upadhye** |

### 👥 Team Members

| Roll No. | Student Name | PRN |
| :---: | :--- | :---: |
| **04** | Akash Kumar | 12410741 |
| **07** | Aryan Jagtap | 12411032 |
| **09** | Atharva Gaikwad | 12411136 |
| **38** | Shravani Phadtare | 12410978 |
| **49** | Shweta Patil | 12410292 |

---

## 📌 Project Overview

**Crimson Orbit** is an interactive musical band and audio system developed in 16-bit 8086 real-mode assembly language. The project bridges low-level hardware control with creative software design, delivering both a **bare-metal 8086 audio application** running on emu8086/PC hardware and an interactive **Real Sound Studio Workstation** with studio-grade instruments.

### Key Highlights
- **Direct Hardware Sound Engine**: Real-time frequency generation using the Intel 8254 Programmable Interval Timer (PIT, Ports `42h`/`43h`) and Intel 8255 Programmable Peripheral Interface (PPI, Port `61h`) driving the PC Speaker.
- **Three Live Instruments**:
  - 🎹 **Concert Grand Piano**: Multi-octave chromatic scale with active key press indicators.
  - 🎸 **6-String Lead Guitar**: Fretboard graphics with string pluck dynamics.
  - 🥁 **5-Piece Drum Kit**: Synthesized percussive frequencies for Kick, Snare, Hi-Hat, Tom-Tom, and Crash Cymbal.
- **Pre-installed Song Repertoire**: Classic melodies (e.g., Ode to Joy, Twinkle Twinkle, Jingle Bells, Für Elise) with live animated spectrum visualizer.
- **Real Sound Studio (Web Edition)**: High-fidelity studio workstation with realistic recorded instrument samples, loop recorders, and visual effects.

---

## 🏗️ 3-Tier System Architecture

```
+-------------------------------------------------------------------------+
|                       TIER 1: USER INPUT LAYER                          |
|    • QWERTY Keyboard Capture (BIOS INT 16h)                             |
|    • Interactive Menu Navigation & Instrument Selection                 |
|    • Real Sound Studio Touch / Mouse / Key Controls                     |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                    TIER 2: SOUND PROCESSING ENGINE                      |
|    • Note-to-Divisor Pitch Mapping: Divisor = 1,193,180 Hz / Frequency |
|    • Intel 8254 PIT (Port 42h/43h) Square-Wave Timer Programming        |
|    • Intel 8255 PPI (Port 61h) Speaker Gate Enable/Disable Controls     |
|    • Audio Synthesis & Base64 High-Fidelity Audio Buffers               |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                     TIER 3: OUTPUT & VISUAL DISPLAY                     |
|    • PC Speaker Acoustic Sound Waves                                    |
|    • CGA/VGA 80x25 Color Text Mode (03h) Buffer at 0xB8000              |
|    • Real-time Key Illumination, Fretboard Vibrations & Drum Visuals    |
+-------------------------------------------------------------------------+
```

---

## 📂 Repository Structure

```
Crimson_Orbit/
├── Source/                             # 16-bit 8086 Assembly Source Code
│   ├── boot.asm                        # Bare-metal MBR bootloader (BIOS INT 13h)
│   ├── kernel.asm                      # Kernel entry, splash screen & coordinator
│   ├── menu.asm                        # Interactive menu navigation
│   ├── piano.asm                       # Concert Grand Piano implementation
│   ├── guitar.asm                      # 6-String Lead Guitar implementation
│   ├── drums.asm                       # 5-Piece Drum Kit implementation
│   ├── speaker.asm                     # PIT 8254 & PPI 8255 sound engine
│   ├── songs.asm                       # Music score data tables
│   ├── demo.asm                        # Automated demo player & visualizer
│   ├── graphics.asm                    # CP437 UI box drawing & color palettes
│   ├── keyboard.asm                    # Keyboard interrupt handlers
│   └── utils.asm                       # Screen, cursor & timing routines
│
├── Studio/                             # Real Sound Studio Workstation
│   ├── index.html                      # Interactive modern studio web app
│   ├── standalone.html                 # 100% self-contained offline studio
│   ├── style.css                       # Crimson Orbit dark-theme design
│   ├── app.js                          # WebAudio multi-instrument engine
│   └── audio/                          # 28 studio-quality audio samples
│
├── Builds/                             # Ready-to-Run Binaries & Images
│   ├── new2.flp                        # Bootable 1.44 MB Floppy Disk Image
│   ├── MusicalBand.flp                 # Floppy disk image
│   ├── loader.bin                      # 512-byte MBR bootloader binary
│   └── kernel.bin                      # Assembled flat kernel binary
│
├── Assets/
│   ├── Documentation/
│   │   ├── CrimsonOrbit_Presentation.pptx     # 13-Slide Review Presentation
│   │   ├── CrimsonOrbit_Presentation_Script.pdf # Official Speech Script & Q&A
│   │   ├── CrimsonOrbit_Presentation_Script.docx# Word version of speech script
│   │   ├── EMU8086_GUIDE.md                   # emu8086 configuration guide
│   │   └── VMWARE_SETUP.md                    # VMware Workstation setup guide
│   ├── Audio/Real/                            # Real instrument audio samples
│   └── Images/                                # Presentation title & team graphics
│
├── Tools/                              # Python Build & Generator Scripts
│   ├── build_floppy.py                 # Floppy disk packaging utility
│   ├── generate_presentation.py        # Presentation generator
│   └── generate_script_docs.py         # Script & Q&A document generator
│
├── VMware/
│   └── CrimsonOrbit.vmx                # VMware virtual machine configuration
│
├── build.bat                           # Windows batch build script
├── build.ps1                           # PowerShell automation build script
└── README.md                           # Project documentation
```

---

## 🚀 How to Run

### Option 1: Running in emu8086 (Recommended for Lab / Evaluation)
1. Download and install **emu8086 Microprocessor Emulator**.
2. Open emu8086, click **Open**, and browse to `Source/kernel.asm`.
3. Click **Compile** or **Emulate** (`F5`).
4. Click **Run** in the emulator window.
5. Use keys `1`–`6` to navigate instruments, play notes with your keyboard, or enjoy automated song playback!

### Option 2: Running in VMware / VirtualBox / QEMU
1. Create a new Virtual Machine (Other 16-bit OS).
2. Attach `Builds/new2.flp` as a Floppy Drive image.
3. Power on the Virtual Machine. The MBR bootloader will load the kernel directly without any underlying OS!

### Option 3: Launching the Real Sound Studio (Browser)
1. Open `Studio/index.html` or `Studio/standalone.html` directly in Google Chrome, Microsoft Edge, or Mozilla Firefox.
2. Click anywhere on the screen or press keys to play real piano, guitar chords, and drum beats with responsive animations.

---

## 🎹 Keyboard Controls Guide (emu8086)

| Key | Action |
| :---: | :--- |
| `1` | Open **Piano** Mode |
| `2` | Open **Guitar** Mode |
| `3` | Open **Drums** Mode |
| `4` | Open **Song Player** / Demo Mode |
| `5` | View **Help & Controls** |
| `6` / `ESC` | Exit / Return to Main Menu |
| `A`–`K` | Musical Notes (C4 to C5 on Piano) |
| `1`–`6` | Guitar Strings (E2, A2, D3, G3, B3, E4) |
| `Z`, `X`, `C`, `V`, `B` | Drum Pads (Kick, Snare, Hi-Hat, Tom, Crash) |

---

## 🏆 Project Deliverables
- 📄 **Presentation Slides**: [`Assets/Documentation/CrimsonOrbit_Presentation.pptx`](file:///c:/FOIDS_CP/Assets/Documentation/CrimsonOrbit_Presentation.pptx)
- 🎙️ **Speech Script & Viva Q&A**: [`Assets/Documentation/CrimsonOrbit_Presentation_Script.pdf`](file:///c:/FOIDS_CP/Assets/Documentation/CrimsonOrbit_Presentation_Script.pdf)
- 💾 **Bootable Floppy Image**: [`Builds/new2.flp`](file:///c:/FOIDS_CP/Builds/new2.flp)
- 🌐 **Real Sound Studio**: [`Studio/index.html`](file:///c:/FOIDS_CP/Studio/index.html)

---

## 📜 License
Developed for academic purposes under the guidance of **Prof. Gopal Upadhye**, Department of Multidisciplinary Engineering, **Vishwakarma Institute of Technology, Pune**.
