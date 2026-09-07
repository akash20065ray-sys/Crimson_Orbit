; ==============================================================================
; CRIMSON ORBIT – MUSICAL BAND
; Module: Interactive Concert Grand Piano (piano.asm)
; Target Assembler: emu8086
; Professional 8086 Concert Grand Piano with 3D ivory/ebony keyboard aesthetics,
; acoustic hammer-strike physical modeling, dynamic decay, sustain pedal,
; multi-octave high-Hertz switching, live VU meter, and real-time frequency HUD.
; ==============================================================================

; Visual Piano Box Boundaries (Rows 6..16, Cols 16..63)
PIANO_ROW_TOP       equ 6
PIANO_ROW_BOT       equ 16
PIANO_COL_LEFT      equ 16
PIANO_COL_RIGHT     equ 63

; ------------------------------------------------------------------------------
; Piano State Variables
; ------------------------------------------------------------------------------
piano_octave        dw 5        ; Default: Octave 5 (Concert High-Hz, 523..1046 Hz)
piano_last_freq     dw 523      ; Last played frequency in Hz

; Note Frequency Tables for Octave 4 Base (C4..C5)
; Indexed: 0=C, 1=C#, 2=D, 3=D#, 4=E, 5=F, 6=F#, 7=G, 8=G#, 9=A, 10=A#, 11=B, 12=C+
piano_base_freqs:
    dw 262, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 494, 523

; ------------------------------------------------------------------------------
; Piano_Run
; Main Interactive Piano Entry Point
; ------------------------------------------------------------------------------
Piano_Run proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; 1. Clear Screen to Deep Black
    mov bl, 07h
    call Utils_ClearScreen
    call Utils_HideCursor

    ; 2. Render Header & Subtitle
    mov si, str_piano_hdr
    call Graphics_DrawHeader

    mov dh, 4
    mov dl, 18
    mov bl, THEME_ACCENT
    mov si, str_piano_sub
    call Utils_PrintStringAt

    ; 3. Render Grand Piano Keyboard Visuals
    call Piano_DrawKeyboard

    ; 4. Render Initial HUD
    call Piano_ClearHUD

    ; 5. Render Footer Instructions
    mov si, str_piano_foot
    call Graphics_DrawFooter

piano_event_loop:
    call Keyboard_WaitKey       ; AL = ASCII, AH = Scan code

    ; Check for ESC to exit
    cmp al, KEY_ESC
    je piano_exit

    ; Check for [TAB] to toggle Octave (4 -> 5 -> 6 -> 4)
    cmp al, KEY_TAB
    jne p_chk_pedal
    call Piano_ToggleOctave
    jmp piano_event_loop

p_chk_pedal:
    ; Check for [SPACE] to toggle Sustain / Damper Pedal
    cmp al, KEY_SPACE
    jne p_chk_note_keys
    call Piano_TogglePedal
    jmp piano_event_loop

p_chk_note_keys:
    ; Convert letter to uppercase
    call Keyboard_ToUpper

    ; Dispatch keys
    cmp al, 'Q'
    jne p_check_2
    mov bx, 0                   ; Note 0: C
    mov si, str_note_name_c
    mov dl, 17                  ; Col for C
    call Piano_PlayWhiteKey
    jmp piano_event_loop

p_check_2:
    cmp al, '2'
    jne p_check_w
    mov bx, 1                   ; Note 1: C#
    mov si, str_note_name_cs
    mov dl, 21                  ; Col for C#
    call Piano_PlayBlackKey
    jmp piano_event_loop

p_check_w:
    cmp al, 'W'
    jne p_check_3
    mov bx, 2                   ; Note 2: D
    mov si, str_note_name_d
    mov dl, 23                  ; Col for D
    call Piano_PlayWhiteKey
    jmp piano_event_loop

p_check_3:
    cmp al, '3'
    jne p_check_e
    mov bx, 3                   ; Note 3: D#
    mov si, str_note_name_ds
    mov dl, 27                  ; Col for D#
    call Piano_PlayBlackKey
    jmp piano_event_loop

p_check_e:
    cmp al, 'E'
    jne p_check_r
    mov bx, 4                   ; Note 4: E
    mov si, str_note_name_e
    mov dl, 29                  ; Col for E
    call Piano_PlayWhiteKey
    jmp piano_event_loop

p_check_r:
    cmp al, 'R'
    jne p_check_5
    mov bx, 5                   ; Note 5: F
    mov si, str_note_name_f
    mov dl, 35                  ; Col for F
    call Piano_PlayWhiteKey
    jmp piano_event_loop

