; ==============================================================================
; CRIMSON ORBIT – MUSICAL BAND
; Module: Main Menu System, Help & About (menu.asm)
; Target Assembler: emu8086
; Central hub: routes to Piano, Guitar, Drums, Demo Songs, Help, About, Exit.
; ==============================================================================

MainMenu_Run proc
    push ax
    push bx
    push cx
    push dx
    push si

main_menu_redraw:
    ; 1. Clear Screen to Black
    mov bl, 07h
    call Utils_ClearScreen
    call Utils_HideCursor

    ; 2. Outer Decorative Frame Box (Rows 2..21, Cols 14..65)
    mov dh, 2
    mov dl, 14
    mov ch, 21
    mov cl, 65
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    ; 3. Crimson Orbit Banner
    mov dh, 3
    mov dl, 20
    mov bl, THEME_TITLE
    mov si, str_menu_banner1
    call Utils_PrintStringAt

    mov dh, 4
    mov dl, 24
    mov bl, THEME_TITLE
    mov si, str_menu_banner2
    call Utils_PrintStringAt

    mov dh, 5
    mov dl, 25
    mov bl, THEME_ACCENT
    mov si, str_menu_banner3
    call Utils_PrintStringAt

    mov dh, 6
    mov dl, 20
    mov bl, THEME_TITLE
    mov si, str_menu_banner1
    call Utils_PrintStringAt

    ; 4. Menu Items
    mov bl, THEME_TEXT
    mov dh, 8
    mov dl, 26
    mov si, str_menu_item1
    call Utils_PrintStringAt

    mov dh, 9
    mov dl, 26
    mov si, str_menu_item2
    call Utils_PrintStringAt

    mov dh, 10
    mov dl, 26
    mov si, str_menu_item3
    call Utils_PrintStringAt

    mov dh, 11
    mov dl, 26
    mov si, str_menu_item4
    call Utils_PrintStringAt

    mov dh, 12
    mov dl, 26
    mov bl, THEME_ACCENT
    mov si, str_menu_item5
    call Utils_PrintStringAt

    mov bl, THEME_TEXT
    mov dh, 13
    mov dl, 26
    mov si, str_menu_item6
    call Utils_PrintStringAt

    mov dh, 14
    mov dl, 26
    mov si, str_menu_item7
    call Utils_PrintStringAt

    mov bl, THEME_MUTED
    mov dh, 15
    mov dl, 26
    mov si, str_menu_item8
    call Utils_PrintStringAt

    ; Separator
    mov dh, 16
    mov dl, 15
    mov cx, 50
    mov al, CP437_S_H
    mov bl, THEME_MUTED
    call Graphics_DrawHLine

    ; Prompt
    mov dh, 18
    mov dl, 24
    mov bl, THEME_TITLE
    mov si, str_menu_prompt
    call Utils_PrintStringAt

    ; Bottom Instruction Footer
    mov si, str_menu_foot
    call Graphics_DrawFooter

menu_input_loop:
    call Keyboard_WaitKey

    cmp al, KEY_ESC
    je menu_do_exit

    cmp al, '1'
    jne m_chk_2
    call Piano_Run
    jmp main_menu_redraw

m_chk_2:
    cmp al, '2'
    jne m_chk_3
    call Guitar_Run
    jmp main_menu_redraw

m_chk_3:
    cmp al, '3'
    jne m_chk_4
    call Drums_Run
    jmp main_menu_redraw

m_chk_4:
    cmp al, '4'
    jne m_chk_5
    call Demo_Run
    jmp main_menu_redraw

m_chk_5:
    cmp al, '5'
    jne m_chk_6
    call Composer_Run
    jmp main_menu_redraw

m_chk_6:
    cmp al, '6'
    jne m_chk_7
    call Menu_ShowHelp
    jmp main_menu_redraw

m_chk_7:
    cmp al, '7'
    jne m_chk_8
    call Menu_ShowAbout
    jmp main_menu_redraw

m_chk_8:
    cmp al, '8'
    jne menu_input_loop

menu_do_exit:
    call Menu_ShowExit
    ; If user pressed ESC in exit dialog, redraw menu
    jmp main_menu_redraw

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
MainMenu_Run endp

