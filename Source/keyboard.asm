; ==============================================================================
; CRIMSON ORBIT – MUSICAL BAND
; Module: Keyboard Input System (keyboard.asm)
; Target Assembler: emu8086
; Centralized BIOS keyboard handling, buffering, and key translation.
; ==============================================================================

; ------------------------------------------------------------------------------
; Standard ASCII Key Constants
; ------------------------------------------------------------------------------
KEY_ESC             equ 1Bh
KEY_ENTER           equ 0Dh
KEY_SPACE           equ 20h
KEY_BACKSPACE       equ 08h
KEY_TAB             equ 09h

; ------------------------------------------------------------------------------
; Keyboard_WaitKey
; Blocks until a key is pressed.
; Output: AL = ASCII character (00h for special/extended keys)
;         AH = BIOS scan code
; ------------------------------------------------------------------------------
Keyboard_WaitKey proc
    mov ah, 00h
    int 16h
    ret
Keyboard_WaitKey endp

; ------------------------------------------------------------------------------
; Keyboard_CheckKey
; Non-blocking check for keyboard input.
; Output: ZF = 1 if no keystroke is available
;         ZF = 0 if a keystroke is available:
;             AL = ASCII character
;             AH = BIOS scan code
; (Note: Does NOT remove the key from the keyboard buffer)
; ------------------------------------------------------------------------------
Keyboard_CheckKey proc
    mov ah, 01h
    int 16h
    ret
Keyboard_CheckKey endp

; ------------------------------------------------------------------------------
; Keyboard_ClearBuffer
; Flushes all pending keystrokes from the BIOS keyboard buffer.
; ------------------------------------------------------------------------------
Keyboard_ClearBuffer proc
    push ax
k_flush_loop:
    call Keyboard_CheckKey
    jz k_flush_done             ; Buffer is empty
    call Keyboard_WaitKey       ; Consume key
    jmp k_flush_loop
k_flush_done:
    pop ax
    ret
Keyboard_ClearBuffer endp

; ------------------------------------------------------------------------------
; Keyboard_ToUpper
; Converts ASCII character in AL to uppercase if it is 'a'..'z'.
; Input/Output: AL = ASCII character
; ------------------------------------------------------------------------------
Keyboard_ToUpper proc
    cmp al, 'a'
    jb k_tu_done
    cmp al, 'z'
    ja k_tu_done
    sub al, 20h
k_tu_done:
    ret
Keyboard_ToUpper endp

; ------------------------------------------------------------------------------
; Keyboard_WaitAnyKey
; Clears the buffer, then waits for any single keypress and discards it.
; ------------------------------------------------------------------------------
Keyboard_WaitAnyKey proc
    call Keyboard_ClearBuffer
    call Keyboard_WaitKey
    ret
Keyboard_WaitAnyKey endp
