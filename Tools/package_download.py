#!/usr/bin/env python3
import os
import shutil
import zipfile

def main():
    root = r"C:\FOIDS_CP"
    builds = os.path.join(root, "Builds")
    flp_src = os.path.join(builds, "new2.flp")
    kernel_src = os.path.join(builds, "kernel.bin")
    loader_src = os.path.join(builds, "loader.bin")

    user_profile = os.environ.get("USERPROFILE", r"C:\Users\akash")
    downloads_dir = os.path.join(user_profile, "Downloads")
    desktop_dir = os.path.join(user_profile, "Desktop")

    os.makedirs(downloads_dir, exist_ok=True)
    os.makedirs(desktop_dir, exist_ok=True)

    # 1. Direct copy of new2.flp to Downloads
    dst_flp_dl = os.path.join(downloads_dir, "new2.flp")
    shutil.copy2(flp_src, dst_flp_dl)
    print(f"[+] Direct FLP copied to Downloads: {dst_flp_dl} ({os.path.getsize(dst_flp_dl)} bytes)")

    # 2. Package into CrimsonOrbit_new2.zip
    zip_dl = os.path.join(downloads_dir, "CrimsonOrbit_new2.zip")
    zip_desktop = os.path.join(desktop_dir, "CrimsonOrbit_new2.zip")
    zip_builds = os.path.join(builds, "CrimsonOrbit_new2.zip")

    readme_content = """CRIMSON ORBIT - MUSICAL BAND (High-Hertz Acoustic Edition)
============================================================
Included Files:
- new2.flp       : Bootable 1.44 MB Floppy Image (Concert Piano, Singing Guitar, LFSR Drums)
- loader.bin     : 512-byte MBR boot sector with 0x55AA signature
- kernel.bin     : Flat 16-bit binary loaded at 1000h:0000h

How to Run:
1. In VMware Workstation:
   - Create/open virtual machine
   - In Floppy Drive settings, connect 'new2.flp'
   - Power On virtual machine
2. In emu8086:
   - Open Source/kernel.asm -> click Emulate -> click Run
============================================================
"""

    with zipfile.ZipFile(zip_dl, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(flp_src, arcname="new2.flp")
        z.write(kernel_src, arcname="kernel.bin")
        z.write(loader_src, arcname="loader.bin")
        z.writestr("README.txt", readme_content)

    shutil.copy2(zip_dl, zip_desktop)
    shutil.copy2(zip_dl, zip_builds)
    print(f"[+] ZIP package created at: {zip_dl} ({os.path.getsize(zip_dl)} bytes)")
    print(f"[+] ZIP package copied to Desktop: {zip_desktop}")

    # 3. Create an HTML download portal (one-click download in browser)
    import base64
    with open(flp_src, "rb") as f:
        flp_b64 = base64.b64encode(f.read()).decode("ascii")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Download new2.flp - Crimson Orbit</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f0c15;
            color: #f1f1f1;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }}
        .card {{
            background: #1b1625;
            border: 2px solid #e53935;
            border-radius: 16px;
            padding: 40px;
            max-width: 540px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(229, 57, 53, 0.3);
        }}
        h1 {{
            color: #e53935;
            margin-top: 0;
            font-size: 28px;
            letter-spacing: 1px;
        }}
        p {{
            color: #b0bec5;
            line-height: 1.6;
        }}
        .btn {{
            display: inline-block;
            background: linear-gradient(135deg, #e53935, #ffb300);
            color: #000;
            font-weight: bold;
            font-size: 18px;
            padding: 16px 36px;
            border-radius: 8px;
            text-decoration: none;
            cursor: pointer;
            margin: 20px 0;
            transition: transform 0.2s, box-shadow 0.2s;
            border: none;
        }}
        .btn:hover {{
            transform: scale(1.04);
            box-shadow: 0 6px 20px rgba(255, 179, 0, 0.4);
        }}
        .info {{
            font-size: 13px;
            color: #78909c;
            margin-top: 15px;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>CRIMSON ORBIT</h1>
        <p><strong>Musical Band (High-Hertz Acoustic Edition)</strong></p>
        <p>Click below to download <code>new2.flp</code> directly to your computer:</p>
        <a id="dlBtn" class="btn" href="data:application/octet-stream;base64,{flp_b64}" download="new2.flp">
            DOWNLOAD new2.flp (1.44 MB)
        </a>
        <div class="info">
            File: <strong>new2.flp</strong> (1,474,560 bytes)<br>
            Direct download embedded. Ready for VMware, VirtualBox & emu8086.
        </div>
    </div>
    <script>
        // Trigger auto-download when page opens
        window.addEventListener('DOMContentLoaded', () => {{
            const btn = document.getElementById('dlBtn');
            btn.click();
        }});
    </script>
</body>
</html>
"""
    html_dl = os.path.join(downloads_dir, "download_new2.html")
    html_desktop = os.path.join(desktop_dir, "download_new2.html")
    html_builds = os.path.join(builds, "download_new2.html")

    with open(html_dl, "w", encoding="utf-8") as f:
        f.write(html_content)
    with open(html_desktop, "w", encoding="utf-8") as f:
        f.write(html_content)
    with open(html_builds, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] HTML one-click downloader created: {html_desktop}")

if __name__ == "__main__":
    main()
