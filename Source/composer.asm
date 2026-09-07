; ==============================================================================
; CRIMSON ORBIT – MUSICAL BAND
; Module: Custom Music Composer & Live Track Recorder (composer.asm)
; Target Assembler: emu8086
; Features:
; - Real-time custom song creation directly into 8086 RAM memory
; - Interactive piano keyboard layout with instant audible preview
; - Visual multi-slot Track Tape showing composed notes
; - Dynamic Note Duration selector (150ms, 300ms, 600ms, 1000ms)
; - Undo / Backspace, Clear Song, and Load Starter Preset
; - Full in-engine playback of user-created custom songs
; - Interoperable with Demo Songs Repertoire (Song 7)
; ==============================================================================

Composer_Run proc
    push ax
    push bx
    push cx
    push dx
    push si
    push di

composer_redraw_all:
    ; 1. Clear Screen
    mov bl, 07h
    call Utils_ClearScreen
    call Utils_HideCursor

    ; 2. Outer Decorative Frame Box (Rows 2..22, Cols 6..73)
    mov dh, 2
    mov dl, 6
    mov ch, 22
    mov cl, 73
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    ; 3. Header Titles
    mov dh, 3
    mov dl, 16
    mov bl, THEME_TITLE
    mov si, str_comp_title1
    call Utils_PrintStringAt

    mov dh, 4
    mov dl, 14
    mov bl, THEME_ACCENT
    mov si, str_comp_title2
    call Utils_PrintStringAt

    ; 4. Horizontal Separator
    mov dh, 5
    mov dl, 7
    mov cx, 66
    mov al, CP437_S_H
    mov bl, THEME_MUTED
    call Graphics_DrawHLine

    ; 5. Draw Track Tape Frame (Rows 6..9, Cols 8..71)
    mov dh, 6
    mov dl, 8
    mov ch, 9
    mov cl, 71
    mov bl, THEME_ACCENT
    call Graphics_DrawBoxSingle

    mov dh, 6
    mov dl, 12
    mov bl, THEME_TITLE
    mov si, str_comp_track_hdr
    call Utils_PrintStringAt

    ; 6. Render Current Notes on Track Tape
    call Composer_DrawTrackTape

    ; 7. Draw Keyboard Layout Frame (Rows 11..16, Cols 8..71)
    mov dh, 11
    mov dl, 8
    mov ch, 16
    mov cl, 71
    mov bl, THEME_BORDER
    call Graphics_DrawBoxSingle

    mov dh, 11
    mov dl, 12
    mov bl, THEME_TITLE
    mov si, str_comp_kb_hdr
    call Utils_PrintStringAt

    ; Black Keys Row
    mov dh, 12
    mov dl, 14
    mov bl, THEME_MUTED
    mov si, str_comp_keys_black
    call Utils_PrintStringAt

    mov dh, 13
    mov dl, 14
    mov bl, THEME_TEXT
    mov si, str_comp_names_black
    call Utils_PrintStringAt

    ; White Keys Row
    mov dh, 14
    mov dl, 12
    mov bl, THEME_ACCENT
    mov si, str_comp_keys_white
    call Utils_PrintStringAt

    mov dh, 15
    mov dl, 12
    mov bl, THEME_TEXT
    mov si, str_comp_names_white
    call Utils_PrintStringAt

    ; 8. Draw Control Commands (Rows 18..20)
    mov dh, 18
    mov dl, 10
    mov bl, THEME_ACCENT
    mov si, str_comp_cmd1
    call Utils_PrintStringAt

    mov dh, 19
    mov dl, 10
    mov bl, THEME_TEXT
    mov si, str_comp_cmd2
    call Utils_PrintStringAt

    mov dh, 20
    mov dl, 10
    mov bl, THEME_MUTED
    mov si, str_comp_cmd3
    call Utils_PrintStringAt

    ; 9. Draw Footer
    mov si, str_comp_foot
    call Graphics_DrawFooter

composer_input_loop:
    call Keyboard_WaitKey

    cmp al, KEY_ESC
    je composer_exit

    ; Check Duration Selectors: '1'..'4'
    cmp al, '1'
    jne comp_chk_2
    mov word [custom_note_dur], 150
    call Composer_DrawTrackTape
    jmp composer_input_loop

comp_chk_2:
    cmp al, '2'
    jne comp_chk_3
    mov word [custom_note_dur], 300
    call Composer_DrawTrackTape
    jmp composer_input_loop

comp_chk_3:
    cmp al, '3'
    jne comp_chk_4
    mov word [custom_note_dur], 600
    call Composer_DrawTrackTape
    jmp composer_input_loop

