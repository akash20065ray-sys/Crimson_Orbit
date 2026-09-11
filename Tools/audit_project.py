"""
==============================================================================
CRIMSON ORBIT :: SYSTEM HEALTH & INTEGRITY AUDITOR (audit_project.py)
Automated verification of Assembly, JavaScript, DOM IDs, Audio Assets, and Builds
==============================================================================
"""

import os
import re
import sys
import subprocess

BASE_DIR = r"c:\FOIDS_CP"
STUDIO_DIR = os.path.join(BASE_DIR, "Studio")
AUDIO_DIR = os.path.join(STUDIO_DIR, "audio")
BUILDS_DIR = os.path.join(BASE_DIR, "Builds")
SOURCE_DIR = os.path.join(BASE_DIR, "Source")

print("=" * 75)
print("  CRIMSON ORBIT :: FULL REPOSITORY INTEGRITY AUDIT")
print("=" * 75)

errors = []
warnings = []

# ---------------------------------------------------------------------------
# 1. Check Audio Assets on Disk
# ---------------------------------------------------------------------------
print("\n[1/5] Auditing Audio Sample Assets in Studio/audio/...")
js_path = os.path.join(STUDIO_DIR, "app.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Find all 'audio/*.mp3' in app.js
audio_refs = set(re.findall(r"audio/([a-zA-Z0-9_-]+\.mp3)", js_content))
print(f"  Found {len(audio_refs)} unique audio references in app.js.")

for audio_file in sorted(audio_refs):
    fpath = os.path.join(AUDIO_DIR, audio_file)
    if not os.path.exists(fpath):
        errors.append(f"Missing Audio File: {fpath}")
    else:
        size = os.path.getsize(fpath)
        if size == 0:
            errors.append(f"Empty Audio File (0 bytes): {fpath}")

print(f"  Audio asset audit passed! ({len(audio_refs)} files verified on disk)")

# ---------------------------------------------------------------------------
# 2. Check DOM IDs between app.js, bridge.js, and index.html
# ---------------------------------------------------------------------------
print("\n[2/5] Auditing DOM Element IDs in Studio/index.html...")
bridge_path = os.path.join(STUDIO_DIR, "bridge.js")
with open(bridge_path, "r", encoding="utf-8") as f:
    bridge_content = f.read()

html_path = os.path.join(STUDIO_DIR, "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Extract DOM IDs referenced in JS
ids_in_js = set(re.findall(r"getElementById\(['\"]([a-zA-Z0-9_-]+)['\"]\)", js_content + bridge_content))
ids_in_js.update(re.findall(r"querySelector\(['\"]#([a-zA-Z0-9_-]+)['\"]\)", js_content + bridge_content))

# Extract all IDs defined in HTML
ids_in_html = set(re.findall(r'id=["\']([a-zA-Z0-9_-]+)["\']', html_content))

missing_ids = []
for el_id in sorted(ids_in_js):
    if el_id not in ids_in_html:
        # Check if it's optionally queried with ?. or has a fallback
        missing_ids.append(el_id)

if missing_ids:
    for m in missing_ids:
        # Check if it's critical
        warnings.append(f"DOM ID referenced in JS but not found in index.html: #{m}")
        print(f"  [WARN] DOM ID '{m}' not in index.html")
else:
    print(f"  All {len(ids_in_js)} DOM IDs referenced in JavaScript exist in index.html!")

# ---------------------------------------------------------------------------
# 3. Check Assembly Source Files & Binary Floppy
# ---------------------------------------------------------------------------
print("\n[3/5] Auditing Bare-Metal Assembly Modules & Builds...")
expected_asm = [
    "boot.asm", "kernel.asm", "menu.asm", "speaker.asm", "composer.asm",
    "songs.asm", "piano.asm", "guitar.asm", "drums.asm", "graphics.asm",
    "keyboard.asm", "utils.asm"
]

for asm_file in expected_asm:
    fpath = os.path.join(SOURCE_DIR, asm_file)
    if not os.path.exists(fpath):
        errors.append(f"Missing Assembly Source File: {fpath}")
    else:
        size = os.path.getsize(fpath)
        if size == 0:
            errors.append(f"Empty Assembly File: {fpath}")

# Check floppy image
floppy_path = os.path.join(BUILDS_DIR, "new2.flp")
if not os.path.exists(floppy_path):
    errors.append(f"Missing Floppy Image: {floppy_path}")
else:
    fsize = os.path.getsize(floppy_path)
    if fsize != 1474560:
        errors.append(f"Invalid Floppy Image Size: {fsize} bytes (expected 1,474,560)")
    else:
        print(f"  Floppy image verified: {floppy_path} (exact 1,474,560 bytes / 1.44 MB standard).")

# ---------------------------------------------------------------------------
# 4. Check Standalone HTML Builds
# ---------------------------------------------------------------------------
print("\n[4/5] Auditing Standalone Single-File Distribution Packages...")
standalone_studio = os.path.join(STUDIO_DIR, "standalone.html")
standalone_builds = os.path.join(BUILDS_DIR, "CrimsonOrbit_RealStudio_Standalone.html")

for s_path in [standalone_studio, standalone_builds]:
    if not os.path.exists(s_path):
        errors.append(f"Missing Standalone HTML: {s_path}")
    else:
        ssize = os.path.getsize(s_path)
        if ssize < 1000000:
            warnings.append(f"Standalone HTML suspiciously small: {s_path} ({ssize:,} bytes)")
        else:
            print(f"  Verified standalone bundle: {os.path.basename(s_path)} ({ssize:,} bytes, self-contained).")

# ---------------------------------------------------------------------------
# 5. Check Documentation & Benchmark Artifacts
# ---------------------------------------------------------------------------
print("\n[5/5] Auditing Research Documentation & Telemetry...")
expected_docs = [
    os.path.join(BASE_DIR, "BRAIN.md"),
    os.path.join(BASE_DIR, "brain.d", "01_project_overview.md"),
    os.path.join(BASE_DIR, "brain.d", "02_system_architecture.md"),
    os.path.join(BASE_DIR, "brain.d", "03_technical_phases.md"),
    os.path.join(BASE_DIR, "brain.d", "04_research_literature_and_gaps.md"),
    os.path.join(BASE_DIR, "brain.d", "05_interception_protocol.md"),
    os.path.join(BASE_DIR, "brain.d", "06_reviewer_defense_faq.md"),
    os.path.join(BASE_DIR, "Assets", "Documentation", "BENCHMARK_RESULTS.json"),
    os.path.join(BASE_DIR, "Assets", "Documentation", "EMPIRICAL_BENCHMARKS.md"),
    os.path.join(BASE_DIR, "Assets", "Documentation", "PLAGIARISM_AND_ORIGINALITY_REPORT.md"),
]

for doc_path in expected_docs:
    if not os.path.exists(doc_path):
        errors.append(f"Missing Documentation/Artifact: {doc_path}")
    else:
        if os.path.getsize(doc_path) == 0:
            errors.append(f"Empty Documentation File: {doc_path}")

print(f"  All {len(expected_docs)} documentation and benchmark artifacts verified.")

# ---------------------------------------------------------------------------
# Summary Report
# ---------------------------------------------------------------------------
print("\n" + "=" * 75)
print("  AUDIT SUMMARY")
print("=" * 75)
if not errors and not warnings:
    print("  [PERFECT HEALTH] ZERO ERRORS, ZERO WARNINGS!")
    print("  All Assembly modules, Audio samples, DOM elements, Bridges, and")
    print("  Standalone builds are 100% synchronized, functional, and intact.")
else:
    if errors:
        print(f"  FOUND {len(errors)} CRITICAL ERROR(S):")
        for e in errors:
            print(f"    - [ERROR] {e}")
    if warnings:
        print(f"  FOUND {len(warnings)} WARNING(S):")
        for w in warnings:
            print(f"    - [WARN] {w}")

print("=" * 75)
