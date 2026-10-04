#!/usr/bin/env python3
"""
CRIMSON ORBIT :: PRESENTATION SCRIPT PDF GENERATOR
=============================================================================
Converts PRESENTATION_SLIDES_AND_SCRIPT.md into a high-quality A4 PDF
using Microsoft Edge headless printing.
Saves to:
  - Assets/Documentation/CrimsonOrbit_Presentation_Script.pdf
  - C:/Users/akash/Desktop/CrimsonOrbit_Presentation_Script.pdf
=============================================================================
"""

import os
import re
import shutil
import subprocess

SCRIPT_MD = "Assets/Documentation/PRESENTATION_SLIDES_AND_SCRIPT.md"
HTML_OUT = "Assets/Documentation/CrimsonOrbit_Presentation_Script.html"
PDF_OUT = "Assets/Documentation/CrimsonOrbit_Presentation_Script.pdf"
DESKTOP_PDF = os.path.expanduser(r"~\Desktop\CrimsonOrbit_Presentation_Script.pdf")

def parse_markdown_to_html(md_text):
    # Split into sections
    lines = md_text.splitlines()
    html_parts = []
    
    in_table = False
    table_lines = []
    in_quote = False
    quote_lines = []
    
    def flush_table():
        nonlocal in_table, table_lines
        if not table_lines:
            return ""
        out = ["<table class='script-table'>"]
        header_done = False
        for l in table_lines:
            if "---" in l:
                header_done = True
                continue
            cells = [c.strip() for c in l.strip("|").split("|")]
            tag = "th" if not header_done else "td"
            row = "<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in cells) + "</tr>"
            out.append(row)
        out.append("</table>")
        in_table = False
        table_lines = []
        return "\n".join(out)
        
    def flush_quote():
        nonlocal in_quote, quote_lines
        if not quote_lines:
            return ""
        out = "<div class='speech-card'>" + "\n".join(quote_lines) + "</div>"
        in_quote = False
        quote_lines = []
        return out

    for line in lines:
        # Table detection
        if line.strip().startswith("|") and line.strip().endswith("|"):
            if in_quote:
                html_parts.append(flush_quote())
            in_table = True
            table_lines.append(line)
            continue
        elif in_table:
            html_parts.append(flush_table())
            
        # Blockquote / Speech detection
        if line.startswith(">"):
            in_quote = True
            content = line.lstrip("> ").strip()
            # formatting
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
            quote_lines.append(f"<p>{content}</p>")
            continue
        elif in_quote:
            html_parts.append(flush_quote())
            
        # Headers
        if line.startswith("# "):
            title = line[2:].strip()
            html_parts.append(f"<h1 class='doc-title'>{title}</h1>")
        elif line.startswith("## "):
            h2 = line[3:].strip()
            if "Slide " in h2:
                # Add speaker pill if present
                html_parts.append(f"<div class='slide-header'><h2>{h2}</h2></div>")
            else:
                html_parts.append(f"<h2 class='section-title'>{h2}</h2>")
        elif line.startswith("### "):
            h3 = line[4:].strip()
            h3 = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', h3)
            html_parts.append(f"<h3 class='sub-title'>{h3}</h3>")
        elif line.startswith("- "):
            item = line[2:].strip()
            item = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item)
            item = re.sub(r'\*(.*?)\*', r'<em>\1</em>', item)
            item = re.sub(r'`(.*?)`', r'<code>\1</code>', item)
            html_parts.append(f"<li class='bullet-item'>{item}</li>")
        elif line.strip() == "---":
            html_parts.append("<hr class='divider' />")
        elif line.strip():
            p = line.strip()
            p = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p)
            p = re.sub(r'\*(.*?)\*', r'<em>\1</em>', p)
            p = re.sub(r'`(.*?)`', r'<code>\1</code>', p)
            html_parts.append(f"<p class='body-text'>{p}</p>")

    if in_table:
        html_parts.append(flush_table())
    if in_quote:
        html_parts.append(flush_quote())
        
    return "\n".join(html_parts)

