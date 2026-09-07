; ==============================================================================
; CRIMSON ORBIT – MUSICAL BAND
; Module: Simulated Acoustic & Lead Guitar (guitar.asm)
; Target Assembler: emu8086
; Professional 6-string acoustic/lead guitar with wound-bronze & steel string visuals,
; elevated concert frequencies, plectrum attack transient physical modeling,
; expressive finger vibrato, multi-string chord strumming, and live HUD.
; ==============================================================================

; Fretboard Column Limits
FRET_COL_START      equ 14
FRET_COL_END        equ 68

; ------------------------------------------------------------------------------
; Guitar State Variables
; ------------------------------------------------------------------------------
guitar_octave_mode  dw 0        ; 0 = Concert Acoustic (165..659 Hz), 1 = Lead Solo (330..1318 Hz)
guitar_chord_idx    dw 0        ; Current strum chord index (0=Em, 1=G, 2=C, 3=D)

; Tuning Frequencies (Concert Acoustic Mode - Bright, Singing Hz)
; String 1 (High E5) -> String 6 (Low E3)
guitar_freqs_acoustic:
    dw 659, 494, 392, 294, 220, 165

; Tuning Frequencies (Lead Solo Mode - High-Hertz Electric Brilliance)
; String 1 (High E6) -> String 6 (Low E4)
guitar_freqs_lead:
    dw 1318, 988, 784, 587, 440, 330

; Chords for Strumming (Arrays of frequencies ending with 0)
chord_em:   dw 165, 247, 330, 392, 494, 659, 0
chord_g:    dw 196, 247, 294, 392, 494, 784, 0
chord_c:    dw 262, 330, 392, 523, 659, 0
chord_d:    dw 294, 370, 440, 587, 740, 0

chord_ptrs:
    dw chord_em, chord_g, chord_c, chord_d
chord_names:
    dw str_chord_em, str_chord_g, str_chord_c, str_chord_d

; ------------------------------------------------------------------------------
; Guitar_Run
; Main Interactive Guitar Entry Point
; ------------------------------------------------------------------------------
Guitar_Run proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; 1. Clear Screen
    mov bl, 07h
    call Utils_ClearScreen
    call Utils_HideCursor

    ; 2. Render Header
    mov si, str_guitar_hdr
    call Graphics_DrawHeader

    mov dh, 4
    mov dl, 19
    mov bl, THEME_ACCENT
    mov si, str_guitar_sub
    call Utils_PrintStringAt

    ; 3. Draw Fretboard, Nut, Frets and Strings
    call Guitar_DrawFretboard

    ; 4. Draw HUD
    call Guitar_ClearHUD

    ; 5. Draw Footer
    mov si, str_guitar_foot
    call Graphics_DrawFooter

guitar_event_loop:
    call Keyboard_WaitKey

    cmp al, KEY_ESC
    je guitar_exit

    ; Check for [TAB] to toggle Acoustic / Lead Solo mode
    cmp al, KEY_TAB
    jne g_chk_strum
    call Guitar_ToggleMode
    jmp guitar_event_loop

g_chk_strum:
    ; Convert letter to uppercase
    call Keyboard_ToUpper

    ; Check for 'S' to Strum Chord
    cmp al, 'S'
    jne g_chk_strings
    call Guitar_StrumNextChord
    jmp guitar_event_loop

g_chk_strings:
    cmp al, 'Q'
    jne g_chk_w
    mov bx, 0                   ; String 1 (High E)
    mov dh, 7                   ; Row 7
    mov si, str_g_str1
    call Guitar_PluckStringIdx
    jmp guitar_event_loop

g_chk_w:
    cmp al, 'W'
    jne g_chk_e
    mov bx, 1                   ; String 2 (B)
    mov dh, 9                   ; Row 9
    mov si, str_g_str2
    call Guitar_PluckStringIdx
    jmp guitar_event_loop

g_chk_e:
    cmp al, 'E'
    jne g_chk_r
    mov bx, 2                   ; String 3 (G)
    mov dh, 11                  ; Row 11
    mov si, str_g_str3
    call Guitar_PluckStringIdx
    jmp guitar_event_loop

