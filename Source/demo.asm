; ==============================================================================
; CRIMSON ORBIT – MUSICAL BAND
; Module: Demo Songs Player & Visualizer (demo.asm)
; Target Assembler: emu8086
; Features: Song selection (1..6), Realistic Instrument synthesis (Concert Piano,
; Singing Acoustic/Lead Guitar, Studio Drums), real-time spectrum visualizer with
; dancing audio equalizer bars, live frequency (Hz) HUD, and live ESC abort.
; ==============================================================================

Demo_Run proc
    push ax
    push bx
    push cx
    push dx
    push si
    push di

demo_menu_loop:
    ; 1. Clear Screen
    mov bl, 07h
    call Utils_ClearScreen
    call Utils_HideCursor

    ; 2. Render Demo Songs Menu Box
    mov dh, 3
    mov dl, 16
    mov ch, 20
    mov cl, 63
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    ; Header
    mov dh, 4
    mov dl, 27
    mov bl, THEME_TITLE
    mov si, str_demo_banner1
    call Utils_PrintStringAt

    mov dh, 5
    mov dl, 24
    mov bl, THEME_ACCENT
    mov si, str_demo_banner2
    call Utils_PrintStringAt

    ; Horizontal Separator
    mov dh, 6
    mov dl, 17
    mov cx, 46
    mov al, CP437_S_H
    mov bl, THEME_MUTED
    call Graphics_DrawHLine

    ; Song Options 1..6
    mov bl, THEME_TEXT
    mov dh, 8
    mov dl, 20
    mov si, str_opt_song1
    call Utils_PrintStringAt

    mov dh, 9
    mov dl, 20
    mov si, str_opt_song2
    call Utils_PrintStringAt

    mov dh, 10
    mov dl, 20
    mov si, str_opt_song3
    call Utils_PrintStringAt

    mov dh, 11
    mov dl, 20
    mov si, str_opt_song4
    call Utils_PrintStringAt

    mov dh, 12
    mov dl, 20
    mov si, str_opt_song5
    call Utils_PrintStringAt

    mov dh, 13
    mov dl, 20
    mov si, str_opt_song6
    call Utils_PrintStringAt

    ; Back Option 7
    mov bl, THEME_ACCENT
    mov dh, 15
    mov dl, 20
    mov si, str_opt_song7
    call Utils_PrintStringAt

    ; Prompt
    mov bl, THEME_TITLE
    mov dh, 18
    mov dl, 20
    mov si, str_demo_prompt
    call Utils_PrintStringAt

    ; Footer
    mov si, str_demo_foot
    call Graphics_DrawFooter

demo_wait_song_choice:
    call Keyboard_WaitKey

    cmp al, KEY_ESC
    je demo_exit

    cmp al, '7'
    je demo_exit

    cmp al, '1'
    jb demo_wait_song_choice
    cmp al, '6'
    ja demo_wait_song_choice

    ; Valid song selection (1..6)
    sub al, '1'
    xor ah, ah
    mov [selected_song_idx], al

    ; Advance to Instrument Selection Screen
    call Demo_ChooseInstrument
    test al, al
    jz demo_menu_loop           ; If cancelled with ESC, return to song menu

    ; Play the selected song with chosen instrument
    call Demo_PlaySong
    jmp demo_menu_loop

demo_exit:
    call Speaker_ToneOff
    call Utils_ShowCursor
    pop di
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Demo_Run endp

; ------------------------------------------------------------------------------
; Demo_ChooseInstrument
; Submenu: Prompts user to select instrument mode (1=Piano, 2=Guitar, 3=Drums).
; Output: AL = 1 (Piano), 2 (Guitar), 3 (Drums), or 0 if cancelled (ESC).
; ------------------------------------------------------------------------------
Demo_ChooseInstrument proc
    push bx
    push cx
    push dx
    push si

    ; Draw Instrument Modal Box at Rows 8..18, Cols 22..58
    mov dh, 8
    mov dl, 22
    mov ch, 18
    mov cl, 58
    mov bl, THEME_TITLE
    call Graphics_DrawBoxDouble

    mov dh, 9
    mov dl, 28
    mov bl, THEME_TITLE
    mov si, str_inst_title
    call Utils_PrintStringAt

    mov dh, 10
    mov dl, 23
    mov cx, 35
    mov al, CP437_S_H
    mov bl, THEME_MUTED
    call Graphics_DrawHLine

    mov bl, THEME_TEXT
    mov dh, 12
    mov dl, 25
    mov si, str_inst_opt1
    call Utils_PrintStringAt

    mov dh, 13
    mov dl, 25
    mov si, str_inst_opt2
    call Utils_PrintStringAt

    mov dh, 14
    mov dl, 25
    mov si, str_inst_opt3
    call Utils_PrintStringAt

    mov bl, THEME_MUTED
    mov dh, 16
    mov dl, 25
    mov si, str_inst_cancel
    call Utils_PrintStringAt

demo_wait_inst:
    call Keyboard_WaitKey

    cmp al, KEY_ESC
    jne d_chk_inst_1
    xor al, al                  ; Cancelled
    jmp demo_inst_done