comp_chk_4:
    cmp al, '4'
    jne comp_chk_cmd
    mov word [custom_note_dur], 1000
    call Composer_DrawTrackTape
    jmp composer_input_loop

comp_chk_cmd:
    ; Check for 'P' / 'p' to Play
    cmp al, 'P'
    je comp_do_play
    cmp al, 'p'
    je comp_do_play

    ; Check for 'C' / 'c' to Clear
    cmp al, 'C'
    je comp_do_clear
    cmp al, 'c'
    je comp_do_clear

    ; Check for 'B' / 'b' or Backspace (ASCII 8) to Undo
    cmp al, 'B'
    je comp_do_undo
    cmp al, 'b'
    je comp_do_undo
    cmp al, 8
    je comp_do_undo

    ; Check for 'L' / 'l' to Load Preset
    cmp al, 'L'
    je comp_do_preset
    cmp al, 'l'
    je comp_do_preset

    ; Check for Spacebar = Rest
    cmp al, ' '
    jne comp_chk_notes
    mov ax, N_REST
    mov si, str_note_rest
    call Composer_AddNote
    jmp composer_input_loop

comp_chk_notes:
    ; Convert letter to uppercase
    call Keyboard_ToUpper

    ; White keys: A, S, D, F, G, H, J, K
    cmp al, 'A'
    jne ck_w
    mov ax, N_C5
    mov si, str_note_c5
    call Composer_AddNote
    jmp composer_input_loop

ck_w:
    cmp al, 'W'
    jne ck_s
    mov ax, N_CS5
    mov si, str_note_cs5
    call Composer_AddNote
    jmp composer_input_loop

ck_s:
    cmp al, 'S'
    jne ck_e
    mov ax, N_D5
    mov si, str_note_d5
    call Composer_AddNote
    jmp composer_input_loop

ck_e:
    cmp al, 'E'
    jne ck_d
    mov ax, N_DS5
    mov si, str_note_ds5
    call Composer_AddNote
    jmp composer_input_loop

ck_d:
    cmp al, 'D'
    jne ck_f
    mov ax, N_E5
    mov si, str_note_e5
    call Composer_AddNote
    jmp composer_input_loop

ck_f:
    cmp al, 'F'
    jne ck_t
    mov ax, N_F5
    mov si, str_note_f5
    call Composer_AddNote
    jmp composer_input_loop

ck_t:
    cmp al, 'T'
    jne ck_g
    mov ax, N_FS5
    mov si, str_note_fs5
    call Composer_AddNote
    jmp composer_input_loop

ck_g:
    cmp al, 'G'
    jne ck_y
    mov ax, N_G5
    mov si, str_note_g5
    call Composer_AddNote
    jmp composer_input_loop

ck_y:
    cmp al, 'Y'
    jne ck_h
    mov ax, N_GS5
    mov si, str_note_gs5
    call Composer_AddNote
    jmp composer_input_loop

ck_h:
    cmp al, 'H'
    jne ck_u
    mov ax, N_A5
    mov si, str_note_a5
    call Composer_AddNote
    jmp composer_input_loop

ck_u:
    cmp al, 'U'
    jne ck_j
    mov ax, N_AS5
    mov si, str_note_as5
    call Composer_AddNote
    jmp composer_input_loop

ck_j:
    cmp al, 'J'
    jne ck_k
    mov ax, N_B5
    mov si, str_note_b5
    call Composer_AddNote
    jmp composer_input_loop

ck_k:
    cmp al, 'K'
    jne composer_input_loop
    mov ax, N_C6
    mov si, str_note_c6
    call Composer_AddNote
    jmp composer_input_loop

comp_do_play:
    call Composer_PlayTrack
    jmp composer_input_loop

comp_do_clear:
    mov word [custom_song_count], 0
    mov word [Song_CustomUser], SONG_END
    mov word [Song_CustomUser + 2], 0
    call Composer_DrawTrackTape
    jmp composer_input_loop

comp_do_undo:
    cmp word [custom_song_count], 0
    jbe composer_input_loop
    dec word [custom_song_count]
    ; Place SONG_END at new end
    mov bx, [custom_song_count]
    shl bx, 2                   ; 4 bytes per note (dw freq, dw dur)
    mov word [Song_CustomUser + bx], SONG_END
    mov word [Song_CustomUser + bx + 2], 0
    call Composer_DrawTrackTape
    jmp composer_input_loop

comp_do_preset:
    call Composer_LoadPreset
    call Composer_DrawTrackTape
    jmp composer_input_loop