g_chk_r:
    cmp al, 'R'
    jne g_chk_t
    mov bx, 3                   ; String 4 (D)
    mov dh, 13                  ; Row 13
    mov si, str_g_str4
    call Guitar_PluckStringIdx
    jmp guitar_event_loop

g_chk_t:
    cmp al, 'T'
    jne g_chk_y
    mov bx, 4                   ; String 5 (A)
    mov dh, 15                  ; Row 15
    mov si, str_g_str5
    call Guitar_PluckStringIdx
    jmp guitar_event_loop

g_chk_y:
    cmp al, 'Y'
    jne guitar_event_loop
    mov bx, 5                   ; String 6 (Low E)
    mov dh, 17                  ; Row 17
    mov si, str_g_str6
    call Guitar_PluckStringIdx
    jmp guitar_event_loop

guitar_exit:
    call Speaker_ToneOff
    call Utils_ShowCursor
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Guitar_Run endp

; ------------------------------------------------------------------------------
; Guitar_GetFreq
; Returns frequency in AX for string index in BX (0..5) based on guitar_octave_mode.
; ------------------------------------------------------------------------------
Guitar_GetFreq proc
    push bx
    shl bx, 1
    cmp word [guitar_octave_mode], 0
    jne ggf_lead
    mov ax, [guitar_freqs_acoustic + bx]
    pop bx
    ret
ggf_lead:
    mov ax, [guitar_freqs_lead + bx]
    pop bx
    ret
Guitar_GetFreq endp

; ------------------------------------------------------------------------------
; Guitar_ToggleMode
; Switches between Concert Acoustic and Lead Solo mode.
; ------------------------------------------------------------------------------
Guitar_ToggleMode proc
    push ax
    push bx
    push cx
    push dx
    push si

    xor word [guitar_octave_mode], 1

    ; Play mode switch chime
    mov ax, 1046
    mov cx, 35
    call Speaker_GuitarPluckPro

    call Guitar_ClearHUD
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Guitar_ToggleMode endp

; ------------------------------------------------------------------------------
; Guitar_DrawFretboard
; Renders the 6 strings, frets, nut, and tuning pegs.
; ------------------------------------------------------------------------------
Guitar_DrawFretboard proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; Fretboard Outer Border Box (Rows 6..18, Cols 12..70)
    mov dh, 6
    mov dl, 12
    mov ch, 18
    mov cl, 70
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    ; Vertical Fret Wires at Cols 24, 35, 46, 57, 68
    mov bl, THEME_MUTED
    mov al, CP437_S_V

    mov dl, 24
    mov dh, 7
    mov cx, 11
    call Graphics_DrawVLine

    mov dl, 35
    mov dh, 7
    mov cx, 11
    call Graphics_DrawVLine

    mov dl, 46
    mov dh, 7
    mov cx, 11
    call Graphics_DrawVLine

    mov dl, 57
    mov dh, 7
    mov cx, 11
    call Graphics_DrawVLine

    ; Fret Inlay Markers (Row 12, cols 30, 41, 52, and 63 double dot)
    mov dh, 12
    mov dl, 30
    mov al, 'o'
    mov bl, THEME_ACCENT
    call Graphics_DrawChar

    mov dl, 41
    call Graphics_DrawChar

    mov dl, 52
    call Graphics_DrawChar

    ; Fret 12 Octave Double Dot (::)
    mov dl, 63
    mov al, ':'
    call Graphics_DrawChar

    ; Draw all 6 resting strings with wound bronze and steel distinctions
    mov dh, 7
    call Guitar_DrawRestingString

    mov dh, 9
    call Guitar_DrawRestingString

    mov dh, 11
    call Guitar_DrawRestingString

    mov dh, 13
    call Guitar_DrawRestingString

    mov dh, 15
    call Guitar_DrawRestingString

    mov dh, 17
    call Guitar_DrawRestingString

    ; Left-side string labels & keys (Cols 2..10)
    mov bl, THEME_TEXT
    mov dh, 7
    mov dl, 3
    mov si, str_lbl_str1
    call Utils_PrintStringAt

    mov dh, 9
    mov dl, 3
    mov si, str_lbl_str2
    call Utils_PrintStringAt

    mov dh, 11
    mov dl, 3
    mov si, str_lbl_str3
    call Utils_PrintStringAt

    mov dh, 13
    mov dl, 3
    mov si, str_lbl_str4
    call Utils_PrintStringAt

    mov dh, 15
    mov dl, 3
    mov si, str_lbl_str5
    call Utils_PrintStringAt

    mov dh, 17
    mov dl, 3
    mov si, str_lbl_str6
    call Utils_PrintStringAt

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Guitar_DrawFretboard endp