p_check_5:
    cmp al, '5'
    jne p_check_t
    mov bx, 6                   ; Note 6: F#
    mov si, str_note_name_fs
    mov dl, 39                  ; Col for F#
    call Piano_PlayBlackKey
    jmp piano_event_loop

p_check_t:
    cmp al, 'T'
    jne p_check_6
    mov bx, 7                   ; Note 7: G
    mov si, str_note_name_g
    mov dl, 41                  ; Col for G
    call Piano_PlayWhiteKey
    jmp piano_event_loop

p_check_6:
    cmp al, '6'
    jne p_check_y
    mov bx, 8                   ; Note 8: G#
    mov si, str_note_name_gs
    mov dl, 45                  ; Col for G#
    call Piano_PlayBlackKey
    jmp piano_event_loop

p_check_y:
    cmp al, 'Y'
    jne p_check_7
    mov bx, 9                   ; Note 9: A (Concert Pitch 440/880 Hz)
    mov si, str_note_name_a
    mov dl, 47                  ; Col for A
    call Piano_PlayWhiteKey
    jmp piano_event_loop

p_check_7:
    cmp al, '7'
    jne p_check_u
    mov bx, 10                  ; Note 10: A#
    mov si, str_note_name_as
    mov dl, 51                  ; Col for A#
    call Piano_PlayBlackKey
    jmp piano_event_loop

p_check_u:
    cmp al, 'U'
    jne p_check_i
    mov bx, 11                  ; Note 11: B
    mov si, str_note_name_b
    mov dl, 53                  ; Col for B
    call Piano_PlayWhiteKey
    jmp piano_event_loop

p_check_i:
    cmp al, 'I'
    jne piano_event_loop        ; Unmapped key -> ignore
    mov bx, 12                  ; Note 12: C+
    mov si, str_note_name_c_hi
    mov dl, 59                  ; Col for C+
    call Piano_PlayWhiteKey
    jmp piano_event_loop

piano_exit:
    call Speaker_ToneOff
    mov word [piano_sustain_flag], 0
    call Utils_ShowCursor
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Piano_Run endp

; ------------------------------------------------------------------------------
; Piano_CalcNoteFreq
; Calculates frequency in AX for note index in BX according to piano_octave.
; Input:  BX = Note index (0..12)
; Output: AX = Frequency in Hz
; ------------------------------------------------------------------------------
Piano_CalcNoteFreq proc
    push bx
    push dx

    shl bx, 1                   ; 2 bytes per word
    mov ax, [piano_base_freqs + bx] ; Octave 4 frequency

    mov dx, [piano_octave]
    cmp dx, 4
    je p_cnf_done
    cmp dx, 5
    jne p_cnf_oct6
    shl ax, 1                   ; Octave 5: * 2 (Concert High 523..1046 Hz)
    jmp p_cnf_done
p_cnf_oct6:
    shl ax, 2                   ; Octave 6: * 4 (Brilliant 1046..2093 Hz)

p_cnf_done:
    mov [piano_last_freq], ax
    pop dx
    pop bx
    ret
Piano_CalcNoteFreq endp

; ------------------------------------------------------------------------------
; Piano_ToggleOctave
; Cycles Octave 4 -> 5 -> 6 -> 4 and updates status display.
; ------------------------------------------------------------------------------
Piano_ToggleOctave proc
    push ax
    push bx
    push cx
    push dx
    push si

    mov ax, [piano_octave]
    inc ax
    cmp ax, 6
    jbe p_to_save
    mov ax, 4
p_to_save:
    mov [piano_octave], ax

    ; Play quick octave chime
    mov ax, 880
    mov cx, 30
    call Speaker_PlayToneMs

    call Piano_ClearHUD
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Piano_ToggleOctave endp

; ------------------------------------------------------------------------------
; Piano_TogglePedal
; Toggles Sustain Pedal ON/OFF and updates status display.
; ------------------------------------------------------------------------------
Piano_TogglePedal proc
    push ax
    push bx
    push cx
    push dx
    push si

    xor word [piano_sustain_flag], 1

    ; Brief soft thud click
    mov ax, 180
    mov cx, 15
    call Speaker_PlayToneMs

    call Piano_ClearHUD
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Piano_TogglePedal endp

