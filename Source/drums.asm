; ==============================================================================
; CRIMSON ORBIT – MUSICAL BAND
; Module: Simulated Studio Drum Kit (drums.asm)
; Target Assembler: emu8086
; Professional 7-piece acoustic percussion workstation with LFSR white-noise
; synthesis, punchy acoustic bass drum, dual-layer snare wire & shell pop,
; metallic hi-hats (closed & open), explosive crash cymbal, and live HUD.
; ==============================================================================

Drums_Run proc
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
    mov si, str_drums_hdr
    call Graphics_DrawHeader

    mov dh, 4
    mov dl, 17
    mov bl, THEME_ACCENT
    mov si, str_drums_sub
    call Utils_PrintStringAt

    ; 3. Draw Drum Pads
    call Drums_DrawKit

    ; 4. Draw HUD
    call Drums_ClearHUD

    ; 5. Draw Footer
    mov si, str_drums_foot
    call Graphics_DrawFooter

drums_event_loop:
    call Keyboard_WaitKey

    cmp al, KEY_ESC
    je drums_exit

    call Keyboard_ToUpper

    cmp al, 'Q'
    jne d_chk_w
    ; Strike Kick Drum
    mov si, str_d_kick
    call Drums_StrikeKick
    jmp drums_event_loop

d_chk_w:
    cmp al, 'W'
    jne d_chk_e
    ; Strike Snare Drum
    mov si, str_d_snare
    call Drums_StrikeSnare
    jmp drums_event_loop

d_chk_e:
    cmp al, 'E'
    jne d_chk_y
    ; Strike Closed Hi-Hat
    mov si, str_d_hihat
    call Drums_StrikeHiHat
    jmp drums_event_loop

d_chk_y:
    cmp al, 'Y'
    jne d_chk_r
    ; Strike Open Hi-Hat
    mov si, str_d_open_hh
    call Drums_StrikeOpenHiHat
    jmp drums_event_loop

d_chk_r:
    cmp al, 'R'
    jne d_chk_t
    ; Strike Tom
    mov si, str_d_tom
    call Drums_StrikeTom
    jmp drums_event_loop

d_chk_t:
    cmp al, 'T'
    jne d_chk_u
    ; Strike Crash
    mov si, str_d_crash
    call Drums_StrikeCrash
    jmp drums_event_loop

d_chk_u:
    cmp al, 'U'
    jne drums_event_loop
    ; Strike Ride Cymbal
    mov si, str_d_ride
    call Drums_StrikeRide
    jmp drums_event_loop

drums_exit:
    call Speaker_ToneOff
    call Utils_ShowCursor
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Drums_Run endp

; ------------------------------------------------------------------------------
; Drums_DrawKit
; Draws the 6 visual drum pads in rest state.
; ------------------------------------------------------------------------------
Drums_DrawKit proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; Pad 1: Crash Cymbal (Top Left: Rows 6..9, Cols 5..24)
    mov dh, 6
    mov dl, 5
    mov ch, 9
    mov cl, 24
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble
    mov dh, 7
    mov dl, 7
    mov bl, THEME_ACCENT
    mov si, str_lbl_crash
    call Utils_PrintStringAt
    mov dh, 8
    mov dl, 7
    mov bl, THEME_TEXT
    mov si, str_key_crash
    call Utils_PrintStringAt

    ; Pad 2: Hi-Hat Pair (Mid Left: Rows 11..15, Cols 5..24)
    mov dh, 11
    mov dl, 5
    mov ch, 15
    mov cl, 24
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble
    mov dh, 12
    mov dl, 7
    mov bl, THEME_ACCENT
    mov si, str_lbl_hihat
    call Utils_PrintStringAt
    mov dh, 13
    mov dl, 7
    mov bl, THEME_TEXT
    mov si, str_key_hihat
    call Utils_PrintStringAt
    mov dh, 14
    mov dl, 7
    mov bl, THEME_MUTED
    mov si, str_key_open_hh
    call Utils_PrintStringAt

    ; Pad 3: Tom-Tom (Top Right: Rows 6..9, Cols 55..74)
    mov dh, 6
    mov dl, 55
    mov ch, 9
    mov cl, 74
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble
    mov dh, 7
    mov dl, 57
    mov bl, THEME_ACCENT
    mov si, str_lbl_tom
    call Utils_PrintStringAt
    mov dh, 8
    mov dl, 57
    mov bl, THEME_TEXT
    mov si, str_key_tom
    call Utils_PrintStringAt

    ; Pad 4: Snare Drum (Mid Right: Rows 11..15, Cols 55..74)
    mov dh, 11
    mov dl, 55
    mov ch, 15
    mov cl, 74
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble
    mov dh, 12
    mov dl, 57
    mov bl, THEME_ACCENT
    mov si, str_lbl_snare
    call Utils_PrintStringAt
    mov dh, 13
    mov dl, 57
    mov bl, THEME_TEXT
    mov si, str_key_snare
    call Utils_PrintStringAt
    mov dh, 14
    mov dl, 57
    mov bl, THEME_MUTED
    mov si, str_lbl_snare_wire
    call Utils_PrintStringAt

    ; Pad 5: Bass Kick Drum (Center Stage: Rows 8..15, Cols 28..51)
    mov dh, 8
    mov dl, 28
    mov ch, 15
    mov cl, 51
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    ; Resonant drumhead graphic
    mov dh, 10
    mov dl, 31
    mov bl, THEME_TITLE
    mov si, str_lbl_kick
    call Utils_PrintStringAt

    mov dh, 11
    mov dl, 33
    mov bl, THEME_ACCENT
    mov si, str_lbl_kick_brand
    call Utils_PrintStringAt

    mov dh, 13
    mov dl, 34
    mov bl, THEME_TEXT
    mov si, str_key_kick
    call Utils_PrintStringAt

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Drums_DrawKit endp