; ------------------------------------------------------------------------------
; Guitar_DrawRestingString
; Draws a resting string line at row DH from FRET_COL_START to FRET_COL_END.
; Heavy wound strings at rows 15 and 17 use double-line CP437_D_H (═) in bronze.
; Treble strings at rows 7, 9, 11, 13 use single-line CP437_S_H (─) in silver.
; Input: DH = row
; ------------------------------------------------------------------------------
Guitar_DrawRestingString proc
    push ax
    push bx
    push cx
    push dx

    mov dl, FRET_COL_START
    mov cx, (FRET_COL_END - FRET_COL_START + 1)

    cmp dh, 15
    jae g_drs_wound             ; Rows 15 and 17: Wound bronze bass strings
    mov al, CP437_S_H           ; ─
    mov bl, 07h                 ; Silver/gray steel
    jmp g_drs_draw
g_drs_wound:
    mov al, CP437_D_H           ; ═
    mov bl, 06h                 ; Brown/Bronze wound
g_drs_draw:
    call Graphics_DrawHLine

    pop dx
    pop cx
    pop bx
    pop ax
    ret
Guitar_DrawRestingString endp

; ------------------------------------------------------------------------------
; Guitar_PluckStringIdx
; Plucks string by index BX (0..5), vibrates visually, plays singing tone, restores.
; Input:  BX = String index (0..5)
;         DH = string row
;         SI -> string description
; ------------------------------------------------------------------------------
Guitar_PluckStringIdx proc
    push ax
    push bx
    push cx
    push dx
    push si

    call Guitar_GetFreq          ; AX = calculated Hz for this string
    push ax

    ; 1. Update HUD with String Info & Hz
    push dx
    push si
    mov dh, 20
    mov dl, 16
    mov bl, THEME_TITLE
    call Utils_PrintStringAt

    ; Display Hz readout
    mov dh, 20
    mov dl, 46
    mov bl, THEME_TEXT
    mov si, str_hud_freq_lbl
    call Utils_PrintStringAt

    pop si
    pop dx
    pop ax
    push ax
    push dx
    mov dl, 52
    call Piano_PrintWordNum

    mov dh, 20
    mov dl, 57
    mov bl, THEME_ACCENT
    mov si, str_hud_hz
    call Utils_PrintStringAt
    pop dx

    ; 2. Animate vibrating string (radiating glowing wave ~≈~≈)
    push dx
    mov dl, FRET_COL_START
    mov cx, (FRET_COL_END - FRET_COL_START + 1)
    mov al, '~'
    mov bl, THEME_TITLE
    call Graphics_DrawHLine
    pop dx

    ; 3. Play realistic singing guitar tone with plectrum attack & vibrato
    pop ax
    push dx
    mov cx, 240                 ; 240ms duration
    call Speaker_GuitarPluckPro
    pop dx

    ; 4. Restore resting string
    call Guitar_DrawRestingString

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Guitar_PluckStringIdx endp

; ------------------------------------------------------------------------------
; Guitar_StrumNextChord
; Strums next chord in progression (Em -> G -> C -> D -> Em) with full animation.
; ------------------------------------------------------------------------------
Guitar_StrumNextChord proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; Get current chord pointer
    mov bx, [guitar_chord_idx]
    shl bx, 1
    mov si, [chord_ptrs + bx]
    mov di, [chord_names + bx]

    ; Update HUD
    mov dh, 20
    mov dl, 16
    mov bl, THEME_TITLE
    mov si, di
    call Utils_PrintStringAt

    ; Animate full fretboard wave vibration across all 6 strings
    mov dh, 7
    mov cx, 6