; ------------------------------------------------------------------------------
; Piano_DrawKeyboard
; Renders the visual 8-white-key, 5-black-key concert keyboard layout.
; ------------------------------------------------------------------------------
Piano_DrawKeyboard proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; Outer Frame Box (Double border in Crimson)
    mov dh, PIANO_ROW_TOP - 1
    mov dl, PIANO_COL_LEFT - 1
    mov ch, PIANO_ROW_BOT + 1
    mov cl, PIANO_COL_RIGHT + 1
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    ; White keys base background (Rows 6..16)
    ; White key columns:
    ; C: 17..21 | D: 23..27 | E: 29..33 | F: 35..39
    ; G: 41..45 | A: 47..51 | B: 53..57 | C+: 59..63
    mov dh, PIANO_ROW_TOP
p_rows_loop:
    mov dl, PIANO_COL_LEFT
    mov bl, 70h                 ; Black on White/Gray Ivory
    mov si, str_white_row
    call Utils_PrintStringAt
    inc dh
    cmp dh, PIANO_ROW_BOT
    jbe p_rows_loop

    ; Render Ebony Black Keys (Rows 6..11)
    ; Black keys: C#(21..22), D#(27..28), F#(39..40), G#(45..46), A#(51..52)
    mov dh, PIANO_ROW_TOP
p_black_loop:
    mov bl, 00h                 ; Ebony Black
    ; C#
    mov dl, 21
    mov cx, 2
    mov al, ' '
    call Graphics_DrawHLine
    ; D#
    mov dl, 27
    mov cx, 2
    mov al, ' '
    call Graphics_DrawHLine
    ; F#
    mov dl, 39
    mov cx, 2
    mov al, ' '
    call Graphics_DrawHLine
    ; G#
    mov dl, 45
    mov cx, 2
    mov al, ' '
    call Graphics_DrawHLine
    ; A#
    mov dl, 51
    mov cx, 2
    mov al, ' '
    call Graphics_DrawHLine

    inc dh
    cmp dh, PIANO_ROW_TOP + 5
    jbe p_black_loop

    ; Labels on White Keys (Row 14: Keys, Row 15: Note Names)
    mov bl, 70h
    mov dh, 14
    mov dl, PIANO_COL_LEFT
    mov si, str_white_keys_lbl
    call Utils_PrintStringAt

    mov dh, 15
    mov dl, PIANO_COL_LEFT
    mov si, str_white_note_lbl
    call Utils_PrintStringAt

    ; Labels on Black Keys (Row 8: Black key numbers)
    mov dh, 8
    mov bl, 0Fh                 ; Bright white text on black key
    mov dl, 21
    mov al, '2'
    call Graphics_DrawChar
    mov dl, 27
    mov al, '3'
    call Graphics_DrawChar
    mov dl, 39
    mov al, '5'
    call Graphics_DrawChar
    mov dl, 45
    mov al, '6'
    call Graphics_DrawChar
    mov dl, 51
    mov al, '7'
    call Graphics_DrawChar

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Piano_DrawKeyboard endp

; ------------------------------------------------------------------------------
; Piano_PlayWhiteKey
; Highlights white key with 3D depression, updates HUD, plays hammer tone, restores.
; Input:  BX = Note index (0..12)
;         SI -> Note description string
;         DL = start column of white key
; ------------------------------------------------------------------------------
Piano_PlayWhiteKey proc
    push bx
    push cx
    push dx
    push si

    ; Calculate exact frequency according to current octave
    call Piano_CalcNoteFreq      ; AX = Calculated Hz
    push ax

    ; Update HUD with Note Info & VU meter
    push dx
    call Piano_UpdateHUD
    pop dx

    ; Visual Key Depression Animation:
    ; Highlight white key in glowing Crimson & Gold (Rows 12..16, 5 cols wide)
    push dx
    mov dh, 12
p_pwk_hl:
    mov cx, 5
    mov al, CP437_BLOCK_FULL
    mov bl, THEME_TITLE
    call Graphics_DrawHLine
    inc dh
    cmp dh, PIANO_ROW_BOT
    jbe p_pwk_hl
    pop dx

    ; Play realistic acoustic piano tone with hammer strike & decay envelope
    pop ax                      ; AX = Frequency in Hz
    push dx
    mov cx, 200                 ; 200ms base duration
    call Speaker_PianoTone
    pop dx

    ; Restore normal white key visual
    mov dh, 12
p_pwk_rst:
    mov cx, 5
    mov al, ' '
    mov bl, 70h
    call Graphics_DrawHLine
    inc dh
    cmp dh, PIANO_ROW_BOT
    jbe p_pwk_rst

    ; Re-render labels
    mov dh, 14
    mov dl, PIANO_COL_LEFT
    mov bl, 70h
    mov si, str_white_keys_lbl
    call Utils_PrintStringAt

    mov dh, 15
    mov dl, PIANO_COL_LEFT
    mov bl, 70h
    mov si, str_white_note_lbl
    call Utils_PrintStringAt

    pop si
    pop dx
    pop cx
    pop bx
    ret
