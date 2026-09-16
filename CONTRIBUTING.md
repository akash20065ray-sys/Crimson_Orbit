# Contributing to Crimson Orbit

Thank you for your interest in contributing to **Crimson Orbit**! This repository unites 16-bit real-mode x86 bare-metal assembly, microsecond bus-cycle serialization, and high-performance WebAudio DSP.

---

## 🛠️ Development & Tooling Requirements

- **Assembler**: [NASM](https://www.nasm.us/) or [emu8086](http://www.emu8086.com/)
- **Virtualization**: [QEMU](https://www.qemu.org/) (`qemu-system-i386`) or VMware Workstation / VirtualBox
- **Python**: 3.9+ (for build scripts, benchmark verification, and standalone bundling)
- **Web Browser**: Chrome / Edge / Firefox / Safari (supporting WebAudio API & AudioWorklet)

---

## 📋 Architectural Guidelines

When submitting contributions or modifications, adhere to these constraints:

### 1. 16-Bit Real-Mode Assembly (`Source/`)
- Code executes directly in 16-bit real mode. **Do not use 32-bit protected-mode or 64-bit long-mode instructions.**
- Adhere strictly to the memory layout:
  - `0000:7C00h`: 512-Byte MBR Bootloader (`boot.asm`)
  - `1000:0000h`: Flat Kernel Execution Segment (`kernel.asm`)
- Hardware timers (Intel 8253 PIT) and speaker ports (Intel 8255 PPI Port 61h) must be driven directly without relying on MS-DOS interrupts (`INT 21h`).

### 2. Digital Audio Workstation (`Studio/`)
- AudioWorklet code must remain non-blocking; never allocate memory dynamically within high-frequency audio rendering loops.
- Maintain support for both **Mode A (1-Bit Authentic Square Wave)** and **Mode B (Acoustic Resynthesis)**.
- If modifying the Studio interface, test both `Studio/index.html` and verify the single-file distribution via `python Tools/build_standalone_studio.py`.

### 3. Verification & Auditing
Before opening a Pull Request, run the automated repository integrity audit:
```bash
python Tools/audit_project.py
```
Ensure all 5 audit stages pass with **0 errors and 0 warnings**.

---

## 🔀 Pull Request Workflow

1. Fork the repository and create your branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Commit your changes with descriptive, conventional commit messages:
   ```bash
   git commit -m "feat(assembly): optimize LFSR pseudo-random noise routine"
   ```
3. Push to your branch and open a Pull Request against the `main` branch.
4. Describe your changes, specify the hardware/emulator tested on, and verify the audit status.

---

## 📜 Code of Conduct
All contributors are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).
