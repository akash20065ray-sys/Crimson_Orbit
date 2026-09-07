; ==============================================================================
; CRIMSON ORBIT – MUSICAL BAND
; Module: Utility Procedures (utils.asm)
; Target Assembler: emu8086
; Shared generic utility routines for cursor, string, screen, and timing.
; ==============================================================================

; ------------------------------------------------------------------------------
; Utils_ClearScreen
; Clears the full 80x25 text screen with color attribute in BL.
; Input:  BL = color attribute (e.g. 07h = white on black, 0Ch = crimson on black)
; Output: Cursor placed at (0,0)
; ------------------------------------------------------------------------------
Utils_ClearScreen proc
    push ax
    push bx
    push cx
    push dx

    mov bh, bl                  ; Attribute for blank lines
    mov ax, 0600h               ; AH=06h (scroll up), AL=00h (clear full screen)
    xor cx, cx                  ; Upper left = (0,0)
    mov dx, 184Fh               ; Lower right = (24,79)
    int 10h

    ; Position cursor at home (0,0)
    xor dx, dx
    call Utils_SetCursor

    pop dx
    pop cx
    pop bx
    pop ax
    ret
Utils_ClearScreen endp

; ------------------------------------------------------------------------------
; Utils_SetCursor
; Positions the text cursor at row DH, col DL.
; Input:  DH = row (0..24), DL = col (0..79)
; ------------------------------------------------------------------------------
Utils_SetCursor proc
    push ax
    push bx
    mov ah, 02h
    xor bh, bh                  ; Page 0
    int 10h
    pop bx
    pop ax
    ret
Utils_SetCursor endp

; ------------------------------------------------------------------------------
; Utils_GetCursor
; Reads current cursor position.
; Output: DH = row, DL = col
; ------------------------------------------------------------------------------
Utils_GetCursor proc
    push ax
    push bx
    push cx
    mov ah, 03h
    xor bh, bh
    int 10h
    pop cx
    pop bx
    pop ax
    ret
Utils_GetCursor endp

; ------------------------------------------------------------------------------
; Utils_HideCursor
; Makes the text cursor invisible.
; ------------------------------------------------------------------------------
Utils_HideCursor proc
    push ax
    push cx
    mov ah, 01h
    mov cx, 2607h               ; Invisible cursor scanlines
    int 10h
    pop cx
    pop ax
    ret
Utils_HideCursor endp

; ------------------------------------------------------------------------------
; Utils_ShowCursor
; Restores the standard underline text cursor.
; ------------------------------------------------------------------------------
Utils_ShowCursor proc
    push ax
    push cx
    mov ah, 01h
    mov cx, 0607h               ; Standard cursor scanlines
    int 10h
    pop cx
    pop ax
    ret
Utils_ShowCursor endp

; ------------------------------------------------------------------------------
; Utils_PrintChar
; Outputs character in AL at current cursor location (teletype mode).
; Input:  AL = ASCII character
; ------------------------------------------------------------------------------
Utils_PrintChar proc
    push ax
    push bx
    mov ah, 0Eh
    xor bh, bh
    int 10h
    pop bx
    pop ax
    ret
Utils_PrintChar endp

; ------------------------------------------------------------------------------
; Utils_PrintString
; Prints null-terminated string at DS:SI at current cursor location.
; Input:  DS:SI -> null-terminated string
; ------------------------------------------------------------------------------
Utils_PrintString proc
    push ax
    push si
u_ps_loop:
    lodsb
    test al, al
    jz u_ps_done
    call Utils_PrintChar
    jmp u_ps_loop
u_ps_done:
    pop si
    pop ax
    ret
Utils_PrintString endp

; ------------------------------------------------------------------------------
; Utils_PrintStringAt
; Prints null-terminated string at specified (DH, DL) with color attribute BL.
; Input:  DH = row (0..24)
;         DL = col (0..79)
;         BL = color attribute
;         DS:SI -> null-terminated string
; ------------------------------------------------------------------------------
Utils_PrintStringAt proc
    push ax
    push bx
    push cx
    push dx
    push si

u_psa_loop:
    lodsb
    test al, al
    jz u_psa_done

    ; Set cursor at current (DH, DL)
    call Utils_SetCursor

    ; Write character with attribute BL
    mov ah, 09h
    xor bh, bh                  ; Page 0
    mov cx, 1                   ; 1 character
    int 10h

    inc dl                      ; Advance column
    cmp dl, 80
    jb u_psa_loop
    ; Wrap to next line if exceeds column 79
    xor dl, dl
    inc dh
    jmp u_psa_loop

u_psa_done:
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Utils_PrintStringAt endp

; ------------------------------------------------------------------------------
; Utils_DelayTicks
; Waits for CX BIOS timer ticks (1 tick ≈ 54.9 ms, ~18.2 ticks per second).
; Reads the 16-bit tick counter from BIOS Data Area 0040h:006Ch.
; Input:  CX = number of ticks to delay
; ------------------------------------------------------------------------------
Utils_DelayTicks proc
    push ax
    push ds
    push si

    test cx, cx
    jz u_dt_done

    ; Access BIOS Data Area (segment 0040h)
    mov ax, 0040h
    mov ds, ax
    mov si, 006Ch               ; BDA timer low word

u_dt_outer:
    mov ax, [si]
u_dt_wait:
    cmp ax, [si]
    je u_dt_wait                ; Wait until tick value changes
    loop u_dt_outer

u_dt_done:
    pop si
    pop ds
    pop ax
    ret
Utils_DelayTicks endp

; ------------------------------------------------------------------------------
; Utils_DelayMs
; Approximate millisecond delay for short UI / percussion effects.
; Input:  CX = approximate milliseconds (1..65535)
; ------------------------------------------------------------------------------
Utils_DelayMs proc
    push ax
    push cx
    push dx

u_dms_outer:
    mov dx, 600                 ; Calibrated loop count for 1ms on typical 8086/VMware
u_dms_inner:
    dec dx
    jnz u_dms_inner
    loop u_dms_outer

    pop dx
    pop cx
    pop ax
    ret
Utils_DelayMs endp
