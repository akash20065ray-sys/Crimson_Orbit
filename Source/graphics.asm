; ==============================================================================
; CRIMSON ORBIT – MUSICAL BAND
; Module: Graphics & Text-Mode UI Engine (graphics.asm)
; Target Assembler: emu8086
; Provides reusable CP437 box drawing, borders, headers, and Crimson styling.
; ==============================================================================

; ------------------------------------------------------------------------------
; Color Attribute Definitions (Foreground on Black)
; ------------------------------------------------------------------------------
COLOR_BLACK         equ 00h
COLOR_BLUE          equ 01h
COLOR_GREEN         equ 02h
COLOR_CYAN          equ 03h
COLOR_RED           equ 04h
COLOR_MAGENTA       equ 05h
COLOR_BROWN         equ 06h
COLOR_LIGHTGRAY     equ 07h
COLOR_DARKGRAY      equ 08h
COLOR_LIGHTBLUE     equ 09h
COLOR_LIGHTGREEN    equ 0Ah
COLOR_LIGHTCYAN     equ 0Bh
COLOR_CRIMSON       equ 0Ch     ; Bright / Light Red
COLOR_LIGHTMAGENTA  equ 0Dh
COLOR_GOLD          equ 0Eh     ; Yellow / Amber
COLOR_WHITE         equ 0Fh     ; Bright White

; Standard Theme Attributes
THEME_TITLE         equ 0Ch     ; Crimson
THEME_ACCENT        equ 0Eh     ; Gold
THEME_BORDER        equ 0Ch     ; Crimson border
THEME_TEXT          equ 0Fh     ; Bright white text
THEME_MUTED         equ 08h     ; Dark gray for hints
THEME_BG_BAR        equ 4Fh     ; Bright white on red background

; ------------------------------------------------------------------------------
; CP437 Box-Drawing Characters
; ------------------------------------------------------------------------------
CP437_D_TL          equ 0C9h    ; ╔
CP437_D_TR          equ 0BBh    ; ╗
CP437_D_BL          equ 0C8h    ; ╚
CP437_D_BR          equ 0BCh    ; ╝
CP437_D_H           equ 0CDh    ; ═
CP437_D_V           equ 0BAh    ; ║

CP437_S_TL          equ 0DAh    ; ┌
CP437_S_TR          equ 0BFh    ; ┐
CP437_S_BL          equ 0C0h    ; └
CP437_S_BR          equ 0D9h    ; ┘
CP437_S_H           equ 0C4h    ; ─
CP437_S_V           equ 0B3h    ; │

CP437_BLOCK_FULL    equ 0DBh    ; █
CP437_BLOCK_DARK    equ 0B2h    ; ▓
CP437_BLOCK_MED     equ 0B1h    ; ▒
CP437_BLOCK_LIGHT   equ 0B0h    ; ░

; ------------------------------------------------------------------------------
; Graphics_DrawChar
; Helper: Draws a single character AL at (DH, DL) with attribute BL.
; ------------------------------------------------------------------------------
Graphics_DrawChar proc
    push ax
    push bx
    push cx
    call Utils_SetCursor
    mov ah, 09h
    xor bh, bh
    mov cx, 1
    int 10h
    pop cx
    pop bx
    pop ax
    ret
Graphics_DrawChar endp

; ------------------------------------------------------------------------------
; Graphics_DrawHLine
; Draws a horizontal line of character AL, length CX, starting at (DH, DL).
; Input:  DH = row, DL = col, CX = length, AL = character, BL = attribute
; ------------------------------------------------------------------------------
Graphics_DrawHLine proc
    push cx
    push dx
g_dhl_loop:
    test cx, cx
    jz g_dhl_done
    call Graphics_DrawChar
    inc dl
    dec cx
    jmp g_dhl_loop
g_dhl_done:
    pop dx
    pop cx
    ret
Graphics_DrawHLine endp

; ------------------------------------------------------------------------------
; Graphics_DrawVLine
; Draws a vertical line of character AL, height CX, starting at (DH, DL).
; Input:  DH = row, DL = col, CX = height, AL = character, BL = attribute
; ------------------------------------------------------------------------------
Graphics_DrawVLine proc
    push cx
    push dx
g_dvl_loop:
    test cx, cx
    jz g_dvl_done
    call Graphics_DrawChar
    inc dh
    dec cx
    jmp g_dvl_loop
g_dvl_done:
    pop dx
    pop cx
    ret
Graphics_DrawVLine endp