; ------------------------------------------------------------------------------
; Drums Strike Handlers
; ------------------------------------------------------------------------------

; Strike Kick (Center Stage 22" Bass Drum)
Drums_StrikeKick proc
    push ax
    push bx
    push cx
    push dx
    push si

    call Drums_UpdateHUD

    ; Flash Kick Pad border in Bright White
    mov dh, 8
    mov dl, 28
    mov ch, 15
    mov cl, 51
    mov bl, COLOR_WHITE
    call Graphics_DrawBoxDouble

    ; Sound synthesis (punchy beater attack + acoustic shell glide)
    call Sound_Kick

    ; Restore normal border
    mov dh, 8
    mov dl, 28
    mov ch, 15
    mov cl, 51
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Drums_StrikeKick endp

; Strike Snare (Mid Right Pad)
Drums_StrikeSnare proc
    push ax
    push bx
    push cx
    push dx
    push si

    call Drums_UpdateHUD

    ; Flash Snare Pad border in Gold
    mov dh, 11
    mov dl, 55
    mov ch, 15
    mov cl, 74
    mov bl, COLOR_GOLD
    call Graphics_DrawBoxDouble

    ; Dual-layer acoustic snare: LFSR wire sizzle + wooden shell pop
    call Sound_Snare

    ; Restore border
    mov dh, 11
    mov dl, 55
    mov ch, 15
    mov cl, 74
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Drums_StrikeSnare endp

; Strike Closed Hi-Hat (Mid Left Pad)
Drums_StrikeHiHat proc
    push ax
    push bx
    push cx
    push dx
    push si

    call Drums_UpdateHUD

    ; Flash Hi-Hat Pad border in Light Cyan
    mov dh, 11
    mov dl, 5
    mov ch, 15
    mov cl, 24
    mov bl, COLOR_LIGHTCYAN
    call Graphics_DrawBoxDouble

    call Sound_HiHat

    ; Restore border
    mov dh, 11
    mov dl, 5
    mov ch, 15
    mov cl, 24
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Drums_StrikeHiHat endp

; Strike Open Hi-Hat
Drums_StrikeOpenHiHat proc
    push ax
    push bx
    push cx
    push dx
    push si

    call Drums_UpdateHUD

    mov dh, 11
    mov dl, 5
    mov ch, 15
    mov cl, 24
    mov bl, COLOR_WHITE
    call Graphics_DrawBoxDouble

    call Sound_HiHat_Open

    mov dh, 11
    mov dl, 5
    mov ch, 15
    mov cl, 24
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Drums_StrikeOpenHiHat endp

; Strike Tom (Top Right Pad)
Drums_StrikeTom proc
    push ax
    push bx
    push cx
    push dx
    push si

    call Drums_UpdateHUD

    mov dh, 6
    mov dl, 55
    mov ch, 9
    mov cl, 74
    mov bl, COLOR_GOLD
    call Graphics_DrawBoxDouble

    call Sound_Tom

    mov dh, 6
    mov dl, 55
    mov ch, 9
    mov cl, 74
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Drums_StrikeTom endp

; Strike Crash Cymbal (Top Left Pad)
Drums_StrikeCrash proc
    push ax
    push bx
    push cx
    push dx
    push si

    call Drums_UpdateHUD

    mov dh, 6
    mov dl, 5
    mov ch, 9
    mov cl, 24
    mov bl, COLOR_WHITE
    call Graphics_DrawBoxDouble

    call Sound_Crash

    mov dh, 6
    mov dl, 5
    mov ch, 9
    mov cl, 24
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Drums_StrikeCrash endp

; Strike Ride Cymbal Bell
Drums_StrikeRide proc
    push ax
    push bx
    push cx
    push dx
    push si

    call Drums_UpdateHUD

    mov dh, 6
    mov dl, 55
    mov ch, 9
    mov cl, 74
    mov bl, COLOR_LIGHTCYAN
    call Graphics_DrawBoxDouble

    call Sound_Ride

    mov dh, 6
    mov dl, 55
    mov ch, 9
    mov cl, 74
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Drums_StrikeRide endp

; ------------------------------------------------------------------------------
; HUD Procedures
; ------------------------------------------------------------------------------
Drums_ClearHUD proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; Single box at Rows 18..21, Cols 10..70
    mov dh, 18
    mov dl, 10
    mov ch, 21
    mov cl, 70
    mov bl, THEME_MUTED
    call Graphics_DrawBoxSingle

    mov dh, 19
    mov dl, 13
    mov bl, THEME_MUTED
    mov si, str_d_hud_idle
    call Utils_PrintStringAt

    mov dh, 20
    mov dl, 13
    mov bl, THEME_TEXT
    mov si, str_d_hud_tech
    call Utils_PrintStringAt

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Drums_ClearHUD endp

Drums_UpdateHUD proc
    push ax
    push bx
    push dx
    push si

    mov dh, 19
    mov dl, 13
    mov bl, THEME_TITLE
    call Utils_PrintStringAt

    ; Flash Impact Meter on Row 20
    mov dh, 20
    mov dl, 50
    mov bl, 0Ah                 ; Light Green VU impact
    mov si, str_d_impact_meter
    call Utils_PrintStringAt

    pop si
    pop dx
    pop bx
    pop ax
    ret
Drums_UpdateHUD endp

; ------------------------------------------------------------------------------
; Drums Strings & Visual Labels
; ------------------------------------------------------------------------------
str_drums_hdr       db "STUDIO DRUM WORKSTATION", 0
str_drums_sub       db "[ LFSR White Noise & Acoustic Physical Percussion Synthesis ]", 0
str_drums_foot      db "[ESC] Menu | [Q] Kick [W] Snare [E] Closed HH [Y] Open HH [R] Tom [T] Crash [U] Ride", 0

str_lbl_crash       db "CRASH CYMBAL", 0
str_key_crash       db "  Key: [T]", 0

str_lbl_hihat       db "HI-HAT PAIR", 0
str_key_hihat       db "  [E] Closed", 0
str_key_open_hh     db "  [Y] Open", 0

str_lbl_tom         db "  TOM-TOM", 0
str_key_tom         db "  Key: [R]", 0

str_lbl_snare       db "SNARE DRUM", 0
str_key_snare       db " Key: [W]", 0
str_lbl_snare_wire  db " Wire+Shell", 0

str_lbl_kick        db "22in BASS KICK", 0
str_lbl_kick_brand  db "- CRIMSON -", 0
str_key_kick        db "Key: [Q]", 0

str_d_hud_idle      db "Studio Kit Ready - Strike drum pads [Q, W, E, Y, R, T, U]... ", 0
str_d_hud_tech      db "Synthesis: 16-Bit LFSR White Noise + Acoustic Shell Glides  ", 0
str_d_impact_meter  db "[IMPACT: #####*]", 0

str_d_kick          db "Hit: KICK DRUM    Punch Transient + Resonant Shell [Q]     ", 0
str_d_snare         db "Hit: SNARE DRUM   LFSR Wire Sizzle + Wooden Pop [W]        ", 0
str_d_hihat         db "Hit: HI-HAT       Ultra-Crisp Metallic Choke [E]           ", 0
str_d_open_hh       db "Hit: OPEN HI-HAT  Shimmering Sizzle Decay [Y]              ", 0
str_d_tom           db "Hit: TOM-TOM      Resonant Stick Impact & Glide [R]        ", 0
str_d_crash         db "Hit: CRASH CYMBAL Explosive Metallic Splash Decay [T]      ", 0
str_d_ride          db "Hit: RIDE CYMBAL  Clear High Bell Ping (1318 Hz) [U]       ", 0
