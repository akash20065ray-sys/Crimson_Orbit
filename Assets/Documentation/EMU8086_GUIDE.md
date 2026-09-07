# emu8086 Compilation & Build Guide

This guide details how to assemble, test, and build the **Crimson Orbit – Musical Band** binaries using **emu8086**.

---

## 1. Project Architecture in emu8086

emu8086 supports direct generation of bare-metal binaries through compiler directives:
- `#make_boot#`: Creates a boot sector binary formatted for Sector 1 of a floppy disk (`0000:7C00h`).
- `#make_bin#`: Creates a flat binary executable loaded at a designated segment and offset (e.g. `1000h:0000h`).

Because emu8086 does not use an external DOS linker for bare-metal targets, `Source/kernel.asm` uses `include` directives to bring in all instrument modules (`piano.asm`, `guitar.asm`, `drums.asm`, `demo.asm`, etc.) into one unified, cohesive kernel binary (`Builds/kernel.bin`).

---

## 2. Step-by-Step Compilation in emu8086 GUI

### Step A: Assemble the Bootloader (`boot.asm`)
1. Launch **emu8086**.
2. Click **File -> Open** and choose:
   ```
   C:\FOIDS_CP\Source\boot.asm
   ```
3. Notice the `#make_boot#` directive at line 1.
4. Click the **Compile** button on the toolbar (or press `F5` / click **Compile** in the menu).
5. In the Save Dialog, save the compiled binary as:
   ```
   C:\FOIDS_CP\Builds\loader.bin
   ```
   *(Ensure the output format is `.bin` or `.boot`).*

### Step B: Assemble the Kernel (`kernel.asm`)
1. In **emu8086**, click **File -> Open** and choose:
   ```
   C:\FOIDS_CP\Source\kernel.asm
   ```
2. Notice the `#make_bin#` and `#LOAD_SEGMENT=1000h#` directives at the top.
3. Click the **Compile** button on the toolbar.
4. Save the compiled binary as:
   ```
   C:\FOIDS_CP\Builds\kernel.bin
   ```
   *(emu8086 will also create `kernel.binf` alongside it containing segment register defaults).*

---

## 3. Building the Bootable Floppy Image (`MusicalBand.flp`)

Once `loader.bin` and `kernel.bin` exist in the `Builds/` folder:

### Method 1: Automated Script (Recommended)
Open PowerShell in the project directory and run:
```powershell
.\build.ps1
```
or
```powershell
python Tools\build_floppy.py
```
This will:
- Validate `loader.bin` (ensuring 512 bytes with signature `0x55AA`).
- Place `loader.bin` at Sector 1 (Bytes 0..511).
- Place `kernel.bin` at Sector 2 onwards (Bytes 512..end of kernel binary).
- Pad the disk image with zeros to the exact 1,474,560 byte standard.
- Produce `Builds\MusicalBand.flp` (and syncs `CrimsonOrbit.flp` / `CrimsonOrbit.img`).

### Method 2: emu8086 Virtual Drive Menu
1. In emu8086, open the **Virtual Drive** menu on the main toolbar.
2. Select **Write 512 bytes to boot sector of a virtual floppy drive**.
3. Select `Builds\loader.bin`.
4. Then use the emu8086 floppy editor or `Tools\build_floppy.py` to write `kernel.bin` to Sector 2.

---

## 4. Direct Emulation in emu8086

You can also test components directly inside the emu8086 emulator window:
1. Open `Source/kernel.asm` in emu8086.
2. Click **Emulate** (green play triangle icon).
3. The emu8086 emulator will open with:
   - `CS = 1000h`, `IP = 0000h`
   - `DS = 1000h`, `ES = 1000h`
   - `SS = 1000h`, `SP = FFFEh`
4. Click **Run** in the emulator window to test the splash screen, sound, and instruments within the emulator.