d_chk_inst_1:
    cmp al, '1'
    jb demo_wait_inst
    cmp al, '3'
    ja demo_wait_inst

    ; Valid choice: '1', '2', or '3'
    sub al, '0'
    mov [selected_inst_idx], al

demo_inst_done:
    pop si
    pop dx
    pop cx
    pop bx
    ret
Demo_ChooseInstrument endp

; ------------------------------------------------------------------------------
; Demo_PlaySong
; Executes playback loop for selected_song_idx with selected_inst_idx.
; Renders live visualizer, updates HUD, checks for ESC to break.
; ------------------------------------------------------------------------------
Demo_PlaySong proc
    push ax
    push bx
    push cx
    push dx
    push si
    push di

    ; Clear Screen & Setup Visualizer Stage
    mov bl, 07h
    call Utils_ClearScreen
    call Utils_HideCursor

    ; Top Header
    mov si, str_vis_hdr
    call Graphics_DrawHeader

    ; Info Bar (Song Title + Instrument)
    mov dh, 3
    mov dl, 10
    mov bl, THEME_ACCENT
    mov si, str_now_playing
    call Utils_PrintStringAt

    ; Print Selected Song Title
    xor bx, bx
    mov bl, [selected_song_idx]
    shl bx, 1                   ; 2 bytes per pointer
    mov si, [song_titles + bx]
    mov bl, THEME_TITLE
    mov dh, 3
    mov dl, 23
    call Utils_PrintStringAt

    ; Print Selected Instrument Name
    mov dh, 4
    mov dl, 10
    mov bl, THEME_ACCENT
    mov si, str_inst_style
    call Utils_PrintStringAt

    mov al, [selected_inst_idx]
    cmp al, 1
    jne d_ps_g
    mov si, str_inst_name_piano
    jmp d_ps_show_inst
d_ps_g:
    cmp al, 2
    jne d_ps_d
    mov si, str_inst_name_guitar
    jmp d_ps_show_inst
d_ps_d:
    mov si, str_inst_name_drums
d_ps_show_inst:
    mov bl, THEME_TITLE
    mov dh, 4
    mov dl, 23
    call Utils_PrintStringAt

    ; Draw Visualizer Spectrum Stage (Rows 6..18, Cols 10..70)
    mov dh, 6
    mov dl, 10
    mov ch, 18
    mov cl, 70
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    ; Draw Frequency Spectrum Column Labels (Row 17)
    mov dh, 17
    mov dl, 12
    mov bl, THEME_TEXT
    mov si, str_spec_labels
    call Utils_PrintStringAt

    ; Bottom Footer Instruction
    mov si, str_vis_foot
    call Graphics_DrawFooter

    ; Locate Song Data Table
    xor bx, bx
    mov bl, [selected_song_idx]
    shl bx, 1
    mov si, [song_table + bx]    ; SI -> Song score array

play_score_loop:
    ; Read Note: [SI] = Frequency (word), [SI+2] = Duration (word)
    lodsw                       ; AX = Frequency
    cmp ax, SONG_END
    je song_finished

    mov bx, ax                  ; BX = Frequency
    lodsw
    mov cx, ax                  ; CX = Duration in ms

    ; Check for user ESC abort before playing note
    call Keyboard_CheckKey
    jz no_key_abort
    call Keyboard_WaitKey       ; Consume key
    cmp al, KEY_ESC
    je song_aborted

no_key_abort:
    ; Animate Visualizer Spectrum Column for Frequency in BX
    call Demo_UpdateVisualizer

    ; Play note sound according to selected realistic instrument
    mov ax, bx                  ; AX = Frequency
    mov dl, [selected_inst_idx]

    cmp dl, 1
    jne chk_inst_guitar
    ; Style 1: Concert Piano (Hammer Attack & Decay Engine)
    call Speaker_PianoTone
    jmp note_play_done

chk_inst_guitar:
    cmp dl, 2
    jne chk_inst_drums
    ; Style 2: Guitar (Plectrum transient + singing acoustic vibrato)
    call Speaker_GuitarPluckPro
    jmp note_play_done

chk_inst_drums:
    ; Style 3: Studio Drums (Acoustic percussion groove interpretation)
    test ax, ax
    jz drum_rest
    cmp ax, 600
    ja drum_mid
    call Sound_Kick             ; Low pitch note -> punchy acoustic kick
    jmp drum_wait
drum_mid:
    cmp ax, 750
    ja drum_high
    call Sound_Snare            ; Mid pitch note -> LFSR snare rattle + pop
    jmp drum_wait
drum_high:
    cmp ax, 950
    ja drum_peak
    call Sound_Tom              ; High note -> resonant tom
    jmp drum_wait
drum_peak:
    call Sound_Crash            ; Peak note -> explosive crash cymbal
    jmp drum_wait
drum_rest:
    call Sound_HiHat            ; Rest -> tight closed hi-hat click
drum_wait:
    ; Wait remaining duration
    cmp cx, 40
    jbe note_play_done
    sub cx, 35
    call Utils_DelayMs