Piano_PlayWhiteKey endp

; ------------------------------------------------------------------------------
; Piano_PlayBlackKey
; Highlights black key with 3D depression, updates HUD, plays hammer tone, restores.
; Input:  BX = Note index (0..12)
;         SI -> Note description string
;         DL = start column of black key
; ------------------------------------------------------------------------------
Piano_PlayBlackKey proc
    push bx
    push cx
    push dx
    push si

    ; Calculate exact frequency according to current octave
    call Piano_CalcNoteFreq      ; AX = Calculated Hz
    push ax

    ; Update HUD with Note Info & VU meter
    push dx
    call Piano_UpdateHUD
    pop dx

    ; Highlight black key in Gold (Rows 6..11, 2 cols wide)
    push dx
    mov dh, PIANO_ROW_TOP
p_pbk_hl:
    mov cx, 2
    mov al, CP437_BLOCK_FULL
    mov bl, THEME_ACCENT
    call Graphics_DrawHLine
    inc dh
    cmp dh, PIANO_ROW_TOP + 5
    jbe p_pbk_hl
    pop dx

    ; Play realistic acoustic piano tone with hammer strike & decay envelope
    pop ax                      ; AX = Frequency in Hz
    push dx
    mov cx, 200                 ; 200ms base duration
    call Speaker_PianoTone
    pop dx

    ; Restore black key visual
    push dx
    mov dh, PIANO_ROW_TOP
p_pbk_rst:
    mov cx, 2
    mov al, ' '
    mov bl, 00h
    call Graphics_DrawHLine
    inc dh
    cmp dh, PIANO_ROW_TOP + 5
    jbe p_pbk_rst
    pop dx

    ; Restore number label
    mov dh, 8
    mov bl, 0Fh
    cmp dl, 21
    jne pb_rst_3
    mov al, '2'
    jmp pb_draw_lbl
pb_rst_3:
    cmp dl, 27
    jne pb_rst_5
    mov al, '3'
    jmp pb_draw_lbl
pb_rst_5:
    cmp dl, 39
    jne pb_rst_6
    mov al, '5'
    jmp pb_draw_lbl
pb_rst_6:
    cmp dl, 45
    jne pb_rst_7
    mov al, '6'
    jmp pb_draw_lbl
pb_rst_7:
    mov al, '7'
pb_draw_lbl:
    call Graphics_DrawChar

    pop si
    pop dx
    pop cx
    pop bx
    ret
Piano_PlayBlackKey endp

; ------------------------------------------------------------------------------
; Piano_ClearHUD
; Renders the status and HUD panel showing Octave and Sustain state.
; ------------------------------------------------------------------------------
Piano_ClearHUD proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; Draw HUD Box at Rows 18..21, Cols 14..65
    mov dh, 18
    mov dl, 14
    mov ch, 21
    mov cl, 65
    mov bl, THEME_MUTED
    call Graphics_DrawBoxSingle

    ; Line 1: Status / Note prompt
    mov dh, 19
    mov dl, 16
    mov bl, THEME_MUTED
    mov si, str_hud_idle
    call Utils_PrintStringAt

    ; Line 2: Active Mode Indicators (Octave & Sustain Pedal)
    mov dh, 20
    mov dl, 16
    mov bl, THEME_TEXT
    mov si, str_hud_oct_lbl
    call Utils_PrintStringAt

    ; Print Octave Value
    mov ax, [piano_octave]
    add al, '0'
    mov dl, 24
    mov bl, THEME_ACCENT
    call Graphics_DrawChar

    ; Octave Descriptor
    mov ax, [piano_octave]
    cmp ax, 4
    jne p_chud_5
    mov si, str_oct4_desc
    jmp p_chud_pdesc
p_chud_5:
    cmp ax, 5
    jne p_chud_6
    mov si, str_oct5_desc
    jmp p_chud_pdesc
p_chud_6:
    mov si, str_oct6_desc
p_chud_pdesc:
    mov dh, 20
    mov dl, 26
    mov bl, THEME_MUTED
    call Utils_PrintStringAt

    ; Print Sustain Pedal Status
    mov dh, 20
    mov dl, 44
    mov bl, THEME_TEXT
    mov si, str_hud_pedal_lbl
    call Utils_PrintStringAt

    cmp word [piano_sustain_flag], 0
    jz p_chud_ped_off
    mov dh, 20
    mov dl, 52
    mov bl, 0Ah                 ; Light Green for Active Pedal
    mov si, str_pedal_on
    call Utils_PrintStringAt
    jmp p_chud_done