composer_exit:
    call Speaker_ToneOff
    call Utils_ShowCursor
    pop di
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Composer_Run endp

; ------------------------------------------------------------------------------
; Composer_AddNote
; Inputs: AX = Frequency (Hz), SI = Note name string pointer
; ------------------------------------------------------------------------------
Composer_AddNote proc
    push bx
    push cx
    push dx
    push si

    ; Check buffer limit (max 60 notes)
    cmp word [custom_song_count], 60
    jae comp_an_skip

    ; 1. Auditory preview - play note immediately
    mov bx, ax
    mov cx, [custom_note_dur]
    test bx, bx
    jz comp_an_silent
    mov ax, bx
    call Speaker_PlayToneMs
    jmp comp_an_store

comp_an_silent:
    mov cx, 150
    call Utils_DelayMs

comp_an_store:
    ; 2. Store in Song_CustomUser array
    mov bx, [custom_song_count]
    shl bx, 2                   ; 4 bytes per note
    ; Store Frequency
    pop si
    push si
    ; We need frequency back from caller, but let's resolve by name or keep AX
    ; Let's retrieve frequency from BX
    mov word [Song_CustomUser + bx], ax
    ; Store Duration
    mov dx, [custom_note_dur]
    mov word [Song_CustomUser + bx + 2], dx
    ; Advance count
    inc word [custom_song_count]
    ; Terminate with SONG_END
    add bx, 4
    mov word [Song_CustomUser + bx], SONG_END
    mov word [Song_CustomUser + bx + 2], 0

    ; 3. Update Visual Track Tape
    call Composer_DrawTrackTape

comp_an_skip:
    pop si
    pop dx
    pop cx
    pop bx
    ret
Composer_AddNote endp

; ------------------------------------------------------------------------------
; Composer_DrawTrackTape
; Renders the notes in Song_CustomUser on screen (Row 7 and 8)
; ------------------------------------------------------------------------------
Composer_DrawTrackTape proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; 1. Clear Track Tape Interior (Rows 7..8, Cols 10..69)
    mov dh, 7
    mov dl, 10
    mov ch, 8
    mov cl, 69
    mov al, ' '
    mov bl, 07h
    call Graphics_FillArea

    ; 2. Print Status Info on Row 7
    mov dh, 7
    mov dl, 10
    mov bl, THEME_ACCENT
    mov si, str_track_lbl
    call Utils_PrintStringAt

    ; Print Note Count
    mov ax, [custom_song_count]
    mov dl, 23
    mov dh, 7
    call Composer_PrintNumber

    mov dl, 26
    mov bl, THEME_MUTED
    mov si, str_track_max
    call Utils_PrintStringAt

    ; Print Duration
    mov dl, 38
    mov bl, THEME_ACCENT
    mov si, str_dur_lbl
    call Utils_PrintStringAt

    mov ax, [custom_note_dur]
    mov dl, 47
    mov dh, 7
    call Composer_PrintNumber

    mov dl, 52
    mov bl, THEME_MUTED
    mov si, str_ms_lbl
    call Utils_PrintStringAt

    ; 3. Print Notes Sequence on Row 8
    mov dh, 8
    mov dl, 10
    mov bl, THEME_TITLE
    mov si, str_tape_lbl
    call Utils_PrintStringAt

    mov cx, [custom_song_count]
    test cx, cx
    jnz comp_has_notes
    mov dh, 8
    mov dl, 18
    mov bl, THEME_MUTED
    mov si, str_empty_track
    call Utils_PrintStringAt
    jmp comp_dtt_done

comp_has_notes:
    ; If count > 10, display the last 10 notes
    mov si, 0
    cmp cx, 10
    jbe comp_notes_start
    mov si, cx
    sub si, 10                  ; SI = start note index

comp_notes_start:
    mov dl, 18                  ; start column for notes
comp_disp_loop:
    cmp si, [custom_song_count]
    jae comp_dtt_done

    mov bx, si
    shl bx, 2                   ; 4 bytes per note
    mov ax, [Song_CustomUser + bx] ; Frequency

    ; Find note name for frequency
    push si
    push dx
    push cx
    call Composer_GetNoteName   ; returns SI -> 3-letter name, BL = color
    pop cx
    pop dx
    call Utils_PrintStringAt
    pop si

    add dl, 5                   ; spacing between notes
    inc si
    jmp comp_disp_loop

comp_dtt_done:
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Composer_DrawTrackTape endp

