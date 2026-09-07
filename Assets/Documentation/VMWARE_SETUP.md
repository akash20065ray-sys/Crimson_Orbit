# VMware Workstation Setup & Boot Guide

This guide describes how to boot the **Crimson Orbit – Musical Band** floppy image (`MusicalBand.flp`) in **VMware Workstation**.

---

## Method A: Instant Launch with Preconfigured VM (Fastest)

We have created a ready-to-run VMware virtual machine configuration file at:
```
C:\FOIDS_CP\VMware\CrimsonOrbit.vmx
```

### Steps:
1. Open **VMware Workstation**.
2. Click **File -> Open...** (or press `Ctrl + O`).
3. Navigate to `C:\FOIDS_CP\VMware\` and select `CrimsonOrbit.vmx`.
4. Click **Power on this virtual machine** (green play button).
5. The virtual machine will boot directly from `..\Builds\MusicalBand.flp`:
   - BIOS loads the MBR bootloader from Sector 1.
   - Bootloader loads the kernel into memory at `1000h:0000h`.
   - The Crimson Orbit welcome screen and intro sound will greet you!

---

## Method B: Creating a Custom Virtual Machine from Scratch

If you prefer to configure a new VM manually in VMware Workstation:

### 1. Create a New Virtual Machine
- Click **File -> New Virtual Machine...**
- Select **Typical (recommended)** -> Next.
- Select **I will install the operating system later** -> Next.
- Guest Operating System: Choose **Other**, Version: **Other** (or **MS-DOS** / **FreeDOS**) -> Next.
- VM Name: `Crimson Orbit - Musical Band`. Location: Any convenient folder -> Next.
- Disk Size: 0.1 GB (or 1 GB, disk is not needed for floppy boot) -> Next.
- Click **Customize Hardware...**

### 2. Configure Virtual Hardware
- **Memory**: Set to `32 MB` or `64 MB`.
- **Processors**: `1 CPU, 1 Core`.
- **Sound Card**:
  - Check **Connect at power on**.
  - Check **Use default host sound card**.
  - *(Crucial: This routes PC Speaker frequency tones to your speakers/headphones).*
- **Add Floppy Drive**:
  1. Click **Add...** at the bottom of the hardware list.
  2. Select **Floppy Drive** -> Finish.
  3. Under Floppy Connection, select **Use floppy image file**.
  4. Browse to:
     ```
     C:\FOIDS_CP\Builds\MusicalBand.flp
     ```
  5. Ensure **Connect at power on** is checked!
- Click **Close**, then click **Finish**.

### 3. Power On and Boot
- Power on the virtual machine.
- If VMware attempts to boot network or hard drive first:
  - Power off the VM.
  - Right-click VM -> **Power -> Power On to Firmware** (BIOS setup).
  - Use arrow keys to navigate to the **Boot** tab.
  - Highlight **Legacy Floppy Drives** and use the `+` key to move it to the top of the boot priority list.
  - Press `F10` to Save and Exit.
- The Crimson Orbit bootloader will now execute, load the kernel, and display the soundstage!

---

## Troubleshooting & Audio Configuration

| Issue | Cause | Solution |
|---|---|---|
| "Operating System not found" | Floppy image not connected | Open VM Settings -> Floppy Drive -> verify "Connect at power on" is checked and path points to `MusicalBand.flp`. |
| No sound during playback | Host PC Speaker audio muted or VM sound device disabled | In VM Settings -> Sound Card -> Ensure "Connected" is checked. Verify host Windows volume is unmuted. |
| Key presses not responding | VMware window doesn't have focus | Click inside the VMware display window to capture keyboard input. Press `Ctrl + Alt` to release mouse. |
