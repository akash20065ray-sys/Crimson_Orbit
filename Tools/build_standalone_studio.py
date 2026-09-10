"""
Build Standalone Single-File Real Studio Workstation
Bundles HTML, CSS, JavaScript, and all 28 real MP3 instrument recordings into a single portable HTML file.
Zero-dependency, zero-server, zero-CORS restriction.
"""

import os
import base64
import sys

BASE_DIR = r"c:\FOIDS_CP"
STUDIO_DIR = os.path.join(BASE_DIR, "Studio")
AUDIO_DIR = os.path.join(STUDIO_DIR, "audio")
DESKTOP_DIR = r"C:\Users\akash\Desktop"
BUILDS_DIR = os.path.join(BASE_DIR, "Builds")

print("Building Standalone Studio Workstation...")

# 1. Read index.html
html_path = os.path.join(STUDIO_DIR, "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# 2. Read style.css
css_path = os.path.join(STUDIO_DIR, "style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

# 3. Read bridge.js & app.js
bridge_path = os.path.join(STUDIO_DIR, "bridge.js")
bridge_content = ""
if os.path.exists(bridge_path):
    with open(bridge_path, "r", encoding="utf-8") as f:
        bridge_content = f.read()

js_path = os.path.join(STUDIO_DIR, "app.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# 4. Encode all 28 audio files to base64
print("Encoding 28 real acoustic audio samples to base64 Data URLs...")
audio_dict = {}
for fname in sorted(os.listdir(AUDIO_DIR)):
    if fname.endswith(".mp3"):
        fpath = os.path.join(AUDIO_DIR, fname)
        with open(fpath, "rb") as af:
            b64_data = base64.b64encode(af.read()).decode("ascii")
            data_url = f"data:audio/mp3;base64,{b64_data}"
            # Mapping key matches the sampleUrls in app.js
            # E.g. piano_C4.mp3 -> 'piano_C4', guitar_chord1.mp3 -> 'chord_em', etc.
            key = os.path.splitext(fname)[0]
            audio_dict[key] = data_url

print(f"Encoded {len(audio_dict)} audio files successfully.")

# Map exact keys used in app.js
sample_mapping = {}
for key, data_url in audio_dict.items():
    if key.startswith("piano_"):
        sample_mapping[key] = data_url
    elif key == "guitar_E2":
        sample_mapping['guitar_6'] = data_url
    elif key == "guitar_A2":
        sample_mapping['guitar_5'] = data_url
    elif key == "guitar_D3":
        sample_mapping['guitar_4'] = data_url
    elif key == "guitar_G3":
        sample_mapping['guitar_3'] = data_url
    elif key == "guitar_B3":
        sample_mapping['guitar_2'] = data_url
    elif key == "guitar_E4":
        sample_mapping['guitar_1'] = data_url
    elif key == "guitar_chord1":
        sample_mapping['chord_em'] = data_url
        sample_mapping['chord_d'] = data_url
    elif key == "guitar_chord2":
        sample_mapping['chord_g'] = data_url
    elif key == "guitar_chord3":
        sample_mapping['chord_c'] = data_url
    elif key.startswith("drum_"):
        sample_mapping[key] = data_url

# Construct embedded JS dictionary
import json
json_samples = json.dumps(sample_mapping)

# Replace this.sampleUrls in js_content with json_samples
# In app.js:
# this.sampleUrls = { ... };
start_marker = "this.sampleUrls = {"
end_marker = "};"

start_idx = js_content.find(start_marker)
if start_idx != -1:
    end_idx = js_content.find(end_marker, start_idx) + len(end_marker)
    js_content_embedded = js_content[:start_idx] + f"this.sampleUrls = {json_samples};" + js_content[end_idx:]
else:
    print("Warning: Could not find sampleUrls block in app.js")
    js_content_embedded = js_content

# Replace link to stylesheet with inline <style>
html_content = html_content.replace(
    '<link rel="stylesheet" href="style.css">',
    f'<style>\n{css_content}\n</style>'
)

# Replace script tags with inline <script>
if bridge_content:
    html_content = html_content.replace(
        '<script src="bridge.js"></script>',
        f'<script>\n{bridge_content}\n</script>'
    )
else:
    html_content = html_content.replace('<script src="bridge.js"></script>', '')

html_content = html_content.replace(
    '<script src="app.js"></script>',
    f'<script>\n{js_content_embedded}\n</script>'
)

# Write to outputs
out_studio = os.path.join(STUDIO_DIR, "standalone.html")
with open(out_studio, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Saved: {out_studio} ({len(html_content):,} bytes)")

out_desktop = os.path.join(DESKTOP_DIR, "CrimsonOrbit_RealStudio_Standalone.html")
try:
    with open(out_desktop, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Saved: {out_desktop} ({len(html_content):,} bytes)")
except Exception as e:
    print(f"Desktop write warning: {e}")

out_builds = os.path.join(BUILDS_DIR, "CrimsonOrbit_RealStudio_Standalone.html")
with open(out_builds, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Saved: {out_builds} ({len(html_content):,} bytes)")

print("Standalone build complete!")