; ------------------------------------------------------------------------------
; Composer_PlayTrack
; Plays all recorded notes in Song_CustomUser
; ------------------------------------------------------------------------------
Composer_PlayTrack proc
    push ax
    push bx
    push cx
    push dx
    push si

    cmp word [custom_song_count], 0
    je comp_pt_empty

    ; Print "PLAYING CUSTOM TRACK..." badge
    mov dh, 7
    mov dl, 58
    mov bl, 4Fh                 ; White on Red
    mov si, str_playing_badge
    call Utils_PrintStringAt

    mov si, Song_CustomUser

comp_pt_loop:
    lodsw                       ; AX = Frequency
    cmp ax, SONG_END
    je comp_pt_end

    mov bx, ax                  ; BX = Frequency
    lodsw                       ; AX = Duration
    mov cx, ax                  ; CX = Duration

    test bx, bx
    jz comp_pt_rest

    ; Play tone
    mov ax, bx
    call Speaker_PlayToneMs
    jmp comp_pt_next

comp_pt_rest:
    call Utils_DelayMs

comp_pt_next:
    ; Check if user pressed ESC to stop playback
    call Keyboard_CheckKey
    test al, al
    jz comp_pt_loop
    call Keyboard_WaitKey
    cmp al, KEY_ESC
    je comp_pt_end
    jmp comp_pt_loop

comp_pt_end:
    call Speaker_ToneOff

    ; Clear "PLAYING" badge
    mov dh, 7
    mov dl, 58
    mov cx, 12
    mov al, ' '
    mov bl, 07h
    call Graphics_DrawHLine
    call Composer_DrawTrackTape

comp_pt_empty:
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Composer_PlayTrack endp

; ------------------------------------------------------------------------------
; Composer_LoadPreset
; Resets to 8-note starter melody
; ------------------------------------------------------------------------------
Composer_LoadPreset proc
    push ax
    push bx

    mov word [custom_song_count], 8
    mov word [custom_note_dur], 300

    mov word [Song_CustomUser + 0],  N_C5
    mov word [Song_CustomUser + 2],  300
    mov word [Song_CustomUser + 4],  N_E5
    mov word [Song_CustomUser + 6],  300
    mov word [Song_CustomUser + 8],  N_G5
    mov word [Song_CustomUser + 10], 300
    mov word [Song_CustomUser + 12], N_C6
    mov word [Song_CustomUser + 14], 600

    mov word [Song_CustomUser + 16], N_G5
    mov word [Song_CustomUser + 18], 300
    mov word [Song_CustomUser + 20], N_E5
    mov word [Song_CustomUser + 22], 300
    mov word [Song_CustomUser + 24], N_C5
    mov word [Song_CustomUser + 26], 600
    mov word [Song_CustomUser + 28], N_REST
    mov word [Song_CustomUser + 30], 200

    mov word [Song_CustomUser + 32], SONG_END
    mov word [Song_CustomUser + 34], 0

    pop bx
    pop ax
    ret
Composer_LoadPreset endp

; ------------------------------------------------------------------------------
; Composer_GetNoteName
; Input:  AX = Frequency
; Output: SI = Note string, BL = color attribute
; ------------------------------------------------------------------------------
Composer_GetNoteName proc
    cmp ax, N_REST
    jne cgn_c5
    mov si, str_disp_rst
    mov bl, THEME_MUTED
    ret
cgn_c5:
    cmp ax, N_C5
    jne cgn_cs5
    mov si, str_disp_c5
    mov bl, THEME_TEXT
    ret
cgn_cs5:
    cmp ax, N_CS5
    jne cgn_d5
    mov si, str_disp_cs5
    mov bl, THEME_TITLE
    ret
cgn_d5:
    cmp ax, N_D5
    jne cgn_ds5
    mov si, str_disp_d5
    mov bl, THEME_TEXT
    ret
cgn_ds5:
    cmp ax, N_DS5
    jne cgn_e5
    mov si, str_disp_ds5
    mov bl, THEME_TITLE
    ret
cgn_e5:
    cmp ax, N_E5
    jne cgn_f5
    mov si, str_disp_e5
    mov bl, THEME_TEXT
    ret
cgn_f5:
    cmp ax, N_F5
    jne cgn_fs5
    mov si, str_disp_f5
    mov bl, THEME_TEXT
    ret
cgn_fs5:
    cmp ax, N_FS5
    jne cgn_g5
    mov si, str_disp_fs5
    mov bl, THEME_TITLE
    ret
cgn_g5:
    cmp ax, N_G5
    jne cgn_gs5
    mov si, str_disp_g5
    mov bl, THEME_TEXT
    ret
cgn_gs5:
    cmp ax, N_GS5
    jne cgn_a5
    mov si, str_disp_gs5
    mov bl, THEME_TITLE
    ret
