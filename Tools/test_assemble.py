#!/usr/bin/env python3
"""
Test Assembler Tool using emu8086 internal FASM engine.
Validates all syntax and builds loader.bin, kernel.bin, and MusicalBand.flp.
"""

import os
import re
import subprocess
import sys

FASM_PATH = r"C:\emu8086\fasm\FASM.EXE"

def prepare_file(src_path, dst_path, is_boot=False):
    with open(src_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    clean_lines = []
    for line in lines:
        stripped = line.strip()
        # Remove emu8086 directives starting and ending with #
        if re.match(r"^#[^#]+#", stripped):
            clean_lines.append("; " + line)
        elif re.match(r"^\s*(\w+)\s+proc\b", line, re.IGNORECASE):
            # Translate 'ProcName proc' to 'ProcName:'
            clean_lines.append(re.sub(r"^\s*(\w+)\s+proc\b.*", r"\1:", line, flags=re.IGNORECASE))
        elif re.match(r"^\s*\w+\s+endp\b", line, re.IGNORECASE):
            # Comment out 'endp'
            clean_lines.append("; " + line)
        else:
            clean_lines.append(line)

    with open(dst_path, "w", encoding="utf-8") as f:
        f.writelines(clean_lines)

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_dir = os.path.join(root, "Source")
    builds_dir = os.path.join(root, "Builds")
    temp_dir = os.path.join(root, "Builds", "temp")
    os.makedirs(temp_dir, exist_ok=True)

    print("=" * 60)
    print("   CRIMSON ORBIT :: SYNTAX & ASSEMBLY VERIFIER")
    print("=" * 60)

    # 1. Prepare bootloader
    boot_src = os.path.join(source_dir, "boot.asm")
    boot_tmp = os.path.join(temp_dir, "boot_clean.asm")
    loader_bin = os.path.join(builds_dir, "loader.bin")
    prepare_file(boot_src, boot_tmp, is_boot=True)

    print("[*] Assembling bootloader...")
    res = subprocess.run([FASM_PATH, boot_tmp, loader_bin], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print(res.stderr)
    if res.returncode != 0:
        print("[FAIL] Bootloader assembly failed!")
        return 1
    print("[PASS] Bootloader assembled successfully!")

    # 2. Prepare kernel and included modules
    # In order for kernel.asm to include files from Source, we can copy all Source/*.asm to temp_dir
    # with directives commented out.
    for fname in os.listdir(source_dir):
        if fname.endswith(".asm"):
            s_path = os.path.join(source_dir, fname)
            d_path = os.path.join(temp_dir, fname)
            prepare_file(s_path, d_path)

    kernel_tmp = os.path.join(temp_dir, "kernel.asm")
    kernel_bin = os.path.join(builds_dir, "kernel.bin")

    print("\n[*] Assembling kernel and all modules...")
    res = subprocess.run([FASM_PATH, kernel_tmp, kernel_bin], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print(res.stderr)
    if res.returncode != 0:
        print("[FAIL] Kernel assembly failed!")
        return 1
    print("[PASS] Kernel and all modules assembled successfully!")

    # 3. Build Floppy Image
    print("\n[*] Generating MusicalBand.flp...")
    build_floppy_script = os.path.join(root, "Tools", "build_floppy.py")
    res = subprocess.run([sys.executable, build_floppy_script], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("[FAIL] Floppy build failed!")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
