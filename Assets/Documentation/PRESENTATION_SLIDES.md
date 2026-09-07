# Crimson Orbit – Musical Band
## Course Project Presentation Deck & Speaker Script

**Generated PowerPoint File**: [`Assets/Documentation/CrimsonOrbit_Presentation.pptx`](file:///c:/FOIDS_CP/Assets/Documentation/CrimsonOrbit_Presentation.pptx)  
**Format**: 16:9 Widescreen | Clean, Punchy Dark-Crimson Theme  
**Slides Count**: 7 Simple & Direct Slides  
**Presentation Time**: ~5 to 7 minutes + 2-minute live demo  

---

## Slide 1: Title Slide

### Slide Content:
- **Title**: CRIMSON ORBIT – MUSICAL BAND
- **Subtitle**: A Complete Musical Band Built in 8086 Assembly Language
- **Course Project**: Target: emu8086 & VMware Workstation (Bootable Floppy Disk)

### 🎙️ What to Say:
> "Hello everyone and Professor. For our course project, we built **Crimson Orbit – Musical Band**.
> 
> It is an interactive, playable musical band application written completely in **8086 Assembly Language**. It boots directly from a virtual floppy disk in VMware without needing Windows or DOS, and plays real music through the computer's PC speaker."

---

## Slide 2: What Are We Making?

### Slide Content:
#### The Concept:
- We are making an interactive Musical Band using 8086 Assembly.
- Runs completely on bare metal: boots from a floppy disk without DOS or Windows.
- All sounds are synthesized directly through the PC Speaker hardware.
- Includes 3 playable instruments and 6 built-in songs.
- Features a rich Crimson Orbit visual theme in text mode.

#### What's Inside the Band?
- **Piano**: Play musical notes with real-time glowing keys.
- **Guitar**: 6-string guitar with plucked notes and string vibrations.
- **Drums**: Full 5-piece kit (Kick, Snare, Hi-Hat, Tom, Crash).
- **Demo Songs**: 6 classic songs with an animated visualizer.
- **Menu Navigation**: Easy menus and ESC to return anytime.

### 🎙️ What to Say:
> "So what exactly are we making? 
> We are making a complete digital band right inside 8086 assembly. You have a **Piano**, a **Guitar**, and a **Drum Kit** that you can play live using your computer keyboard.
> 
> In addition to the instruments, we added a **Demo Songs** jukebox with 6 classic songs. The coolest part is that everything runs on bare metal—meaning when the PC turns on, our program takes over directly from BIOS, and every sound you hear is generated directly by controlling the motherboard's timer chip and speaker."

---

## Slide 3: Project Workflows — How It's Built & How It Runs

### Slide Content:
#### 1. Development & Testing Workflow (Build Loop):
```
VS Code (Write .asm)
   ↓
emu8086 (Assemble boot.asm & kernel.asm)
   ↓
Floppy Packer (Create MusicalBand.flp)
   ↓
VMware Workstation (Boot & Test)
   ↓
Fix Bugs ──► Advance to Next Phase
```
*Golden Engineering Rule: Never advance to the next phase until the current phase boots cleanly in VMware!*

#### 2. Runtime Execution Workflow (How the App Runs):
```
BIOS Power-On (Executes Sector 1 at 0000:7C00h)
   ↓
boot.asm (Loads 36 sectors into RAM at 1000h:0000h)
   ↓
kernel.asm (Displays Splash Screen & Fanfare)
   ↓
Main Menu (User selects 1 to 7)
   ├── [1] Piano
   ├── [2] Guitar
   ├── [3] Drums
   └── [4] Demo Songs ──► (ESC returns to Main Menu)
```

### 🎙️ What to Say:
> "Now let's look at the workflow. There are two parts to this:
> 
> **First is our Development Workflow**:
> We write code in VS Code, assemble it in **emu8086**, pack the binaries into `MusicalBand.flp`, and boot it in **VMware Workstation** to test. We followed a strict golden rule: never move to the next instrument until the current one works and boots.
> 
> **Second is the Runtime Workflow**:
> When you power on the computer, the BIOS executes our bootloader from Sector 1. The bootloader loads the rest of the kernel from the floppy into RAM, displays our Crimson Orbit splash screen, and opens the Main Menu where you can launch any instrument."

---

## Slide 4: Development Phases — Step by Step

### Slide Content:
- **Phase 1 to 3: Boot & Menu**:
  - Bootloader (`boot.asm`): Loads the kernel from the floppy disk.
  - Kernel (`kernel.asm`): Displays the Crimson Orbit welcome screen and opening music.
  - Main Menu (`menu.asm`): Simple menu to choose instruments or songs.
- **Phase 4 to 6: Core Engine**:
  - Graphics (`graphics.asm`): Draws boxes, borders, and colors.
  - Keyboard (`keyboard.asm`): Reads user keypresses cleanly.
  - Speaker (`speaker.asm`): Drives the PC speaker to make musical notes and drum sounds.
- **Phase 7 to 10: Instruments & Songs**:
  - Piano: Visual keys and octave notes.
  - Guitar: 6 strings with pluck sound dynamics.
  - Drums: 5 pads with percussion effects.
  - Demo Songs: 6 pre-installed songs with a live visualizer.

### 🎙️ What to Say:
> "We built the project step-by-step in phases. 
> First, we made sure the bootloader and kernel could boot successfully. 
> Then we built the engine—the graphics routines for drawing boxes and borders, the keyboard input handler, and the sound engine for generating frequencies.
> Once the foundation was ready, we implemented the instruments one by one: first the Piano, then the Guitar, then the Drums, and finally the Demo Songs player."

---

## Slide 5: The Playable Instruments

### Slide Content:
- 🎹 **Piano (`piano.asm`)**:
  - Visual keyboard on screen.
  - White keys: `[Q, W, E, R, T, Y, U, I]` for notes C4 through C5.
  - Black keys: `[2, 3, 5, 6, 7]` for sharps (C#, D#, etc.).
  - Visual highlight: Keys glow in Crimson and Gold when pressed.
  - Displays note name, frequency (Hz), and solfège (DO-RE-MI).
  - Press `ESC` to return to menu.
- 🎸 **Guitar (`guitar.asm`)**:
  - 6 horizontal strings across the fretboard.
  - Keys `[Q, W, E, R, T, Y]` pluck strings from High E down to Low E.
  - Strings vibrate visually with wave characters (`~~~~~`) when plucked.
  - Sound engine simulates a sharp pluck transient attack.
- 🥁 **Drums (`drums.asm`)**:
  - 5-pad visual drum kit: Kick `[Q]`, Snare `[W]`, Hi-Hat `[E]`, Tom `[R]`, Crash `[T]`.
  - Drum pads flash bright borders when struck.
  - Uses custom frequency glides and noise bursts to sound like real acoustic drums.

### 🎙️ What to Say:
> "Here are the three instruments we created:
> 
> The **Piano** displays a complete musical keyboard. When you press a key like 'Q' for Middle C, the key illuminates on screen, the HUD shows 'C4 - 262 Hz', and the tone plays through the speaker.
> 
> The **Guitar** displays a 6-string fretboard. Plucking any string from Q to Y causes the string to vibrate on screen with a pluck sound effect.
> 
> The **Drum Kit** has 5 pads. Even though the PC speaker only plays one square wave, we used rapid frequency drops to make the Bass Kick thump, and rapid noise clicks to make the Snare snap and Crash splash!"

---

## Slide 6: 6 Demo Songs & Real-Time Visualizer

### Slide Content:
#### 6 Pre-Installed Songs:
1. *Happy Birthday*
2. *Twinkle Twinkle Little Star*
3. *Ode to Joy* (Beethoven)
4. *Jingle Bells*
5. *Mary Had a Little Lamb*
6. *London Bridge Is Falling Down*

#### Choose Your Instrument Style!
- **Piano Style**: Clean melodic notes with smooth phrasing.
- **Guitar Style**: Plucked acoustic guitar tone.
- **Drums Style**: The melody is translated into a rhythm beat (Kick, Snare, Tom, and Crash)!
- **Live Visualizer**: 8 equalizer bars dance on screen in real time with the music.
- **Instant Abort**: Press `ESC` at any time to immediately stop playback.

### 🎙️ What to Say:
> "If you don't want to play manually, you can go into the Demo Songs menu. We have 6 classic songs included.
> 
> When you select a song, you can choose how you want to hear it: in Piano style, Guitar style, or even **Drums style**, where the song is played as a rhythmic drum cover!
> 
> While the song plays, an animated 8-bar equalizer visualizer dances on screen to the beat. You can press ESC at any moment to cancel and go back."

---

## Slide 7: Live Demo & Conclusion

### Slide Content:
#### Live Demonstration:
1. Booting VMware Workstation with `MusicalBand.flp`.
2. BIOS loads the bootloader $\rightarrow$ Kernel starts.
3. Welcome splash screen with fanfare music.
4. Navigating the Main Menu.
5. Playing the Piano, Guitar, and Drums live.
6. Playing a demo song with the visualizer.

#### Conclusion:
- We proved that 8086 Assembly can be used to create fun, interactive multimedia projects.
- Runs completely on bare metal without any operating system.
- Clean, modular code ready for emu8086 and VMware.
- **Thank You! Any Questions?**

### 🎙️ What to Say:
> "Now, I'll switch over to VMware Workstation to give you a quick live demonstration of the band in action...
> 
> *(Run VMware, show the boot sequence, press a few piano notes, pluck guitar strings, hit the drums, and play Happy Birthday).*
> 
> In conclusion, this project allowed us to explore low-level hardware control, BIOS disk loading, and sound synthesis in 8086 Assembly, proving that even bare-metal code can produce an engaging, interactive application. 
> 
> Thank you, and I'd be happy to answer any questions!"