; ------------------------------------------------------------------------------
; Menu_ShowHelp (Phase 11)
; Full-screen guide explaining controls, musical notation, and navigation.
; ------------------------------------------------------------------------------
Menu_ShowHelp proc
    push ax
    push bx
    push cx
    push dx
    push si

    mov bl, 07h
    call Utils_ClearScreen
    call Utils_HideCursor

    mov si, str_help_hdr
    call Graphics_DrawHeader

    ; Main Help Box (Rows 3..20, Cols 4..75)
    mov dh, 3
    mov dl, 4
    mov ch, 20
    mov cl, 75
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    mov bl, THEME_ACCENT
    mov dh, 4
    mov dl, 6
    mov si, str_h_sec1
    call Utils_PrintStringAt

    mov bl, THEME_TEXT
    mov dh, 5
    mov dl, 8
    mov si, str_h_piano
    call Utils_PrintStringAt

    mov bl, THEME_ACCENT
    mov dh, 7
    mov dl, 6
    mov si, str_h_sec2
    call Utils_PrintStringAt

    mov bl, THEME_TEXT
    mov dh, 8
    mov dl, 8
    mov si, str_h_guitar
    call Utils_PrintStringAt

    mov bl, THEME_ACCENT
    mov dh, 10
    mov dl, 6
    mov si, str_h_sec3
    call Utils_PrintStringAt

    mov bl, THEME_TEXT
    mov dh, 11
    mov dl, 8
    mov si, str_h_drums
    call Utils_PrintStringAt

    mov bl, THEME_ACCENT
    mov dh, 13
    mov dl, 6
    mov si, str_h_sec4
    call Utils_PrintStringAt

    mov bl, THEME_TEXT
    mov dh, 14
    mov dl, 8
    mov si, str_h_demo
    call Utils_PrintStringAt

    mov bl, THEME_ACCENT
    mov dh, 16
    mov dl, 6
    mov si, str_h_sec5
    call Utils_PrintStringAt

    mov bl, THEME_TEXT
    mov dh, 17
    mov dl, 8
    mov si, str_h_nav
    call Utils_PrintStringAt

    mov bl, THEME_TITLE
    mov dh, 19
    mov dl, 22
    mov si, str_press_any_key
    call Utils_PrintStringAt

    ; Footer
    mov si, str_help_foot
    call Graphics_DrawFooter

    call Keyboard_WaitAnyKey

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Menu_ShowHelp endp

; ------------------------------------------------------------------------------
; Menu_ShowAbout (Phase 11)
; Displays bare-metal architecture details, hardware specs, and project credits.
; ------------------------------------------------------------------------------
Menu_ShowAbout proc
    push ax
    push bx
    push cx
    push dx
    push si

    mov bl, 07h
    call Utils_ClearScreen
    call Utils_HideCursor

    mov si, str_about_hdr
    call Graphics_DrawHeader

    ; Box (Rows 3..20, Cols 8..71)
    mov dh, 3
    mov dl, 8
    mov ch, 20
    mov cl, 71
    mov bl, THEME_BORDER
    call Graphics_DrawBoxDouble

    mov bl, THEME_TITLE
    mov dh, 5
    mov dl, 20
    mov si, str_ab_title
    call Utils_PrintStringAt

    mov bl, THEME_ACCENT
    mov dh, 6
    mov dl, 19
    mov si, str_ab_sub
    call Utils_PrintStringAt

    mov dh, 7
    mov dl, 10
    mov cx, 60
    mov al, CP437_S_H
    mov bl, THEME_MUTED
    call Graphics_DrawHLine

    mov bl, THEME_TEXT
    mov dh, 9
    mov dl, 12
    mov si, str_ab_line1
    call Utils_PrintStringAt

    mov dh, 10
    mov dl, 12
    mov si, str_ab_line2
    call Utils_PrintStringAt

    mov dh, 11
    mov dl, 12
    mov si, str_ab_line3
    call Utils_PrintStringAt

    mov dh, 12
    mov dl, 12
    mov si, str_ab_line4
    call Utils_PrintStringAt

    mov dh, 13
    mov dl, 12
    mov si, str_ab_line5
    call Utils_PrintStringAt

    mov dh, 14
    mov dl, 12
    mov si, str_ab_line6
    call Utils_PrintStringAt

    mov dh, 15
    mov dl, 12
    mov si, str_ab_line7
    call Utils_PrintStringAt

    mov bl, THEME_TITLE
    mov dh, 18
    mov dl, 22
    mov si, str_press_any_key
    call Utils_PrintStringAt

    mov si, str_about_foot
    call Graphics_DrawFooter

    call Keyboard_WaitAnyKey

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Menu_ShowAbout endp

; ------------------------------------------------------------------------------
; Menu_ShowExit
; Clean shutdown screen with reboot option.
; ------------------------------------------------------------------------------
Menu_ShowExit proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; Modal Box at Rows 8..17, Cols 18..62
    mov dh, 8
    mov dl, 18
    mov ch, 17
    mov cl, 62
    mov bl, THEME_TITLE
    call Graphics_DrawBoxDouble

    ; Clear Modal Interior
    mov dh, 9
    mov dl, 19
    mov ch, 16
    mov cl, 61
    mov al, ' '
    mov bl, 07h
    call Graphics_FillArea

    mov dh, 10
    mov dl, 22
    mov bl, THEME_TITLE
    mov si, str_exit_title
    call Utils_PrintStringAt

    mov dh, 12
    mov dl, 21
    mov bl, THEME_TEXT
    mov si, str_exit_p1
    call Utils_PrintStringAt

    mov dh, 14
    mov dl, 21
    mov bl, THEME_ACCENT
    mov si, str_exit_p2
    call Utils_PrintStringAt

    mov dh, 15
    mov dl, 21
    mov bl, THEME_MUTED
    mov si, str_exit_p3
    call Utils_PrintStringAt

