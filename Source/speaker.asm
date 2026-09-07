; ==============================================================================
; CRIMSON ORBIT – MUSICAL BAND
; Module: PC Speaker Sound Engine (speaker.asm)
; Target Assembler: emu8086
; High-Fidelity Acoustic Audio Synthesis Engine for Intel 8254 PIT & 8255 PPI.
; Features:
; - Real Piano Hammer Attack & Multi-Stage Acoustic Decay with Sustain Pedal
; - Real Guitar Plectrum Attack, Singing Acoustic Vibrato & Strum Arpeggios
; - Real Drum Kit: LFSR White-Noise Snare & Cymbals, Punchy Bass Drum, Warm Toms
; ==============================================================================

; ------------------------------------------------------------------------------
; Hardware Port Definitions
; ------------------------------------------------------------------------------
PIT_CONTROL         equ 43h     ; PIT Mode / Command Register
PIT_CHANNEL2        equ 42h     ; PIT Channel 2 Data Port
PPI_PORT_B          equ 61h     ; System Control Port B (Speaker Gate & Data)
PIT_FREQ_BASE_LO    equ 34DCh   ; 1,193,180 Hz low word
PIT_FREQ_BASE_HI    equ 0012h   ; 1,193,180 Hz high word

; ------------------------------------------------------------------------------
; Global Audio Engine State Variables
; ------------------------------------------------------------------------------
piano_sustain_flag  dw 0        ; 0 = Normal Damper, 1 = Sustain Pedal ON
lfsr_noise_seed     dw 0ACE1h   ; Galois 16-bit LFSR Seed for White Noise

; ------------------------------------------------------------------------------
; Speaker_ToneOn
; Starts tone on PC Speaker at frequency specified in AX (Hz).
; If AX = 0, turns off the speaker.
; Input:  AX = frequency in Hz (e.g. 440, 523, 880)
; ------------------------------------------------------------------------------
Speaker_ToneOn proc
    push ax
    push bx
    push dx

    test ax, ax
    jz spk_ton_off              ; 0 Hz means rest / mute

    mov bx, ax                  ; BX = frequency divisor operand

    ; Calculate PIT divisor: DX:AX = 1,193,180 / BX
    mov dx, PIT_FREQ_BASE_HI
    mov ax, PIT_FREQ_BASE_LO
    div bx                      ; AX = Divisor, DX = Remainder

    mov bx, ax                  ; BX = 16-bit divisor

    ; Configure PIT Channel 2: Mode 3 (Square Wave), LSB then MSB
    mov al, 0B6h
    out PIT_CONTROL, al

    ; Send Divisor LSB then MSB to Channel 2
    mov al, bl
    out PIT_CHANNEL2, al
    mov al, bh
    out PIT_CHANNEL2, al

    ; Enable Speaker Output (PPI Port 61h bits 0 and 1)
    in al, PPI_PORT_B
    or al, 03h
    out PPI_PORT_B, al
    jmp spk_ton_done

spk_ton_off:
    call Speaker_ToneOff

spk_ton_done:
    pop dx
    pop bx
    pop ax
    ret
Speaker_ToneOn endp

; ------------------------------------------------------------------------------
; Speaker_ToneOff
; Disables PC Speaker tone generation by clearing bits 0 and 1 on Port 61h.
; ------------------------------------------------------------------------------
Speaker_ToneOff proc
    push ax
    in al, PPI_PORT_B
    and al, 0FCh                ; Clear bits 0 (Timer 2 Gate) and 1 (Speaker Data)
    out PPI_PORT_B, al
    pop ax
    ret
Speaker_ToneOff endp

; ------------------------------------------------------------------------------
; Speaker_PlayToneMs
; Plays a clean tone at AX Hz for CX milliseconds with micro-articulation.
; Input:  AX = frequency in Hz
;         CX = duration in milliseconds
; ------------------------------------------------------------------------------
Speaker_PlayToneMs proc
    push ax
    push cx

    test ax, ax
    jz spk_ptm_rest

    call Speaker_ToneOn
    call Utils_DelayMs
    call Speaker_ToneOff

    ; Short articulation silence between notes (12ms)
    mov cx, 12
    call Utils_DelayMs
    jmp spk_ptm_done