def build_pdf():
    with open(SCRIPT_MD, "r", encoding="utf-8") as f:
        md_text = f.read()

    body_html = parse_markdown_to_html(md_text)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Crimson Orbit :: Master Defense Presentation Script</title>
<style>
  @page {{
    size: A4;
    margin: 14mm 16mm 14mm 16mm;
    @bottom-center {{
      content: "Page " counter(page);
      font-size: 8pt;
      color: #64748B;
    }}
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #0F172A;
    background-color: #FFFFFF;
    line-height: 1.45;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }}

  .doc-title {{
    color: #991B1B;
    font-size: 18pt;
    font-weight: 800;
    margin: 0 0 4px 0;
    letter-spacing: -0.5px;
    border-bottom: 2px solid #DC2626;
    padding-bottom: 4px;
  }}

  .section-title {{
    color: #0F172A;
    font-size: 13pt;
    font-weight: 700;
    margin: 16px 0 8px 0;
    border-left: 4px solid #DC2626;
    padding-left: 8px;
    background: #F8FAFC;
    padding-top: 3px;
    padding-bottom: 3px;
  }}

  .slide-header {{
    background: #0F172A;
    color: #FFFFFF;
    padding: 6px 12px;
    border-radius: 6px;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
    break-after: avoid;
  }}

  .slide-header h2 {{
    color: #F8FAFC;
    font-size: 11pt;
    margin: 0;
    font-weight: 700;
  }}

  .sub-title {{
    color: #DC2626;
    font-size: 10.5pt;
    font-weight: 700;
    margin: 8px 0 4px 0;
  }}

  .body-text {{
    margin: 4px 0;
    color: #334155;
    font-size: 9.5pt;
  }}

  .bullet-item {{
    margin: 2px 0 2px 16px;
    color: #1E293B;
    font-size: 9pt;
  }}

  .speech-card {{
    background: #FFF5F5;
    border-left: 4px solid #DC2626;
    border-top: 1px solid #FECACA;
    border-right: 1px solid #FECACA;
    border-bottom: 1px solid #FECACA;
    border-radius: 0 6px 6px 0;
    padding: 8px 12px;
    margin: 6px 0 10px 0;
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  .speech-card p {{
    margin: 4px 0;
    color: #1E293B;
    font-size: 9.5pt;
    line-height: 1.45;
  }}

  .speech-card strong {{
    color: #991B1B;
  }}

  .script-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  .script-table th {{
    background: #0F172A;
    color: #F8FAFC;
    padding: 6px 8px;
    text-align: left;
    font-weight: 700;
    border: 1px solid #334155;
  }}

  .script-table td {{
    padding: 5px 8px;
    border: 1px solid #CBD5E1;
    color: #1E293B;
    vertical-align: top;
  }}

  .script-table tr:nth-child(even) {{
    background: #F8FAFC;
  }}

  code {{
    background: #F1F5F9;
    color: #0F172A;
    padding: 1px 4px;
    border-radius: 3px;
    font-family: Consolas, monospace;
    font-size: 8.5pt;
    border: 1px solid #E2E8F0;
  }}

  .divider {{
    border: 0;
    border-top: 1px dashed #CBD5E1;
    margin: 12px 0;
  }}
</style>
</head>
<body>
{body_html}
</body>
</html>
"""

    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Generated HTML intermediate at: {HTML_OUT}")

    # Compile with Edge Headless
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    edge_exe = None
    for p in edge_paths:
        if os.path.exists(p):
            edge_exe = p
            break

    if not edge_exe:
        print("Error: Microsoft Edge executable not found.")
        return

    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={os.path.abspath(PDF_OUT)}",
        os.path.abspath(HTML_OUT)
    ]
    print("Compiling PDF with Edge Headless...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Successfully compiled PDF: {PDF_OUT} ({os.path.getsize(PDF_OUT)} bytes)")
        shutil.copy(PDF_OUT, DESKTOP_PDF)
        print(f"Copied Script PDF to Desktop: {DESKTOP_PDF} ({os.path.getsize(DESKTOP_PDF)} bytes)")
    else:
        print(f"PDF compilation failed: {res.stderr}")

if __name__ == "__main__":
    build_pdf()