exit_wait_key:
    call Keyboard_WaitKey

    cmp al, KEY_ENTER
    je exit_reboot

    cmp al, KEY_ESC
    je exit_return

    jmp exit_wait_key

exit_reboot:
    ; Warm reboot via BIOS INT 19h
    call Speaker_ToneOff
    mov bl, 07h
    call Utils_ClearScreen
    call Utils_ShowCursor
    int 19h

exit_return:
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Menu_ShowExit endp

; ------------------------------------------------------------------------------
; Menu Data & Strings
; ------------------------------------------------------------------------------
str_menu_banner1    db "========================================", 0
str_menu_banner2    db "      CRIMSON ORBIT", 0
str_menu_banner3    db "       MUSICAL BAND", 0

str_menu_item1      db "1. Concert Grand Piano", 0
str_menu_item2      db "2. 6-String Lead Guitar", 0
str_menu_item3      db "3. 5-Piece Drum Kit", 0
str_menu_item4      db "4. Automated Song Repertoire", 0
str_menu_item5      db "5. Custom Music Composer & Recorder", 0
str_menu_item6      db "6. System Help & Controls", 0
str_menu_item7      db "7. About Crimson Orbit", 0
str_menu_item8      db "8. Exit Workstation", 0

str_menu_prompt     db "Select Module [1..8]: ", 0
str_menu_foot       db "[1..8] Select Module  |  [ESC] Exit & Reboot Options", 0

; Help Strings
str_help_hdr        db "SYSTEM HELP & CONTROLS", 0
str_h_sec1          db "1. PIANO CONTROLS:", 0
str_h_piano         db "Keys: [Q..I] White, [2,3, 5,6,7] Black | [TAB] Octave (4/5/6) | [SPACE] Sustain", 0
str_h_sec2          db "2. GUITAR CONTROLS:", 0
str_h_guitar        db "Strings: [Q..Y] Pluck Strings | [S] Strum Full Chord | [TAB] Acoustic/Lead", 0
str_h_sec3          db "3. DRUM KIT CONTROLS:", 0
str_h_drums         db "Pads: [Q] Kick  [W] Snare  [E] Closed HH  [Y] Open HH  [R] Tom  [T] Crash  [U] Ride", 0
str_h_sec4          db "4. DEMO SONGS:", 0
str_h_demo          db "6 Concert scores in High-Hz pitch. Select song [1..6], then choose instrument.", 0
str_h_sec5          db "5. NAVIGATION:", 0
str_h_nav           db "Press [ESC] at any time inside any module to return immediately to Main Menu.", 0
str_press_any_key   db ">>> Press Any Key to Return to Menu <<<", 0
str_help_foot       db "[Any Key] Return to Main Menu", 0

; About Strings
str_about_hdr       db "SYSTEM ARCHITECTURE & ABOUT", 0
str_ab_title        db "CRIMSON ORBIT :: MUSICAL BAND", 0
str_ab_sub          db "Bare-Metal 8086 Real Mode Operating System", 0
str_ab_line1        db "Operating System : Bare-Metal (No DOS, Pure BIOS/Hardware)", 0
str_ab_line2        db "Processor Target : Intel 8086 Real Mode (16-bit)", 0
str_ab_line3        db "Assembler Target : emu8086 / Strict Syntax Compatibility", 0
str_ab_line4        db "Virtual Machine  : VMware Workstation 1.44MB Floppy Bootable", 0
str_ab_line5        db "Sound Engine     : Intel 8254 PIT (Ports 42h/43h) & 8255 PPI (Port 61h)", 0
str_ab_line6        db "Video Graphics   : BIOS Text Mode 03h (80x25 16-Color CP437)", 0
str_ab_line7        db "Boot Mechanism   : Custom MBR Bootloader (Loads Kernel via INT 13h)", 0
str_about_foot      db "[Any Key] Return to Main Menu", 0

; Exit Strings
str_exit_title      db "CRIMSON ORBIT SHUTDOWN", 0
str_exit_p1         db "Thank you for performing with us!", 0
str_exit_p2         db "[ENTER] Warm Reboot Virtual Machine", 0
str_exit_p3         db "[ESC]   Cancel & Return to Menu", 0