; ------------------------------------------------------------------------------
; Graphics_DrawBoxDouble
; Draws a double-lined box from (DH=r1, DL=c1) to (CH=r2, CL=c2) with attribute BL.
; Input:  DH = top row, DL = left col
;         CH = bottom row, CL = right col
;         BL = attribute
; ------------------------------------------------------------------------------
Graphics_DrawBoxDouble proc
    push ax
    push bx
    push cx
    push dx

    mov [box_r1], dh
    mov [box_c1], dl
    mov [box_r2], ch
    mov [box_c2], cl
    mov [box_attr], bl

    ; Top Left corner ╔
    mov dh, [box_r1]
    mov dl, [box_c1]
    mov al, CP437_D_TL
    mov bl, [box_attr]
    call Graphics_DrawChar

    ; Top Horizontal line ═
    mov dh, [box_r1]
    mov dl, [box_c1]
    inc dl
    mov al, [box_c2]
    sub al, [box_c1]
    dec al
    mov cl, al
    xor ch, ch
    mov al, CP437_D_H
    mov bl, [box_attr]
    call Graphics_DrawHLine

    ; Top Right corner ╗
    mov dh, [box_r1]
    mov dl, [box_c2]
    mov al, CP437_D_TR
    mov bl, [box_attr]
    call Graphics_DrawChar

    ; Left Vertical line ║
    mov dh, [box_r1]
    inc dh
    mov dl, [box_c1]
    mov al, [box_r2]
    sub al, [box_r1]
    dec al
    mov cl, al
    xor ch, ch
    mov al, CP437_D_V
    mov bl, [box_attr]
    call Graphics_DrawVLine

    ; Right Vertical line ║
    mov dh, [box_r1]
    inc dh
    mov dl, [box_c2]
    mov al, [box_r2]
    sub al, [box_r1]
    dec al
    mov cl, al
    xor ch, ch
    mov al, CP437_D_V
    mov bl, [box_attr]
    call Graphics_DrawVLine

    ; Bottom Left corner ╚
    mov dh, [box_r2]
    mov dl, [box_c1]
    mov al, CP437_D_BL
    mov bl, [box_attr]
    call Graphics_DrawChar

    ; Bottom Horizontal line ═
    mov dh, [box_r2]
    mov dl, [box_c1]
    inc dl
    mov al, [box_c2]
    sub al, [box_c1]
    dec al
    mov cl, al
    xor ch, ch
    mov al, CP437_D_H
    mov bl, [box_attr]
    call Graphics_DrawHLine

    ; Bottom Right corner ╝
    mov dh, [box_r2]
    mov dl, [box_c2]
    mov al, CP437_D_BR
    mov bl, [box_attr]
    call Graphics_DrawChar

    pop dx
    pop cx
    pop bx
    pop ax
    ret
Graphics_DrawBoxDouble endp

; ------------------------------------------------------------------------------
; Graphics_DrawBoxSingle
; Draws a single-lined box from (DH=r1, DL=c1) to (CH=r2, CL=c2) with attribute BL.
; Input:  DH = top row, DL = left col
;         CH = bottom row, CL = right col
;         BL = attribute
; ------------------------------------------------------------------------------
Graphics_DrawBoxSingle proc
    push ax
    push bx
    push cx
    push dx

    mov [box_r1], dh
    mov [box_c1], dl
    mov [box_r2], ch
    mov [box_c2], cl
    mov [box_attr], bl

    ; Top Left corner ┌
    mov dh, [box_r1]
    mov dl, [box_c1]
    mov al, CP437_S_TL
    mov bl, [box_attr]
    call Graphics_DrawChar

    ; Top Horizontal line ─
    mov dh, [box_r1]
    mov dl, [box_c1]
    inc dl
    mov al, [box_c2]
    sub al, [box_c1]
    dec al
    mov cl, al
    xor ch, ch
    mov al, CP437_S_H
    mov bl, [box_attr]
    call Graphics_DrawHLine

    ; Top Right corner ┐
    mov dh, [box_r1]
    mov dl, [box_c2]
    mov al, CP437_S_TR
    mov bl, [box_attr]
    call Graphics_DrawChar

    ; Left Vertical line │
    mov dh, [box_r1]
    inc dh
    mov dl, [box_c1]
    mov al, [box_r2]
    sub al, [box_r1]
    dec al
    mov cl, al
    xor ch, ch
    mov al, CP437_S_V
    mov bl, [box_attr]
    call Graphics_DrawVLine

    ; Right Vertical line │
    mov dh, [box_r1]
    inc dh
    mov dl, [box_c2]
    mov al, [box_r2]
    sub al, [box_r1]
    dec al
    mov cl, al
    xor ch, ch
    mov al, CP437_S_V
    mov bl, [box_attr]
    call Graphics_DrawVLine

    ; Bottom Left corner └
    mov dh, [box_r2]
    mov dl, [box_c1]
    mov al, CP437_S_BL
    mov bl, [box_attr]
    call Graphics_DrawChar

    ; Bottom Horizontal line ─
    mov dh, [box_r2]
    mov dl, [box_c1]
    inc dl
    mov al, [box_c2]
    sub al, [box_c1]
    dec al
    mov cl, al
    xor ch, ch
    mov al, CP437_S_H
    mov bl, [box_attr]
    call Graphics_DrawHLine

    ; Bottom Right corner ┘
    mov dh, [box_r2]
    mov dl, [box_c2]
    mov al, CP437_S_BR
    mov bl, [box_attr]
    call Graphics_DrawChar

    pop dx
    pop cx
    pop bx
    pop ax
    ret