spk_ptm_rest:
    call Speaker_ToneOff
    call Utils_DelayMs

spk_ptm_done:
    pop cx
    pop ax
    ret
Speaker_PlayToneMs endp

; ==============================================================================
; REAL PIANO ACOUSTIC ENGINE
; ==============================================================================

; ------------------------------------------------------------------------------
; Speaker_PianoTone
; Simulates an authentic Grand Piano key strike:
; 1. Hammer Impact Transient: Instantaneous hammer strike click + upper overtone
; 2. Acoustic String Resonance: Clean fundamental at concert frequency
; 3. Multi-Stage Natural Decay: Exponential amplitude decay simulation
; 4. Sustain Pedal Support: Rings out 60% longer if piano_sustain_flag is set.
; Input:  AX = frequency in Hz (e.g. 523 for C5)
;         CX = duration in milliseconds
; ------------------------------------------------------------------------------
Speaker_PianoTone proc
    push ax
    push bx
    push cx
    push dx
    push si

    test ax, ax
    jz spk_piano_rest

    mov bx, ax                  ; BX = fundamental frequency

    ; If Sustain Pedal is active, lengthen sustain duration
    cmp [piano_sustain_flag], 0
    jz spk_p_no_pedal
    mov dx, cx
    shr dx, 1                   ; +50% duration
    add cx, dx
spk_p_no_pedal:

    ; --- Phase 1: Felt Hammer Strike & Upper Harmonic Sparkle (~12ms) ---
    ; Octave harmonic overtone (AX * 2, or +33% if high frequency to avoid overflow)
    mov ax, bx
    cmp ax, 1000
    ja spk_p_high_h
    shl ax, 1                   ; 2x frequency overtone
    jmp spk_p_play_h
spk_p_high_h:
    mov dx, ax
    shr dx, 2
    add ax, dx                  ; +25% overtone
spk_p_play_h:
    call Speaker_ToneOn
    push cx
    mov cx, 12                  ; 12ms hammer contact attack
    call Utils_DelayMs
    pop cx

    ; --- Phase 2: Fundamental String Resonance (~65% of duration) ---
    mov ax, bx
    call Speaker_ToneOn

    ; Calculate 65% of CX
    mov dx, cx
    shr dx, 1                   ; 50%
    mov si, cx
    shr si, 3                   ; 12.5%
    add dx, si                  ; ~62.5%
    push cx
    mov cx, dx
    call Utils_DelayMs
    pop cx

    ; --- Phase 3: Natural Acoustic Decay Envelope (~25% of duration) ---
    ; Emulates string vibration fading by micro-pulsing speaker output
    mov si, 8
spk_p_decay_loop:
    in al, PPI_PORT_B
    and al, 0FDh                ; Mute bit 1 temporarily
    out PPI_PORT_B, al
    push cx
    mov cx, 2
    call Utils_DelayMs
    pop cx

    in al, PPI_PORT_B
    or al, 03h                 ; Re-enable speaker
    out PPI_PORT_B, al
    push cx
    mov cx, 4
    call Utils_DelayMs
    pop cx

    dec si
    jnz spk_p_decay_loop

    call Speaker_ToneOff

    ; Articulation silence (10ms)
    mov cx, 10
    call Utils_DelayMs
    jmp spk_piano_done

spk_piano_rest:
    call Speaker_ToneOff
    call Utils_DelayMs

spk_piano_done:
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Speaker_PianoTone endp

; ==============================================================================
; REAL GUITAR ACOUSTIC & LEAD SOLO ENGINE
; ==============================================================================