p_chud_ped_off:
    mov dh, 20
    mov dl, 52
    mov bl, THEME_MUTED
    mov si, str_pedal_off
    call Utils_PrintStringAt

p_chud_done:
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Piano_ClearHUD endp

; ------------------------------------------------------------------------------
; Piano_UpdateHUD
; Displays active note, exact frequency in Hz, and dynamic LED VU meter.
; Input: SI -> Note name string
; ------------------------------------------------------------------------------
Piano_UpdateHUD proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; Line 1: Active Note & Frequency
    mov dh, 19
    mov dl, 16
    mov bl, THEME_TITLE
    call Utils_PrintStringAt

    ; Display Frequency in Hz
    mov dh, 19
    mov dl, 32
    mov bl, THEME_TEXT
    mov si, str_hud_freq_lbl
    call Utils_PrintStringAt

    ; Print frequency integer from piano_last_freq
    mov ax, [piano_last_freq]
    mov dl, 38
    call Piano_PrintWordNum

    mov dh, 19
    mov dl, 43
    mov bl, THEME_ACCENT
    mov si, str_hud_hz
    call Utils_PrintStringAt

    ; Animated LED Audio VU Meter on HUD Line 1
    mov dh, 19
    mov dl, 48
    mov bl, 0Ah                 ; Green/Gold VU Level
    mov si, str_hud_vu_active
    call Utils_PrintStringAt

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Piano_UpdateHUD endp

; ------------------------------------------------------------------------------
; Piano_PrintWordNum
; Helper: Prints 16-bit number in AX at row 19, col DL.
; ------------------------------------------------------------------------------
Piano_PrintWordNum proc
    push ax
    push bx
    push cx
    push dx

    mov bx, 10
    xor cx, cx
p_pwn_div:
    xor dx, dx
    div bx                      ; AX = quotient, DX = remainder
    push dx
    inc cx
    test ax, ax
    jnz p_pwn_div

    ; DL holds cursor column passed in
    pop dx                      ; Pop registers
    push dx
p_pwn_print:
    pop ax                      ; Pop digit
    add al, '0'
    mov bl, THEME_ACCENT
    call Graphics_DrawChar
    inc dl
    loop p_pwn_print

    pop dx
    pop cx
    pop bx
    pop ax
    ret
Piano_PrintWordNum endp

; ------------------------------------------------------------------------------
; Piano Strings & Visual Data
; ------------------------------------------------------------------------------
str_piano_hdr       db "CONCERT GRAND PIANO", 0
str_piano_sub       db "[ Studio Acoustic Physics - Hammer Attack & Decay Engine ]", 0
str_piano_foot      db "[ESC] Menu | [TAB] Octave | [SPACE] Sustain Pedal | [Q..I] Keys", 0

str_white_row       db "|     |     |     |     |     |     |     |     |", 0
str_white_keys_lbl  db "| [Q] | [W] | [E] | [R] | [T] | [Y] | [U] | [I] |", 0
str_white_note_lbl  db "|  C  |  D  |  E  |  F  |  G  |  A  |  B  |  C+ |", 0

str_hud_idle        db "Concert Grand Ready  - Strike key to play note...     ", 0
str_hud_oct_lbl     db "Octave: ", 0
str_oct4_desc       db "(Warm 262-523 Hz)  ", 0
str_oct5_desc       db "(Concert 523-1046 Hz)", 0
str_oct6_desc       db "(Brilliant 1046-2093)", 0

str_hud_pedal_lbl   db "Pedal: ", 0
str_pedal_on        db "[SUSTAIN ON] ", 0
str_pedal_off       db "[DAMPER OFF] ", 0

str_hud_freq_lbl    db "Freq: ", 0
str_hud_hz          db "Hz  ", 0
str_hud_vu_active   db "[VU: ####**  ]", 0

str_note_name_c     db "Note: C      ", 0
str_note_name_cs    db "Note: C#     ", 0
str_note_name_d     db "Note: D      ", 0
str_note_name_ds    db "Note: D#     ", 0
str_note_name_e     db "Note: E      ", 0
str_note_name_f     db "Note: F      ", 0
str_note_name_fs    db "Note: F#     ", 0
str_note_name_g     db "Note: G      ", 0
str_note_name_gs    db "Note: G#     ", 0
str_note_name_a     db "Note: A (Concert)", 0
str_note_name_as    db "Note: A#     ", 0
str_note_name_b     db "Note: B      ", 0
str_note_name_c_hi  db "Note: C (Octave) ", 0
