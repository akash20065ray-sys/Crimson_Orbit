#make_boot#
; ==============================================================================
; CRIMSON ORBIT – MUSICAL BAND
; Phase 1: Bare-Metal Floppy Bootloader
; Target Assembler: emu8086
; Target System: 8086 Real Mode / VMware Workstation Floppy Image (1.44 MB)
; Loads kernel from floppy sector 2 into memory segment 1000h:0000h.
; ==============================================================================

org 7C00h

start:
    ; --------------------------------------------------------------------------
    ; 1. Initialize Processor State, Segments, and Stack
    ; --------------------------------------------------------------------------
    cli                         ; Disable interrupts during stack setup
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 7C00h               ; Stack grows down from 0000:7C00h (safe zone)
    sti                         ; Re-enable interrupts

    ; BIOS passes the boot drive index in DL (00h for Floppy 0)
    mov [boot_drive], dl

    ; --------------------------------------------------------------------------
    ; 2. Initialize 80x25 16-Color Color Text Mode (Mode 03h)
    ; --------------------------------------------------------------------------
    mov ax, 0003h
    int 10h

    ; --------------------------------------------------------------------------
    ; 3. Display Crimson Orbit Boot Banner
    ; --------------------------------------------------------------------------
    mov si, msg_title
    call print_string

    mov si, msg_loading
    call print_string

    ; --------------------------------------------------------------------------
    ; 4. Reset Floppy Disk Controller
    ; --------------------------------------------------------------------------
    mov ah, 00h
    mov dl, [boot_drive]
    int 13h
    jc disk_error

    ; --------------------------------------------------------------------------
    ; 5. Load Kernel Sectors into 1000h:0000h
    ;    Reads 36 sectors (18 KB) sequentially using CHS geometry.
    ;    Floppy geometry: 18 sectors/track, 2 heads (0, 1), 80 cylinders.
    ; --------------------------------------------------------------------------
    mov ax, 1000h
    mov es, ax                  ; Destination segment = 1000h
    xor bx, bx                  ; Destination offset  = 0000h

    mov ch, 0                   ; Cylinder 0
    mov dh, 0                   ; Head 0
    mov cl, 2                   ; Start Sector = 2 (Sector 1 is boot sector)
    mov bp, 36                  ; Number of sectors to read (18 KB)

load_loop:
    mov [retry_count], 3        ; Retry each sector up to 3 times

read_sector:
    mov ah, 02h                 ; BIOS INT 13h / AH=02h: Read disk sectors
    mov al, 1                   ; Read 1 sector at a time
    mov dl, [boot_drive]
    int 13h
    jnc read_success            ; Carry flag clear = success

    ; If error, reset disk controller and retry
    xor ax, ax
    mov dl, [boot_drive]
    int 13h

    dec [retry_count]
    jnz read_sector
    jmp disk_error              ; Retries exhausted -> error

read_success:
    ; Print progress dot '.'
    mov al, '.'
    mov ah, 0Eh
    int 10h

    ; Advance memory buffer by 512 bytes (1 sector)
    add bx, 512

    ; Advance CHS address
    inc cl                      ; Next sector
    cmp cl, 18
    jbe advance_done

    ; Reached end of track (sector 18)
    mov cl, 1                   ; Reset to sector 1
    inc dh                      ; Next head (Head 0 -> Head 1)
    cmp dh, 2
    jb advance_done

    ; Reached second head -> advance to next cylinder
    mov dh, 0                   ; Reset to head 0
    inc ch                      ; Next cylinder

advance_done:
    dec bp                      ; Decrement remaining sectors
    jnz load_loop

    ; --------------------------------------------------------------------------
    ; 6. Kernel Load Succeeded: Transfer Control
    ; --------------------------------------------------------------------------
    mov si, msg_ok
    call print_string

    mov si, msg_jump
    call print_string

    ; Far jump to the loaded kernel at 1000h:0000h
    jmp 1000h:0000h

; ------------------------------------------------------------------------------
; Error Handler: Disk Read Failure
; ------------------------------------------------------------------------------
disk_error:
    mov si, msg_err
    call print_string

wait_reboot:
    xor ah, ah                  ; BIOS INT 16h / AH=00h: Wait for keypress
    int 16h
    int 19h                     ; BIOS INT 19h: Warm reboot system
    jmp wait_reboot

; ------------------------------------------------------------------------------
; Helper: Print Teletype String (DS:SI points to null-terminated string)
; ------------------------------------------------------------------------------
print_string:
    push ax
    push si
print_char:
    lodsb
    test al, al
    jz print_done
    mov ah, 0Eh                 ; BIOS INT 10h / AH=0Eh: Teletype output
    int 10h
    jmp print_char
print_done:
    pop si
    pop ax
    ret

; ------------------------------------------------------------------------------
; Data Section
; ------------------------------------------------------------------------------
boot_drive      db 0
retry_count     db 3

msg_title       db 13, 10, "========================================", 13, 10
                db "   CRIMSON ORBIT - SYSTEM BOOTLOADER", 13, 10
                db "========================================", 13, 10, 0
msg_loading     db "Loading Crimson Orbit Kernel [", 0
msg_ok          db "] OK", 13, 10, 0
msg_jump        db "Transferring execution to 1000:0000h...", 13, 10, 0
msg_err         db 13, 10, "CRITICAL: Floppy disk read failure!", 13, 10
                db "Press any key to reboot system...", 13, 10, 0

; Note: When compiled with #make_boot# in emu8086, emu8086 automatically pads 
; the output to 512 bytes and appends the 55AAh boot signature.