Graphics_DrawBoxSingle endp

; ------------------------------------------------------------------------------
; Graphics_FillArea
; Fills rectangular region (DH=r1, DL=c1) to (CH=r2, CL=c2) with char AL and attr BL.
; ------------------------------------------------------------------------------
Graphics_FillArea proc
    push ax
    push bx
    push cx
    push dx

    mov [fill_r1], dh
    mov [fill_c1], dl
    mov [fill_r2], ch
    mov [fill_c2], cl
    mov [fill_char], al
    mov [fill_attr], bl

    mov dh, [fill_r1]
g_fa_row:
    mov dl, [fill_c1]
    mov al, [fill_c2]
    sub al, [fill_c1]
    inc al
    mov cl, al
    xor ch, ch
    mov al, [fill_char]
    mov bl, [fill_attr]
    call Graphics_DrawHLine
    inc dh
    cmp dh, [fill_r2]
    jbe g_fa_row

    pop dx
    pop cx
    pop bx
    pop ax
    ret
Graphics_FillArea endp

; ------------------------------------------------------------------------------
; Graphics_DrawHeader
; Draws the standard top banner for Crimson Orbit screens.
; Input:  DS:SI -> Screen Title String (e.g. "PIANO INTERFACE")
; ------------------------------------------------------------------------------
Graphics_DrawHeader proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; Top border: Row 0, Col 0 to Col 79
    mov dh, 0
    mov dl, 0
    mov cx, 80
    mov al, CP437_D_H
    mov bl, THEME_BORDER
    call Graphics_DrawHLine

    ; Title Bar Background: Row 1
    mov dh, 1
    mov dl, 0
    mov ch, 1
    mov cl, 79
    mov al, ' '
    mov bl, 07h
    call Graphics_FillArea

    ; Main Crimson Orbit Branding on Left
    mov dh, 1
    mov dl, 2
    mov bl, THEME_TITLE
    mov si, str_orbit_brand
    call Utils_PrintStringAt

    ; Screen Title on Right
    pop si
    push si
    mov dh, 1
    mov dl, 45
    mov bl, THEME_ACCENT
    call Utils_PrintStringAt

    ; Separator: Row 2, Col 0 to Col 79
    mov dh, 2
    mov dl, 0
    mov cx, 80
    mov al, CP437_D_H
    mov bl, THEME_BORDER
    call Graphics_DrawHLine

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Graphics_DrawHeader endp

; ------------------------------------------------------------------------------
; Graphics_DrawFooter
; Draws standard bottom instruction bar at Row 23 & 24.
; Input:  DS:SI -> Footer Instruction String (e.g. "[ESC] Main Menu  [Q..U] Notes")
; ------------------------------------------------------------------------------
Graphics_DrawFooter proc
    push ax
    push bx
    push cx
    push dx
    push si

    ; Footer separator line at Row 23
    mov dh, 23
    mov dl, 0
    mov cx, 80
    mov al, CP437_S_H
    mov bl, THEME_MUTED
    call Graphics_DrawHLine

    ; Clear Row 24
    mov dh, 24
    mov dl, 0
    mov ch, 24
    mov cl, 79
    mov al, ' '
    mov bl, 07h
    call Graphics_FillArea

    ; Print instruction string centered or at col 2
    pop si
    mov dh, 24
    mov dl, 2
    mov bl, THEME_TEXT
    call Utils_PrintStringAt

    pop dx
    pop cx
    pop bx
    pop ax
    ret
Graphics_DrawFooter endp

; ------------------------------------------------------------------------------
; Graphics Internal Variables & Strings
; ------------------------------------------------------------------------------
box_r1          db 0
box_c1          db 0
box_r2          db 0
box_c2          db 0
box_attr        db 0

fill_r1         db 0
fill_c1         db 0
fill_r2         db 0
fill_c2         db 0
fill_char       db 0
fill_attr       db 0

str_orbit_brand db "CRIMSON ORBIT :: MUSICAL BAND", 0