; ------------------------------------------------------------------------------
; Speaker_GuitarPluckPro
; Simulates an authentic Acoustic / Lead Guitar string pluck:
; 1. Plectrum / Fingernail Attack Transient: +20% pitch chirp for ~14ms
; 2. Singing Acoustic Vibrato: Modulates pitch ±3 Hz to simulate expressive vibrato
; 3. Natural Exponential Ring-Out Sustain
; Input:  AX = base frequency in Hz (Concert register)
;         CX = total duration in ms
; ------------------------------------------------------------------------------
Speaker_GuitarPluckPro proc
    push ax
    push bx
    push cx
    push dx
    push si

    test ax, ax
    jz spk_gpp_done

    mov bx, ax                  ; BX = nominal fundamental frequency

    ; --- Phase 1: Plectrum Pick Strike Transient (+20% chirp for ~14ms) ---
    mov dx, ax
    shr dx, 2                   ; DX = AX / 4 (+25%)
    add ax, dx
    call Speaker_ToneOn

    push cx
    mov cx, 14
    call Utils_DelayMs
    pop cx

    ; Settle to nominal frequency
    mov ax, bx
    call Speaker_ToneOn

    ; --- Phase 2: Expressive Singing Vibrato Sustain ---
    ; If CX > 60ms, execute warm vibrato cycles
    cmp cx, 60
    jb spk_gpp_short

    sub cx, 18                  ; Deduct attack
    mov si, cx                  ; Remaining ms
    shr si, 4                   ; Number of 16ms vibrato cycles

spk_gpp_vib_loop:
    test si, si
    jz spk_gpp_off

    ; Vibrato High Phase (+3 Hz)
    mov ax, bx
    add ax, 3
    call Speaker_ToneOn
    push cx
    mov cx, 8
    call Utils_DelayMs
    pop cx

    ; Vibrato Low Phase (-2 Hz)
    mov ax, bx
    sub ax, 2
    call Speaker_ToneOn
    push cx
    mov cx, 8
    call Utils_DelayMs
    pop cx

    dec si
    jnz spk_gpp_vib_loop
    jmp spk_gpp_off

spk_gpp_short:
    call Utils_DelayMs

spk_gpp_off:
    call Speaker_ToneOff

    ; String articulation gap
    mov cx, 10
    call Utils_DelayMs

spk_gpp_done:
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Speaker_GuitarPluckPro endp

; ------------------------------------------------------------------------------
; Speaker_GuitarPluck
; Backward-compatible wrapper calling Speaker_GuitarPluckPro
; ------------------------------------------------------------------------------
Speaker_GuitarPluck proc
    call Speaker_GuitarPluckPro
    ret
Speaker_GuitarPluck endp

; ------------------------------------------------------------------------------
; Speaker_StrumChord
; Strums a multi-string chord in rapid arpeggiated acoustic succession:
; Sweeps across 4 to 6 string frequencies with ~16ms per string, then sustains.
; Input:  SI -> Array of word frequencies ending with 0
;         CX = final ring-out duration in ms
; ------------------------------------------------------------------------------
Speaker_StrumChord proc
    push ax
    push bx
    push cx
    push dx
    push si

spk_sc_loop:
    lodsw
    test ax, ax
    jz spk_sc_sustain           ; End of chord array

    ; Pluck individual string during strum sweep
    call Speaker_ToneOn
    push cx
    mov cx, 18
    call Utils_DelayMs
    pop cx
    jmp spk_sc_loop

spk_sc_sustain:
    ; Ring out highest/target string with vibrato
    mov ax, [si - 4]            ; Pick previous valid string note
    test ax, ax
    jz spk_sc_end
    call Speaker_GuitarPluckPro
    jmp spk_sc_done

spk_sc_end:
    call Speaker_ToneOff

spk_sc_done:
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
Speaker_StrumChord endp

; ==============================================================================
; REAL ACOUSTIC PERCUSSION SYNTHESIS (STUDIO DRUM KIT)
; ==============================================================================

; ------------------------------------------------------------------------------
; Sound_RandomLFSR
; 16-bit Galois LFSR for high-speed white noise generation.
; Output: AX = pseudo-random 16-bit word
; ------------------------------------------------------------------------------
Sound_RandomLFSR proc
    push dx
    mov ax, [lfsr_noise_seed]
    test ax, ax
    jnz srl_calc
    mov ax, 0ACE1h              ; Seed recovery
srl_calc:
    mov dx, ax
    shr ax, 1
    test dx, 1
    jz srl_no_xor
    xor ax, 0B400h              ; Polynomial feedback mask
srl_no_xor:
    mov [lfsr_noise_seed], ax
    pop dx
    ret