note_play_done:
    ; Clear active spectrum bars back to resting
    call Demo_ClearVisualizer

    jmp play_score_loop

song_finished:
    call Speaker_ToneOff
    ; Brief high-fidelity concert victory fanfare
    mov ax, 1046
    mov cx, 90
    call Speaker_PlayToneMs
    mov ax, 1318
    mov cx, 90
    call Speaker_PlayToneMs
    mov ax, 1568
    mov cx, 200
    call Speaker_PlayToneMs

    ; Display Completion Message
    mov dh, 20
    mov dl, 20
    mov bl, THEME_ACCENT
    mov si, str_song_complete
    call Utils_PrintStringAt

    call Keyboard_WaitAnyKey
    jmp song_return

song_aborted:
    call Speaker_ToneOff

song_return:
    pop di
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Demo_PlaySong endp

; ------------------------------------------------------------------------------
; Visualizer Helpers
; ------------------------------------------------------------------------------
Demo_UpdateVisualizer proc
    ; BX = Frequency in Hz
    push ax
    push bx
    push cx
    push dx

    test bx, bx
    jz vis_up_done              ; Rest note -> no bar

    ; Map concert frequency to column 0..7
    ; C5 (~523): col 14
    ; D5 (~587): col 21
    ; E5 (~659): col 28
    ; F5 (~698): col 35
    ; G5 (~784): col 42
    ; A5 (~880): col 49
    ; B5 (~988): col 56
    ; C6 (~1046+): col 63
    mov dl, 14
    cmp bx, 550
    jb vis_col_found
    mov dl, 21
    cmp bx, 620
    jb vis_col_found
    mov dl, 28
    cmp bx, 680
    jb vis_col_found
    mov dl, 35
    cmp bx, 740
    jb vis_col_found
    mov dl, 42
    cmp bx, 830
    jb vis_col_found
    mov dl, 49
    cmp bx, 930
    jb vis_col_found
    mov dl, 56
    cmp bx, 1010
    jb vis_col_found
    mov dl, 63

vis_col_found:
    ; Draw dancing equalizer bar in Gold/Crimson (Rows 9..16, 4 chars wide)
    mov dh, 9
vis_draw_bar:
    mov cx, 4
    mov al, CP437_BLOCK_FULL
    mov bl, THEME_TITLE
    call Graphics_DrawHLine
    inc dh
    cmp dh, 16
    jbe vis_draw_bar

vis_up_done:
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Demo_UpdateVisualizer endp

Demo_ClearVisualizer proc
    push ax
    push bx
    push cx
    push dx

    ; Clear equalizer bar area (Rows 9..16, Cols 12..68)
    mov dh, 9
    mov dl, 12
    mov ch, 16
    mov cl, 68
    mov al, ' '
    mov bl, 07h
    call Graphics_FillArea

    pop dx
    pop cx
    pop bx
    pop ax
    ret
Demo_ClearVisualizer endp

; ------------------------------------------------------------------------------
; Demo Data & Strings
; ------------------------------------------------------------------------------
selected_song_idx   db 0
selected_inst_idx   db 1

str_demo_banner1    db "CRIMSON ORBIT", 0
str_demo_banner2    db "DEMO SONGS REPERTOIRE", 0

str_opt_song1       db "[1] Happy Birthday (Concert)", 0
str_opt_song2       db "[2] Twinkle Twinkle Little Star", 0
str_opt_song3       db "[3] Ode to Joy (Beethoven 9th)", 0
str_opt_song4       db "[4] Jingle Bells (High-Hz)", 0
str_opt_song5       db "[5] Mary Had a Little Lamb", 0
str_opt_song6       db "[6] London Bridge Is Falling Down", 0
str_opt_song7       db "[7] Back to Main Menu", 0

str_demo_prompt     db "Select Song [1..7]: ", 0
str_demo_foot       db "[ESC / 7] Return to Main Menu  |  [1..6] Select Song", 0

str_inst_title      db "CHOOSE REAL INSTRUMENT", 0
str_inst_opt1       db "[1] Concert Grand Piano (Hammer & Decay)", 0
str_inst_opt2       db "[2] Lead Guitar (Pick & Vibrato)", 0
str_inst_opt3       db "[3] Studio Drum Kit (LFSR Percussion)", 0
str_inst_cancel     db "[ESC] Cancel & Back", 0

str_vis_hdr         db "DEMO SONGS PLAYBACK", 0
str_now_playing     db "Song:       ", 0
str_inst_style      db "Instrument: ", 0
str_inst_name_piano db "Concert Grand Piano (Hammer/Decay)", 0
str_inst_name_guitar db "Singing Acoustic / Lead Guitar   ", 0
str_inst_name_drums db "Studio LFSR Percussion Groove    ", 0

str_spec_labels     db "[ C5]  [ D5]  [ E5]  [ F5]  [ G5]  [ A5]  [ B5]  [ C6]", 0
str_vis_foot        db "[ESC] Abort Playback & Return to Song Menu", 0
str_song_complete   db "*** Performance Finished! Press Any Key ***", 0