cgn_a5:
    cmp ax, N_A5
    jne cgn_as5
    mov si, str_disp_a5
    mov bl, THEME_TEXT
    ret
cgn_as5:
    cmp ax, N_AS5
    jne cgn_b5
    mov si, str_disp_as5
    mov bl, THEME_TITLE
    ret
cgn_b5:
    cmp ax, N_B5
    jne cgn_c6
    mov si, str_disp_b5
    mov bl, THEME_TEXT
    ret
cgn_c6:
    mov si, str_disp_c6
    mov bl, THEME_ACCENT
    ret
Composer_GetNoteName endp

; ------------------------------------------------------------------------------
; Composer_PrintNumber
; Prints 1..4 digit number in AX at DH, DL.
; ------------------------------------------------------------------------------
Composer_PrintNumber proc
    push ax
    push bx
    push cx
    push dx

    mov bx, 10
    xor cx, cx

cpn_div_loop:
    xor dx, dx
    div bx                      ; AX = quotient, DX = remainder
    push dx                     ; Push digit
    inc cx
    test ax, ax
    jnz cpn_div_loop

    ; Now print digits
cpn_pr_loop:
    pop ax
    add al, '0'
    mov bl, THEME_TEXT
    call Utils_PrintChar
    loop cpn_pr_loop

    pop dx
    pop cx
    pop bx
    pop ax
    ret
Composer_PrintNumber endp

; ------------------------------------------------------------------------------
; Strings & UI Labels
; ------------------------------------------------------------------------------
str_comp_title1     db "CRIMSON ORBIT :: MUSIC COMPOSER", 0
str_comp_title2     db "Compose & Record Custom Songs Directly into 8086 RAM", 0

str_comp_track_hdr  db " LIVE COMPOSER TRACK TAPE ", 0
str_track_lbl       db "Notes Recorded: ", 0
str_track_max       db "/ 60", 0
str_dur_lbl         db "Duration: ", 0
str_ms_lbl          db "ms", 0
str_tape_lbl        db "Tape: ", 0
str_empty_track     db "[ Empty Track - Press A..K or SPACE to record notes! ]", 0
str_playing_badge   db " PLAYING... ", 0

str_comp_kb_hdr     db " VIRTUAL KEYBOARD CONTROLS ", 0
str_comp_keys_black db "      [W]       [E]             [T]       [Y]       [U]", 0
str_comp_names_black db "     (C#5)     (D#5)           (F#5)     (G#5)     (A#5)", 0
str_comp_keys_white db "   [A]     [S]     [D]     [F]     [G]     [H]     [J]     [K]", 0
str_comp_names_white db "  (C5)    (D5)    (E5)    (F5)    (G5)    (A5)    (B5)    (C6)  [SPACE]=Rest", 0

str_comp_cmd1       db "[P] Play Custom Track   |  [C] Clear Track  |  [B / Bksp] Undo Note", 0
str_comp_cmd2       db "[1] Eighth (150ms)  [2] Quarter (300ms)  [3] Half (600ms)  [4] Whole (1s)", 0
str_comp_cmd3       db "[L] Load Preset Fanfare |  [ESC] Return to Main Menu (Track Saved)", 0

str_comp_foot       db "[A..K] Play Note  |  [P] Play All  |  [C] Clear  |  [ESC] Save & Exit", 0

str_note_c5         db "C5", 0
str_note_cs5        db "C#5", 0
str_note_d5         db "D5", 0
str_note_ds5        db "D#5", 0
str_note_e5         db "E5", 0
str_note_f5         db "F5", 0
str_note_fs5        db "F#5", 0
str_note_g5         db "G5", 0
str_note_gs5        db "G#5", 0
str_note_a5         db "A5", 0
str_note_as5        db "A#5", 0
str_note_b5         db "B5", 0
str_note_c6         db "C6", 0
str_note_rest       db "REST", 0

str_disp_c5         db "[C5] ", 0
str_disp_cs5        db "[C#] ", 0
str_disp_d5         db "[D5] ", 0
str_disp_ds5        db "[D#] ", 0
str_disp_e5         db "[E5] ", 0
str_disp_f5         db "[F5] ", 0
str_disp_fs5        db "[F#] ", 0
str_disp_g5         db "[G5] ", 0
str_disp_gs5        db "[G#] ", 0
str_disp_a5         db "[A5] ", 0
str_disp_as5        db "[A#] ", 0
str_disp_b5         db "[B5] ", 0
str_disp_c6         db "[C6] ", 0
str_disp_rst        db "[--] ", 0