g_strum_anim:
    push dx
    push cx
    mov dl, FRET_COL_START
    mov cx, (FRET_COL_END - FRET_COL_START + 1)
    mov al, '~'
    mov bl, THEME_ACCENT
    call Graphics_DrawHLine
    pop cx
    pop dx
    add dh, 2
    loop g_strum_anim

    ; Play acoustic strum arpeggio
    mov bx, [guitar_chord_idx]
    shl bx, 1
    mov si, [chord_ptrs + bx]
    mov cx, 280
    call Speaker_StrumChord

    ; Restore all 6 strings
    mov dh, 7
    call Guitar_DrawRestingString
    mov dh, 9
    call Guitar_DrawRestingString
    mov dh, 11
    call Guitar_DrawRestingString
    mov dh, 13
    call Guitar_DrawRestingString
    mov dh, 15
    call Guitar_DrawRestingString
    mov dh, 17
    call Guitar_DrawRestingString

    ; Advance to next chord
    mov ax, [guitar_chord_idx]
    inc ax
    cmp ax, 4
    jb g_snc_save
    xor ax, ax
g_snc_save:
    mov [guitar_chord_idx], ax

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Guitar_StrumNextChord endp

; ------------------------------------------------------------------------------
; Guitar_ClearHUD
; Renders the idle status and mode panel.
; ------------------------------------------------------------------------------
Guitar_ClearHUD proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; Single box at Rows 19..21, Cols 14..68
    mov dh, 19
    mov dl, 14
    mov ch, 21
    mov cl, 68
    mov bl, THEME_MUTED
    call Graphics_DrawBoxSingle

    mov dh, 20
    mov dl, 16
    mov bl, THEME_MUTED
    mov si, str_g_hud_idle
    call Utils_PrintStringAt

    ; Print Mode Tag
    mov dh, 20
    mov dl, 52
    cmp word [guitar_octave_mode], 0
    jne g_chud_lead
    mov bl, 0Ah                 ; Light Green
    mov si, str_mode_acous
    call Utils_PrintStringAt
    jmp g_chud_done
g_chud_lead:
    mov bl, THEME_TITLE         ; Crimson
    mov si, str_mode_lead
    call Utils_PrintStringAt

g_chud_done:
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Guitar_ClearHUD endp

; ------------------------------------------------------------------------------
; Guitar Strings & Visual Data
; ------------------------------------------------------------------------------
str_guitar_hdr      db "ACOUSTIC & LEAD GUITAR", 0
str_guitar_sub      db "[ Plectrum Attack Physical Modeling & Singing Vibrato ]", 0
str_guitar_foot     db "[ESC] Menu | [TAB] Mode | [S] Strum Chord | [Q..Y] Pluck Strings", 0

str_lbl_str1        db "[Q] 1-E5", 0
str_lbl_str2        db "[W] 2-B4", 0
str_lbl_str3        db "[E] 3-G4", 0
str_lbl_str4        db "[R] 4-D4", 0
str_lbl_str5        db "[T] 5-A3", 0
str_lbl_str6        db "[Y] 6-E3", 0

str_g_hud_idle      db "Guitar Ready - Pluck [Q..Y] or Strum [S]... ", 0
str_mode_acous      db "[ACOUSTIC]", 0
str_mode_lead       db "[LEAD SOLO]", 0

str_g_str1          db "String 1: High E (Concert Singing)  ", 0
str_g_str2          db "String 2: B      (Acoustic Steel)   ", 0
str_g_str3          db "String 3: G      (Acoustic Steel)   ", 0
str_g_str4          db "String 4: D      (Wound Bronze)     ", 0
str_g_str5          db "String 5: A      (Wound Bronze)     ", 0
str_g_str6          db "String 6: Low E  (Deep Wound Bronze)", 0

str_chord_em        db "Acoustic Strum: E Minor Chord (Em)    ", 0
str_chord_g         db "Acoustic Strum: G Major Chord (G)     ", 0
str_chord_c         db "Acoustic Strum: C Major Chord (C)     ", 0
str_chord_d         db "Acoustic Strum: D Major Chord (D)     ", 0
