#make_bin#
#LOAD_SEGMENT=1000h#
#LOAD_OFFSET=0000h#
#CS=1000h#
#IP=0000h#
#DS=1000h#
#ES=1000h#
#SS=1000h#
#SP=FFFEh#

; ==============================================================================
; CRIMSON ORBIT – MUSICAL BAND
; Main Kernel Controller (kernel.asm)
; Target Assembler: emu8086
; Memory Target: Loaded at 1000h:0000h by bootloader
; Coordinates environment, welcome splash screen, intro jingle, and modules.
; ==============================================================================

org 0000h
jmp kernel_entry

; ==============================================================================
; Modular Includes (Strict emu8086 Architecture)
; ==============================================================================
include "utils.asm"
include "graphics.asm"
include "keyboard.asm"
include "speaker.asm"
include "piano.asm"
include "guitar.asm"
include "drums.asm"
include "songs.asm"
include "demo.asm"
include "menu.asm"

kernel_entry:
    ; --------------------------------------------------------------------------
    ; 1. Initialize Kernel Segment Registers & Stack
    ; --------------------------------------------------------------------------
    cli
    mov ax, 1000h
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0FFFEh              ; Stack top at 1000:FFFEh
    sti

    ; --------------------------------------------------------------------------
    ; 2. Initialize 80x25 16-Color Text Mode
    ; --------------------------------------------------------------------------
    mov ax, 0003h
    int 10h

    ; --------------------------------------------------------------------------
    ; 3. Render Crimson Orbit Welcome Splash Screen
    ; --------------------------------------------------------------------------
    call Kernel_ShowSplash

    ; --------------------------------------------------------------------------
    ; 4. Play Welcome Soundstage Arpeggio Fanfare
    ; --------------------------------------------------------------------------
    call Kernel_PlayIntroJingle

    ; --------------------------------------------------------------------------
    ; 5. Wait for [ENTER] Keystroke
    ; --------------------------------------------------------------------------
wait_enter_key:
    call Keyboard_WaitKey
    cmp al, KEY_ENTER
    jne wait_enter_key

    ; --------------------------------------------------------------------------
    ; 6. Enter Main Menu Loop
    ; --------------------------------------------------------------------------
kernel_main_loop:
    call MainMenu_Run
    jmp kernel_main_loop

; ==============================================================================
; Kernel Procedures
; ==============================================================================

; ------------------------------------------------------------------------------
; Kernel_ShowSplash
; Renders the grand opening welcome screen.
; ------------------------------------------------------------------------------
Kernel_ShowSplash proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; Clear screen with deep black
    mov bl, 07h
    call Utils_ClearScreen
    call Utils_HideCursor

    ; Outer Frame (Rows 1..22, Cols 4..75)
    mov dh, 1
    mov dl, 4
    mov ch, 22
    mov cl, 75
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    ; Inner Title Box (Rows 3..7, Cols 10..69)
    mov dh, 3
    mov dl, 10
    mov ch, 7
    mov cl, 69
    mov bl, THEME_ACCENT
    call Graphics_DrawBoxSingle

    mov dh, 4
    mov dl, 20
    mov bl, THEME_TITLE
    mov si, str_splash_title1
    call Utils_PrintStringAt

    mov dh, 5
    mov dl, 22
    mov bl, THEME_ACCENT
    mov si, str_splash_title2
    call Utils_PrintStringAt

    mov dh, 6
    mov dl, 16
    mov bl, THEME_TEXT
    mov si, str_splash_tagline
    call Utils_PrintStringAt

    ; Decorative Musical Staff & Orbit Art (Rows 9..14)
    mov dh, 9
    mov dl, 12
    mov bl, THEME_MUTED
    mov si, str_art_line1
    call Utils_PrintStringAt

    mov dh, 10
    mov dl, 12
    mov bl, THEME_ACCENT
    mov si, str_art_line2
    call Utils_PrintStringAt

    mov dh, 11
    mov dl, 12
    mov bl, THEME_TITLE
    mov si, str_art_line3
    call Utils_PrintStringAt

    mov dh, 12
    mov dl, 12
    mov bl, THEME_ACCENT
    mov si, str_art_line4
    call Utils_PrintStringAt

    mov dh, 13
    mov dl, 12
    mov bl, THEME_MUTED
    mov si, str_art_line5
    call Utils_PrintStringAt

    ; Features Line
    mov dh, 16
    mov dl, 14
    mov bl, THEME_TEXT
    mov si, str_splash_features
    call Utils_PrintStringAt

    ; Prompt Box
    mov dh, 18
    mov dl, 18
    mov ch, 20
    mov cl, 61
    mov bl, THEME_TITLE
    call Graphics_DrawBoxSingle

    mov dh, 19
    mov dl, 20
    mov bl, THEME_ACCENT
    mov si, str_splash_prompt
    call Utils_PrintStringAt

    ; Bottom copyright line
    mov dh, 23
    mov dl, 18
    mov bl, THEME_MUTED
    mov si, str_splash_footer
    call Utils_PrintStringAt

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Kernel_ShowSplash endp

; ------------------------------------------------------------------------------
; Kernel_PlayIntroJingle
; Plays an ascending arpeggio chord jingle in sparkling concert pitch:
; C5 (523) -> E5 (659) -> G5 (784) -> C6 (1046) -> E6 (1318) -> G6 (1568)
; Concludes with a metallic crash cymbal splash on the final cadence!
; ------------------------------------------------------------------------------
Kernel_PlayIntroJingle proc
    push ax
    push cx

    mov ax, 523                 ; C5 (Concert High)
    mov cx, 80
    call Speaker_PlayToneMs

    mov ax, 659                 ; E5
    mov cx, 80
    call Speaker_PlayToneMs

    mov ax, 784                 ; G5
    mov cx, 80
    call Speaker_PlayToneMs

    mov ax, 1046                ; C6
    mov cx, 100
    call Speaker_PlayToneMs

    mov ax, 1318                ; E6
    mov cx, 100
    call Speaker_PlayToneMs

    mov ax, 1568                ; G6 (Concert Brilliant Peak)
    mov cx, 280
    call Speaker_PlayToneMs

    ; Metallic Crash Cymbal burst on final resolution
    call Sound_Crash

    call Speaker_ToneOff

    pop cx
    pop ax
    ret
Kernel_PlayIntroJingle endp

; ==============================================================================
; Kernel Splash Strings
; ==============================================================================
str_splash_title1   db "* * *   C R I M S O N   O R B I T   * * *", 0
str_splash_title2   db "==  M U S I C A L   B A N D  ==", 0
str_splash_tagline  db "High-Fidelity Real-Mode Acoustic Physics Audio Workstation", 0

str_art_line1       db "  ---|-|-------|-------|---------|-------|-------|---|---  ", 0
str_art_line2       db "     | |       (o)     |         |      (o)      | |       ", 0
str_art_line3       db "  <<<[ * ]===-- | -----|---(*)---|------- | ----[ * ]>>>   ", 0
str_art_line4       db "       |        |     (o)        |        |      |         ", 0
str_art_line5       db "  -----|--------|------|---------|--------|------|-------  ", 0

str_splash_features db "Concert Piano :: Lead Guitar :: Studio Drums :: 6 Demo Songs", 0
str_splash_prompt   db ">>> Press [ENTER] to Enter the Soundstage <<<", 0
str_splash_footer   db "Target: emu8086 | Bootable Floppy Image | VMware Workstation", 0