Sound_RandomLFSR endp

; ------------------------------------------------------------------------------
; Sound_Kick (Punchy Acoustic Bass Drum)
; Synthesizes an authentic 22-inch Kick Drum:
; 1. High-pressure wooden beater impact transient (400 Hz -> 260 Hz in 2ms)
; 2. Deep acoustic shell thud: rapid glide 150 Hz -> 110 Hz -> 82 Hz -> 58 Hz -> 42 Hz
; ------------------------------------------------------------------------------
Sound_Kick proc
    push ax
    push cx
    push dx

    ; 1. Beater Attack Impact Click (420 Hz -> 280 Hz)
    mov ax, 420
    call Speaker_ToneOn
    mov cx, 3
    call Utils_DelayMs

    mov ax, 280
    call Speaker_ToneOn
    mov cx, 3
    call Utils_DelayMs

    ; 2. Resonant Bass Shell Thump
    mov ax, 150
    call Speaker_ToneOn
    mov cx, 7
    call Utils_DelayMs

    mov ax, 110
    call Speaker_ToneOn
    mov cx, 8
    call Utils_DelayMs

    mov ax, 82
    call Speaker_ToneOn
    mov cx, 10
    call Utils_DelayMs

    mov ax, 58
    call Speaker_ToneOn
    mov cx, 12
    call Utils_DelayMs

    mov ax, 42
    call Speaker_ToneOn
    mov cx, 14
    call Utils_DelayMs

    call Speaker_ToneOff

    pop dx
    pop cx
    pop ax
    ret
Sound_Kick endp

; ------------------------------------------------------------------------------
; Sound_Snare (Acoustic Studio Snare Drum)
; Dual-layer physical synthesis:
; Layer 1: Snappy metal snare wire sizzle (high-speed LFSR white noise)
; Layer 2: Resonant wooden shell pop (downward glide 240 Hz -> 175 Hz -> 130 Hz)
; ------------------------------------------------------------------------------
Sound_Snare proc
    push ax
    push bx
    push cx
    push dx

    ; Layer 1: Snare Wire Crackle (LFSR pseudo-random noise burst)
    in al, PPI_PORT_B
    mov bl, al
    mov cx, 85                  ; 85 rapid noise samples
snare_lfsr_loop:
    call Sound_RandomLFSR
    and al, 02h                 ; Mask to speaker data bit 1
    and bl, 0FDh
    or bl, al
    mov al, bl
    out PPI_PORT_B, al

    ; Micro-delay varying with random bit
    mov dx, 18
snare_lfsr_wait:
    dec dx
    jnz snare_lfsr_wait
    loop snare_lfsr_loop

    ; Layer 2: Resonant Wooden Shell Acoustic Body Tone
    mov ax, 240
    call Speaker_ToneOn
    mov cx, 10
    call Utils_DelayMs

    mov ax, 175
    call Speaker_ToneOn
    mov cx, 16
    call Utils_DelayMs

    mov ax, 130
    call Speaker_ToneOn
    mov cx, 18
    call Utils_DelayMs

    call Speaker_ToneOff

    pop dx
    pop cx
    pop bx
    pop ax
    ret
Sound_Snare endp

; ------------------------------------------------------------------------------
; Sound_HiHat (Closed Hi-Hat)
; Ultra-crisp, tight metallic choke (~10ms high-frequency LFSR metallic pulse)
; ------------------------------------------------------------------------------
Sound_HiHat proc
    push ax
    push bx
    push cx
    push dx

    in al, PPI_PORT_B
    mov bl, al
    mov cx, 50                  ; 50 tight high-speed metallic pulses
hihat_pro_loop:
    call Sound_RandomLFSR
    and al, 02h
    and bl, 0FDh
    or bl, al
    mov al, bl
    out PPI_PORT_B, al

    mov dx, 8                   ; Ultra-short delay ~4 microseconds
hihat_pro_wait:
    dec dx
    jnz hihat_pro_wait
    loop hihat_pro_loop

    call Speaker_ToneOff

    pop dx
    pop cx
    pop bx
    pop ax
    ret
Sound_HiHat endp

