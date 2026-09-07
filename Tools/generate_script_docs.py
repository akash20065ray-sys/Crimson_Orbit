#!/usr/bin/env python3
"""
CRIMSON ORBIT – MUSICAL BAND & REAL STUDIO WORKSTATION
Simplified Presentation Script Generator (generate_script_docs.py)
Generates both PDF and DOCX presentation scripts for the 5-member team:
- Simple, everyday student language (no heavy technical jargon or chip names).
- Focus on emu8086 (8086 emulator) and Web Studio (HTML, CSS, JavaScript).
- Clear story of research, workflow, and how we decided to build this.
- Sourcing of real sounds: Steinway piano, Martin guitar, Ludwig drums.
- Each member speaks EXACTLY ONCE + simple 30-second teacher defense answers.
"""

import os
import sys
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)

try:
    from docx import Document
    from docx.shared import Pt as DocxPt, Inches as DocxInches, RGBColor as DocxRGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

def build_pdf(pdf_path):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#C62828'),
        alignment=1,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#E65100'),
        alignment=1,
        spaceAfter=6
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#455A64'),
        alignment=1,
        spaceAfter=10
    )

    member_header_style = ParagraphStyle(
        'MemberHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#FFFFFF')
    )

    role_style = ParagraphStyle(
        'MemberRole',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#B71C1C'),
        spaceAfter=5
    )

    speech_label_style = ParagraphStyle(
        'SpeechLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#0D47A1'),
        spaceBefore=2,
        spaceAfter=2
    )

    speech_body_style = ParagraphStyle(
        'SpeechBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.2,
        leading=13.8,
        textColor=colors.HexColor('#212121'),
        spaceAfter=5
    )

    qa_title_style = ParagraphStyle(
        'QATitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#B71C1C'),
        spaceAfter=2
    )

    qa_body_style = ParagraphStyle(
        'QABody',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#263238')
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("CRIMSON ORBIT – MUSICAL BAND & REAL SOUND STUDIO", title_style))
    story.append(Paragraph("Vishwakarma Institute of Technology, Pune • Group - 9", subtitle_style))
    story.append(Paragraph("<b>Guide:</b> Prof. Gopal Upadhye | <b>Primary Platform:</b> emu8086 | <b>Extension:</b> HTML/CSS/JS Studio | <b>Rule:</b> Each Member Speaks Once", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#C62828'), spaceAfter=10))

    # Order Table
    table_data = [
        [Paragraph("<b>Speaker & Roll No.</b>", styles['Normal']), Paragraph("<b>Assigned Role & Contributions</b>", styles['Normal']), Paragraph("<b>Time</b>", styles['Normal'])],
        [Paragraph("<b>1. Akash Kumar</b><br/>(Roll No. 9)", styles['Normal']), Paragraph("Project Leader, Research & Workflow, emu8086 Piano Module & Real Steinway Piano in Web Studio", styles['Normal']), Paragraph("~2.0 min", styles['Normal'])],
        [Paragraph("<b>2. Bhargude Sanskar</b><br/>(Roll No. 38)", styles['Normal']), Paragraph("Acoustic Guitar Module in emu8086 (6 Strings & Chords) + Martin Guitar Fretboard in Web Studio", styles['Normal']), Paragraph("~1.5 min", styles['Normal'])],
        [Paragraph("<b>3. Aher Krishna</b><br/>(Roll No. 7)", styles['Normal']), Paragraph("Drums Module in emu8086 (Noise Generator & 5 Drum Sounds) + 3D Ludwig Drum Kit in Web Studio", styles['Normal']), Paragraph("~1.5 min", styles['Normal'])],
        [Paragraph("<b>4. Hari Birare</b><br/>(Roll No. 49)", styles['Normal']), Paragraph("Songs Repertoire Architecture (songs.asm), Note Timings & Connecting Songs to Web Studio", styles['Normal']), Paragraph("~1.0 min", styles['Normal'])],
        [Paragraph("<b>5. Agaldare Ghansham</b><br/>(Roll No. 4)", styles['Normal']), Paragraph("Jukebox Song Player in emu8086, Visualizer Bars, [ESC] Key + Moving Sound Equalizer in Web Studio", styles['Normal']), Paragraph("~1.5 min", styles['Normal'])],
        [Paragraph("<b>6. Akash Kumar</b><br/>(Closing & Demo)", styles['Normal']), Paragraph("Project Assembling, Explaining Why We Made Both emu8086 & Web Studio, and Live Demonstration", styles['Normal']), Paragraph("~1.5 min", styles['Normal'])],
    ]
    t = Table(table_data, colWidths=[110, 370, 60])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#ECEFF1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CFD8DC')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    members = [
        {
            "name": "SPEAKER 1: AKASH",
            "role": "PROJECT LEADER — IDEA, RESEARCH, WORKFLOW & CONCERT PIANO",
            "speech": (
                "\"Good morning/afternoon, Respected Professor and classmates. Our course project is "
                "<b>Crimson Orbit – Musical Band</b>, developed and tested using the <b>emu8086 emulator</b>.<br/><br/>"
                "<b>How We Started & Our Research Workflow:</b><br/>"
                "When starting our microprocessor project, I wanted our team to build an interactive, fun musical application instead of a basic calculator. "
                "I researched how 8086 computers produce sound and discovered that <b>emu8086 can control the computer's PC speaker</b> directly by sending output signals to the sound ports. "
                "By dividing the clock frequency by musical notes, we can make the PC speaker play exact musical tones.<br/><br/>"
                "However, while testing in emu8086, we noticed an obvious problem: the PC speaker can only make <b>electronic beeps and buzzes</b>. It cannot play real instrument sounds like a genuine acoustic piano or guitar. "
                "So our team decided on a clear workflow: <b>we will create two connected parts for our project</b>. "
                "First, we wrote the full assembly language code in emu8086 to prove low-level hardware control. "
                "Second, we built a modern Web Studio using <b>HTML, CSS, and JavaScript</b>, where we added <b>28 real studio recordings</b> of real instruments so our band sounds completely real.<br/><br/>"
                "In emu8086, I built the <b>Concert Piano module (<code>piano.asm</code>)</b>, drawing 3D white and black keys that press down when you type Q through I on your keyboard, with an octave switcher and a sustain pedal. "
                "In our HTML and JavaScript studio, I integrated <b>real recordings of a Steinway Grand Piano</b>, so when you click the keys, it plays authentic concert piano music.<br/><br/>"
                "I will now pass the presentation to Sanskar to explain the Guitar module.\""
            ),
            "qa": (
                "<b>Teacher:</b> <i>\"Akash, what was your role and how did you decide on this project?\"</i><br/>"
                "<b>Your Answer:</b> \"Sir/Ma'am, I led the project research and workflow. I researched how emu8086 controls the PC speaker to play music. Because the PC speaker only gives basic beeps, I decided we should build the assembly code in emu8086 and also create a realistic Web Studio in HTML, CSS, and JavaScript with real recorded instruments. I programmed the Piano in assembly, added real Steinway piano sounds to the web studio, and assembled the whole team's work together.\""
            )
        },
        {
            "name": "SPEAKER 2: SANSKAR",
            "role": "ACOUSTIC GUITAR MODULE (EMU8086 ASSEMBLY & WEB STUDIO FRETBOARD)",
            "speech": (
                "\"Thank you, Akash. I designed and coded the <b>Acoustic Guitar module (<code>guitar.asm</code>)</b> in emu8086, and helped create the guitar interface in HTML, CSS, and JavaScript.<br/><br/>"
                "In emu8086 assembly, I wanted the guitar to feel like a real instrument rather than flat beeps. I programmed all <b>6 guitar strings from Low E to High E</b>. "
                "To make it sound like an acoustic string, I added a <b>pick strike chirp effect</b> when you pluck any string using keys Q through Y, followed by a gentle <b>finger vibrato effect</b> where the sound wobbles naturally. "
                "I also programmed the <b><code>[S]</code> key to strum a full acoustic chord</b> across all strings.<br/><br/>"
                "In our HTML, CSS, and JavaScript studio, I brought this guitar to life visually. "
                "We searched online and downloaded <b>real acoustic guitar recordings of a Martin D-28 guitar</b>: all 6 open strings plus strummed acoustic chords for E minor, G major, C major, and D major. "
                "When you click or press strings in the web studio, the strings physically vibrate on screen using CSS animations, and it plays authentic acoustic guitar sounds.<br/><br/>"
                "I will now hand over to Krishna to present the Drums module.\""
            ),
            "qa": (
                "<b>Teacher:</b> <i>\"Sanskar, what did you do for the guitar?\"</i><br/>"
                "<b>Your Answer:</b> \"Sir/Ma'am, in emu8086 assembly, I coded the 6 guitar strings, added pick strike sound effects, singing vibrato, and full chord strumming on key [S]. In HTML, CSS, and JavaScript, I built the guitar fretboard with vibrating strings and connected it to real Martin acoustic guitar recordings so it sounds authentic.\""
            )
        },
        {
            "name": "SPEAKER 3: KRISHNA",
            "role": "DRUMS MODULE (EMU8086 NOISE GENERATOR & WEB STUDIO 3D DRUMS)",
            "speech": (
                "\"Thank you, Sanskar. I developed the <b>Drum Kit module (<code>drums.asm</code>)</b> in emu8086, and built the 3D drum kit stage in HTML, CSS, and JavaScript.<br/><br/>"
                "The biggest challenge in emu8086 was that the PC speaker only plays musical tones—it cannot naturally make drum noise like snares or cymbals. "
                "To solve this in assembly, I created a <b>random white noise generator in 8086 code</b>. "
                "Using this noise generator, I created 5 distinct drum sounds in emu8086: a deep <b>Kick Drum</b> that drops rapidly in pitch for an acoustic thump, a <b>Snare Drum</b> that blends white noise with a wooden shell sound, crisp <b>Hi-Hats</b>, and a shimmering <b>Crash Cymbal</b>.<br/><br/>"
                "In our HTML, CSS, and JavaScript studio, I connected these drums to <b>real close-miked studio recordings of a Ludwig Drum Kit</b>. "
                "I designed the circular 3D drum pads so when you hit keys Q, W, E, R, or T, the drum pads light up with expanding shockwaves and play punchy, realistic studio drum beats.<br/><br/>"
                "I will now pass to Hari to explain our Pre-Installed Songs.\""
            ),
            "qa": (
                "<b>Teacher:</b> <i>\"Krishna, how did you make drum sounds on a PC speaker?\"</i><br/>"
                "<b>Your Answer:</b> \"Sir/Ma'am, because a PC speaker can only make musical tones, I wrote a random noise generator in 8086 assembly to create white noise for the snare and cymbals, and used quick frequency drops for the kick drum thump. In the HTML/CSS/JS studio, I connected these pads to real Ludwig drum kit recordings with moving shockwave animations.\""
            )
        },
        {
            "name": "SPEAKER 4: HARI",
            "role": "SONGS REPERTOIRE (EMU8086 TIMING & WEB AUDIO NOTE TABLES)",
            "speech": (
                "\"Thank you, Krishna. Ghansham and I worked together on the <b>Pre-Installed Songs module (<code>songs.asm</code>)</b> in emu8086, and connected our music into the JavaScript Web Studio.<br/><br/>"
                "In emu8086 assembly, I stored the musical notes and timing for <b>6 famous songs</b>: "
                "<i>Happy Birthday</i>, <i>Twinkle Twinkle Little Star</i>, <i>Ode to Joy</i>, <i>Jingle Bells</i>, <i>Mary Had a Little Lamb</i>, and <i>London Bridge</i>. "
                "Each note is stored as two numbers: the note frequency and how long it should play. "
                "I used timer delay loops so every song plays at a steady, natural musical tempo.<br/><br/>"
                "In our HTML and JavaScript studio, I mapped these exact same song notes into our JavaScript audio player. "
                "This allows our web studio to play all 6 songs using the real Steinway piano, Martin guitar, or Ludwig drum beat across multiple octaves with 100% accurate pitch.<br/><br/>"
                "I will now pass to Ghansham to explain the Jukebox player and visualizer.\""
            ),
            "qa": (
                "<b>Teacher:</b> <i>\"Hari, what was your role in the songs module?\"</i><br/>"
                "<b>Your Answer:</b> \"Sir/Ma'am, in emu8086 assembly, I encoded the musical notes and delay timings for 6 classic songs, calibrating the timer loops so songs play at steady tempo. In JavaScript, I mapped these same notes so they trigger real piano, guitar, or drum sounds in the web studio.\""
            )
        },
        {
            "name": "SPEAKER 5: GHANSHAM",
            "role": "JUKEBOX PLAYER & VISUALIZER (EMU8086 & HTML5 SPECTRUM EQUALIZER)",
            "speech": (
                "\"Thank you, Hari. Building on Hari's song notes, I created the <b>Jukebox Song Player and Moving Visualizers</b> in both emu8086 and HTML/CSS/JavaScript.<br/><br/>"
                "In emu8086 assembly (<code>songs.asm</code>), I wrote the automatic player that reads through the song notes, sends sound to the PC speaker, and animates <b>8 colorful equalizer bars</b> bouncing up and down on screen. "
                "I also made sure that pressing the <b><code>[ESC]</code> key stops the song immediately</b> and returns cleanly to the main menu without freezing the emulator.<br/><br/>"
                "In our HTML and JavaScript studio, I upgraded this into a <b>Real-Time 60 FPS Moving Spectrum Equalizer</b>. "
                "As songs play, colorful visualizer bars jump up and down to the music and display live frequency numbers. "
                "Users can also click buttons to hear any song played on Real Grand Piano, Real Acoustic Guitar, or a Rock Drum Beat.<br/><br/>"
                "I will now pass back to Akash to present our system assembling and live demonstration.\""
            ),
            "qa": (
                "<b>Teacher:</b> <i>\"Ghansham, what did you build for the song player?\"</i><br/>"
                "<b>Your Answer:</b> \"Sir/Ma'am, in emu8086 assembly, I built the automatic jukebox player that plays through songs, animated 8 text visualizer bars on screen, and added [ESC] key support to stop playback anytime. In HTML and JavaScript, I built the colorful moving spectrum equalizer that dances in real time to the music.\""
            )
        },
        {
            "name": "SPEAKER 6: AKASH (CLOSING & DEMO)",
            "role": "PROJECT ASSEMBLING & LIVE DEMONSTRATION",
            "speech": (
                "\"Thank you, Ghansham. To conclude our presentation, I will explain how we assembled the complete project and how to run it.<br/><br/>"
                "<b>How We Assembled Everything:</b><br/>"
                "In emu8086, I linked all our team files together inside <code>kernel.asm</code> using <code>include</code> statements: bringing together <code>piano.asm</code>, <code>guitar.asm</code>, <code>drums.asm</code>, and <code>songs.asm</code> into one cohesive program. "
                "You can run it directly in emu8086 by opening <code>kernel.asm</code>, clicking <b>Emulate</b>, and clicking <b>Run</b>.<br/><br/>"
                "To make our Web Studio equally easy to run, I compiled the HTML, CSS, JavaScript, and all <b>28 real instrument recordings into a single standalone file: <code>CrimsonOrbit_RealStudio.html</code></b>. "
                "It sits right in our Downloads and Desktop folder. You just double-click it, and it immediately opens in Chrome or Edge, playing real Steinway piano, Martin guitar, and Ludwig drums completely offline.<br/><br/>"
                "We will now demonstrate both: first our assembly code running in emu8086, and then our Real Sound Studio. "
                "Thank you, Professor, and we are ready for your questions!\""
            ),
            "qa": (
                "<b>Teacher:</b> <i>\"Why does your project have both emu8086 assembly and an HTML/CSS/JS file?\"</i><br/>"
                "<b>Your Answer:</b> \"Professor, our core project is 100% written in 8086 assembly language running in emu8086. But because the PC speaker in emu8086 only makes electronic beeps, we also built the HTML, CSS, and JavaScript studio to show how our exact assembly music sounds with real studio-recorded instruments like Steinway piano and Martin guitar. This proves we mastered both low-level assembly and modern audio presentation!\""
            )
        }
    ]

    for m in members:
        card_content = []
        header_table = Table([[Paragraph(f"<b>{m['name']}</b>", member_header_style)]], colWidths=[540])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#C62828')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        card_content.append(header_table)
        card_content.append(Spacer(1, 3))
        card_content.append(Paragraph(f"<b>ASSIGNED ROLE:</b> {m['role']}", role_style))
        card_content.append(Paragraph("<b>WHAT TO SAY (SPEAKS EXACTLY ONCE):</b>", speech_label_style))
        card_content.append(Paragraph(m['speech'], speech_body_style))
        card_content.append(Spacer(1, 2))
        card_content.append(Paragraph("<b>TEACHER RAPID-FIRE DEFENSE Q&A (30-SECOND ANSWER):</b>", qa_title_style))
        card_content.append(Paragraph(m['qa'], qa_body_style))
        card_content.append(Spacer(1, 8))
        card_content.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E0E0E0'), spaceAfter=8))

        story.append(KeepTogether(card_content))

    doc.build(story)
    print(f"[+] PDF generated successfully at: {pdf_path}")

def build_docx(docx_path):
    if not HAS_DOCX:
        print("[-] python-docx not available, skipping DOCX generation.")
        return

    doc = Document()

    for section in doc.sections:
        section.top_margin = DocxInches(0.5)
        section.bottom_margin = DocxInches(0.5)
        section.left_margin = DocxInches(0.5)
        section.right_margin = DocxInches(0.5)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("CRIMSON ORBIT – MUSICAL BAND & REAL SOUND STUDIO")
    run_title.font.name = 'Arial'
    run_title.font.size = DocxPt(19)
    run_title.font.bold = True
    run_title.font.color.rgb = DocxRGBColor(198, 40, 40)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Complete Team Presentation Script & Simple Teacher Defense Guide")
    run_sub.font.name = 'Arial'
    run_sub.font.size = DocxPt(11)
    run_sub.font.bold = True
    run_sub.font.color.rgb = DocxRGBColor(230, 81, 0)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_meta = p_meta.add_run("Primary Platform: emu8086 (8086 Emulator) | Sound Studio: HTML, CSS, JavaScript | Rule: Each Member Speaks Exactly Once")
    run_meta.font.name = 'Arial'
    run_meta.font.size = DocxPt(9)
    run_meta.font.color.rgb = DocxRGBColor(69, 90, 100)

    doc.add_paragraph().paragraph_format.space_after = DocxPt(6)

    members_data = [
        ("SPEAKER 1: AKASH", "PROJECT LEADER — IDEA, RESEARCH, WORKFLOW & CONCERT PIANO",
         "Good morning/afternoon, Respected Professor and classmates. Our course project is Crimson Orbit – Musical Band, developed and tested using the emu8086 emulator.\n\n"
         "How We Started & Our Research Workflow:\n"
         "When starting our microprocessor project, I wanted our team to build an interactive, fun musical application instead of a basic calculator. "
         "I researched how 8086 computers produce sound and discovered that emu8086 can control the computer's PC speaker directly by sending output signals to the sound ports. "
         "By dividing the clock frequency by musical notes, we can make the PC speaker play exact musical tones.\n\n"
         "However, while testing in emu8086, we noticed an obvious problem: the PC speaker can only make electronic beeps and buzzes. It cannot play real instrument sounds like a genuine acoustic piano or guitar. "
         "So our team decided on a clear workflow: we will create two connected parts for our project. "
         "First, we wrote the full assembly language code in emu8086 to prove low-level hardware control. "
         "Second, we built a modern Web Studio using HTML, CSS, and JavaScript, where we added 28 real studio recordings of real instruments so our band sounds completely real.\n\n"
         "In emu8086, I built the Concert Piano module (piano.asm), drawing 3D white and black keys that press down when you type Q through I on your keyboard, with an octave switcher and a sustain pedal. "
         "In our HTML and JavaScript studio, I integrated real recordings of a Steinway Grand Piano, so when you click the keys, it plays authentic concert piano music.\n\n"
         "I will now pass the presentation to Sanskar to explain the Guitar module.",
         "Teacher: \"Akash, what was your role and how did you decide on this project?\"\n"
         "Your Answer: \"Sir/Ma'am, I led the project research and workflow. I researched how emu8086 controls the PC speaker to play music. Because the PC speaker only gives basic beeps, I decided we should build the assembly code in emu8086 and also create a realistic Web Studio in HTML, CSS, and JavaScript with real recorded instruments. I programmed the Piano in assembly, added real Steinway piano sounds to the web studio, and assembled the whole team's work together.\""),

        ("SPEAKER 2: SANSKAR", "ACOUSTIC GUITAR MODULE (EMU8086 ASSEMBLY & WEB STUDIO FRETBOARD)",
         "Thank you, Akash. I designed and coded the Acoustic Guitar module (guitar.asm) in emu8086, and helped create the guitar interface in HTML, CSS, and JavaScript.\n\n"
         "In emu8086 assembly, I wanted the guitar to feel like a real instrument rather than flat beeps. I programmed all 6 guitar strings from Low E to High E. "
         "To make it sound like an acoustic string, I added a pick strike chirp effect when you pluck any string using keys Q through Y, followed by a gentle finger vibrato effect where the sound wobbles naturally. "
         "I also programmed the [S] key to strum a full acoustic chord across all strings.\n\n"
         "In our HTML, CSS, and JavaScript studio, I brought this guitar to life visually. "
         "We searched online and downloaded real acoustic guitar recordings of a Martin D-28 guitar: all 6 open strings plus strummed acoustic chords for E minor, G major, C major, and D major. "
         "When you click or press strings in the web studio, the strings physically vibrate on screen using CSS animations, and it plays authentic acoustic guitar sounds.\n\n"
         "I will now hand over to Krishna to present the Drums module.",
         "Teacher: \"Sanskar, what did you do for the guitar?\"\n"
         "Your Answer: \"Sir/Ma'am, in emu8086 assembly, I coded the 6 guitar strings, added pick strike sound effects, singing vibrato, and full chord strumming on key [S]. In HTML, CSS, and JavaScript, I built the guitar fretboard with vibrating strings and connected it to real Martin acoustic guitar recordings so it sounds authentic.\""),

        ("SPEAKER 3: KRISHNA", "DRUMS MODULE (EMU8086 NOISE GENERATOR & WEB STUDIO 3D DRUMS)",
         "Thank you, Sanskar. I developed the Drum Kit module (drums.asm) in emu8086, and built the 3D drum kit stage in HTML, CSS, and JavaScript.\n\n"
         "The biggest challenge in emu8086 was that the PC speaker only plays musical tones—it cannot naturally make drum noise like snares or cymbals. "
         "To solve this in assembly, I created a random white noise generator in 8086 code. "
         "Using this noise generator, I created 5 distinct drum sounds in emu8086: a deep Kick Drum that drops rapidly in pitch for an acoustic thump, a Snare Drum that blends white noise with a wooden shell sound, crisp Hi-Hats, and a shimmering Crash Cymbal.\n\n"
         "In our HTML, CSS, and JavaScript studio, I connected these drums to real close-miked studio recordings of a Ludwig Drum Kit. "
         "I designed the circular 3D drum pads so when you hit keys Q, W, E, R, or T, the drum pads light up with expanding shockwaves and play punchy, realistic studio drum beats.\n\n"
         "I will now pass to Hari to explain our Pre-Installed Songs.",
         "Teacher: \"Krishna, how did you make drum sounds on a PC speaker?\"\n"
         "Your Answer: \"Sir/Ma'am, because a PC speaker can only make musical tones, I wrote a random noise generator in 8086 assembly to create white noise for the snare and cymbals, and used quick frequency drops for the kick drum thump. In the HTML/CSS/JS studio, I connected these pads to real Ludwig drum kit recordings with moving shockwave animations.\""),

        ("SPEAKER 4: HARI", "SONGS REPERTOIRE (EMU8086 TIMING & WEB AUDIO NOTE TABLES)",
         "Thank you, Krishna. Ghansham and I worked together on the Pre-Installed Songs module (songs.asm) in emu8086, and connected our music into the JavaScript Web Studio.\n\n"
         "In emu8086 assembly, I stored the musical notes and timing for 6 famous songs: "
         "Happy Birthday, Twinkle Twinkle Little Star, Ode to Joy, Jingle Bells, Mary Had a Little Lamb, and London Bridge. "
         "Each note is stored as two numbers: the note frequency and how long it should play. "
         "I used timer delay loops so every song plays at a steady, natural musical tempo.\n\n"
         "In our HTML and JavaScript studio, I mapped these exact same song notes into our JavaScript audio player. "
         "This allows our web studio to play all 6 songs using the real Steinway piano, Martin guitar, or Ludwig drum beat across multiple octaves with 100% accurate pitch.\n\n"
         "I will now pass to Ghansham to explain the Jukebox player and visualizer.",
         "Teacher: \"Hari, what was your role in the songs module?\"\n"
         "Your Answer: \"Sir/Ma'am, in emu8086 assembly, I encoded the musical notes and delay timings for 6 classic songs, calibrating the timer loops so songs play at steady tempo. In JavaScript, I mapped these same notes so they trigger real piano, guitar, or drum sounds in the web studio.\""),

        ("SPEAKER 5: GHANSHAM", "JUKEBOX PLAYER & VISUALIZER (EMU8086 & HTML5 SPECTRUM EQUALIZER)",
         "Thank you, Hari. Building on Hari's song notes, I created the Jukebox Song Player and Moving Visualizers in both emu8086 and HTML/CSS/JavaScript.\n\n"
         "In emu8086 assembly (songs.asm), I wrote the automatic player that reads through the song notes, sends sound to the PC speaker, and animates 8 colorful equalizer bars bouncing up and down on screen. "
         "I also made sure that pressing the [ESC] key stops the song immediately and returns cleanly to the main menu without freezing the emulator.\n\n"
         "In our HTML and JavaScript studio, I upgraded this into a Real-Time 60 FPS Moving Spectrum Equalizer. "
         "As songs play, colorful visualizer bars jump up and down to the music and display live frequency numbers. "
         "Users can also click buttons to hear any song played on Real Grand Piano, Real Acoustic Guitar, or a Rock Drum Beat.\n\n"
         "I will now pass back to Akash to present our system assembling and live demonstration.",
         "Teacher: \"Ghansham, what did you build for the song player?\"\n"
         "Your Answer: \"Sir/Ma'am, in emu8086 assembly, I built the automatic jukebox player that plays through songs, animated 8 text visualizer bars on screen, and added [ESC] key support to stop playback anytime. In HTML and JavaScript, I built the colorful moving spectrum equalizer that dances in real time to the music.\""),

        ("SPEAKER 6: AKASH (CLOSING & DEMO)", "PROJECT ASSEMBLING & LIVE DEMONSTRATION",
         "Thank you, Ghansham. To conclude our presentation, I will explain how we assembled the complete project and how to run it.\n\n"
         "How We Assembled Everything:\n"
         "In emu8086, I linked all our team files together inside kernel.asm using include statements: bringing together piano.asm, guitar.asm, drums.asm, and songs.asm into one cohesive program. "
         "You can run it directly in emu8086 by opening kernel.asm, clicking Emulate, and clicking Run.\n\n"
         "To make our Web Studio equally easy to run, I compiled the HTML, CSS, JavaScript, and all 28 real instrument recordings into a single standalone file: CrimsonOrbit_RealStudio.html. "
         "It sits right in our Downloads and Desktop folder. You just double-click it, and it immediately opens in Chrome or Edge, playing real Steinway piano, Martin guitar, and Ludwig drums completely offline.\n\n"
         "We will now demonstrate both: first our assembly code running in emu8086, and then our Real Sound Studio. "
         "Thank you, Professor, and we are ready for your questions!",
         "Teacher: \"Why does your project have both emu8086 assembly and an HTML/CSS/JS file?\"\n"
         "Your Answer: \"Professor, our core project is 100% written in 8086 assembly language running in emu8086. But because the PC speaker in emu8086 only makes electronic beeps, we also built the HTML, CSS, and JavaScript studio to show how our exact assembly music sounds with real studio-recorded instruments like Steinway piano and Martin guitar. This proves we mastered both low-level assembly and modern audio presentation!\"")
    ]

    for name, role, speech, qa in members_data:
        p_name = doc.add_paragraph()
        run_name = p_name.add_run(name)
        run_name.font.name = 'Arial'
        run_name.font.size = DocxPt(12)
        run_name.font.bold = True
        run_name.font.color.rgb = DocxRGBColor(198, 40, 40)

        p_role = doc.add_paragraph()
        run_role = p_role.add_run(f"ASSIGNED ROLE: {role}")
        run_role.font.name = 'Arial'
        run_role.font.size = DocxPt(9.5)
        run_role.font.bold = True
        run_role.font.color.rgb = DocxRGBColor(230, 81, 0)

        p_spk_lbl = doc.add_paragraph()
        run_spk_lbl = p_spk_lbl.add_run("WHAT TO SAY (SPEAKS EXACTLY ONCE):")
        run_spk_lbl.font.name = 'Arial'
        run_spk_lbl.font.size = DocxPt(10)
        run_spk_lbl.font.bold = True
        run_spk_lbl.font.color.rgb = DocxRGBColor(13, 71, 161)

        p_speech = doc.add_paragraph()
        run_speech = p_speech.add_run(speech)
        run_speech.font.name = 'Arial'
        run_speech.font.size = DocxPt(9.5)

        p_qa_lbl = doc.add_paragraph()
        run_qa_lbl = p_qa_lbl.add_run("TEACHER RAPID-FIRE DEFENSE Q&A (30-SECOND ANSWER):")
        run_qa_lbl.font.name = 'Arial'
        run_qa_lbl.font.size = DocxPt(9.5)
        run_qa_lbl.font.bold = True
        run_qa_lbl.font.color.rgb = DocxRGBColor(183, 28, 28)

        p_qa = doc.add_paragraph()
        run_qa = p_qa.add_run(qa)
        run_qa.font.name = 'Arial'
        run_qa.font.size = DocxPt(9)
        run_qa.font.italic = True

        doc.add_paragraph().paragraph_format.space_after = DocxPt(10)

    doc.save(docx_path)
    print(f"[+] DOCX generated successfully at: {docx_path}")

def main():
    root = r"C:\FOIDS_CP"
    desktop = r"C:\Users\akash\Desktop"
    downloads = r"C:\Users\akash\Downloads"
    docs_dir = os.path.join(root, "Assets", "Documentation")

    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(downloads, exist_ok=True)

    pdf_project = os.path.join(docs_dir, "CrimsonOrbit_Presentation_Script.pdf")
    docx_project = os.path.join(docs_dir, "CrimsonOrbit_Presentation_Script.docx")

    print("[*] Generating Simplified Presentation Script PDF & DOCX...")
    build_pdf(pdf_project)
    build_docx(docx_project)

    # Copy to Desktop
    for src, fname in [(pdf_project, "CrimsonOrbit_Presentation_Script.pdf"), (docx_project, "CrimsonOrbit_Presentation_Script.docx")]:
        dst = os.path.join(desktop, fname)
        try:
            shutil.copy2(src, dst)
            print(f"[+] Copied to Desktop: {dst}")
        except Exception as e:
            print(f"[-] Desktop copy error ({fname}): {e}")

    # Copy to Downloads
    for src, fname in [(pdf_project, "CrimsonOrbit_Presentation_Script.pdf"), (docx_project, "CrimsonOrbit_Presentation_Script.docx")]:
        dst = os.path.join(downloads, fname)
        try:
            shutil.copy2(src, dst)
            print(f"[+] Copied to Downloads: {dst}")
        except Exception as e:
            print(f"[-] Downloads copy error ({fname}): {e}")

    print("[*] Script generation complete!")

if __name__ == "__main__":
    main()