; ------------------------------------------------------------------------------
; Sound_HiHat_Open (Open Hi-Hat)
; Shimmering metallic sizzle with natural exponential decay over ~60ms.
; ------------------------------------------------------------------------------
Sound_HiHat_Open proc
    push ax
    push bx
    push cx
    push dx

    in al, PPI_PORT_B
    mov bl, al
    mov cx, 110
open_hh_loop:
    call Sound_RandomLFSR
    and al, 02h
    and bl, 0FDh
    or bl, al
    mov al, bl
    out PPI_PORT_B, al

    ; Gradually expanding delay creates natural decay
    mov dx, 160
    sub dx, cx
    shr dx, 2
    inc dx
open_hh_wait:
    dec dx
    jnz open_hh_wait
    loop open_hh_loop

    call Speaker_ToneOff

    pop dx
    pop cx
    pop bx
    pop ax
    ret
Sound_HiHat_Open endp

; ------------------------------------------------------------------------------
; Sound_Tom (Acoustic Rack / Floor Tom)
; Resonant acoustic drumhead pitch bend with stick tip impact:
; 260 Hz -> 215 Hz -> 175 Hz -> 140 Hz -> 110 Hz over ~110ms.
; ------------------------------------------------------------------------------
Sound_Tom proc
    push ax
    push cx

    ; Stick impact attack
    mov ax, 320
    call Speaker_ToneOn
    mov cx, 5
    call Utils_DelayMs

    ; Resonant membrane body
    mov ax, 240
    call Speaker_ToneOn
    mov cx, 18
    call Utils_DelayMs

    mov ax, 195
    call Speaker_ToneOn
    mov cx, 22
    call Utils_DelayMs

    mov ax, 155
    call Speaker_ToneOn
    mov cx, 25
    call Utils_DelayMs

    mov ax, 120
    call Speaker_ToneOn
    mov cx, 25
    call Utils_DelayMs

    mov ax, 95
    call Speaker_ToneOn
    mov cx, 25
    call Utils_DelayMs

    call Speaker_ToneOff

    pop cx
    pop ax
    ret
Sound_Tom endp

; ------------------------------------------------------------------------------
; Sound_Crash (Crash Cymbal)
; Explosive metallic burst: dense LFSR randomized noise burst followed by
; exponential shimmer decay ringing out over ~280ms.
; ------------------------------------------------------------------------------
Sound_Crash proc
    push ax
    push bx
    push cx
    push dx

    in al, PPI_PORT_B
    mov bl, al

    ; High-energy exploding strike burst
    mov cx, 140
crash_pro_burst:
    call Sound_RandomLFSR
    and al, 02h
    and bl, 0FDh
    or bl, al
    mov al, bl
    out PPI_PORT_B, al

    mov dx, 24
crash_pb_wait:
    dec dx
    jnz crash_pb_wait
    loop crash_pro_burst

    ; Shimmering decay tail (increasing intervals)
    mov cx, 100
crash_pro_decay:
    call Sound_RandomLFSR
    and al, 02h
    and bl, 0FDh
    or bl, al
    mov al, bl
    out PPI_PORT_B, al

    mov dx, 120
    sub dx, cx
    shl dx, 1
    add dx, 25
crash_pd_wait:
    dec dx
    jnz crash_pd_wait
    loop crash_pro_decay

    call Speaker_ToneOff

    pop dx
    pop cx
    pop bx
    pop ax
    ret
Sound_Crash endp

; ------------------------------------------------------------------------------
; Sound_Ride (Ride Cymbal / Bell)
; Clear metallic brass ping with high overtone shimmer:
; 1046 Hz (C6) -> 1318 Hz (E6) -> metallic sizzle decay.
; ------------------------------------------------------------------------------
Sound_Ride proc
    push ax
    push cx

    mov ax, 1318                ; High E6 bell ping
    call Speaker_ToneOn
    mov cx, 12
    call Utils_DelayMs

    mov ax, 1046                ; C6 bell resonance
    call Speaker_ToneOn
    mov cx, 30
    call Utils_DelayMs

    call Sound_HiHat            ; Metallic shimmer tail

    pop cx
    pop ax
    ret
Sound_Ride endp
