; ==============================================================================
; CRIMSON ORBIT – MUSICAL BAND
; Module: Song Repertoire Data (songs.asm)
; Target Assembler: emu8086
; Pre-installed concert song scores transposed to crystal-clear high-Hertz
; concert octaves (523..1568 Hz) for sparkling, professional melodic playback:
; 1. Happy Birthday
; 2. Twinkle Twinkle Little Star
; 3. Ode to Joy (Beethoven's 9th Symphony)
; 4. Jingle Bells
; 5. Mary Had a Little Lamb
; 6. London Bridge Is Falling Down
; ==============================================================================

; ------------------------------------------------------------------------------
; Elevated Concert Pitch Frequencies (Octaves 5 & 6 - Bright & Singing)
; ------------------------------------------------------------------------------
N_REST      equ 0
N_G4        equ 392
N_A4        equ 440
N_B4        equ 494
N_C5        equ 523
N_CS5       equ 554
N_D5        equ 587
N_DS5       equ 622
N_E5        equ 659
N_F5        equ 698
N_FS5       equ 740
N_G5        equ 784
N_GS5       equ 831
N_A5        equ 880
N_AS5       equ 932
N_B5        equ 988
N_C6        equ 1046
N_D6        equ 1175
N_E6        equ 1318
N_F6        equ 1397
N_G6        equ 1568

SONG_END    equ 0FFFFh

; ------------------------------------------------------------------------------
; Song 1: Happy Birthday (Concert Pitch)
; ------------------------------------------------------------------------------
Song_HappyBirthday:
    dw N_G5, 250,  N_G5, 250,  N_A5, 500,  N_G5, 500,  N_C6, 500,  N_B5, 1000
    dw N_REST, 150
    dw N_G5, 250,  N_G5, 250,  N_A5, 500,  N_G5, 500,  N_D6, 500,  N_C6, 1000
    dw N_REST, 150
    dw N_G5, 250,  N_G5, 250,  N_G6, 500,  N_E6, 500,  N_C6, 500,  N_B5, 500,  N_A5, 750
    dw N_REST, 150
    dw N_F6, 250,  N_F6, 250,  N_E6, 500,  N_C6, 500,  N_D6, 500,  N_C6, 1000
    dw SONG_END, 0

; ------------------------------------------------------------------------------
; Song 2: Twinkle Twinkle Little Star (Concert Pitch)
; ------------------------------------------------------------------------------
Song_TwinkleTwinkle:
    dw N_C5, 400,  N_C5, 400,  N_G5, 400,  N_G5, 400,  N_A5, 400,  N_A5, 400,  N_G5, 800
    dw N_REST, 100
    dw N_F5, 400,  N_F5, 400,  N_E5, 400,  N_E5, 400,  N_D5, 400,  N_D5, 400,  N_C5, 800
    dw N_REST, 100
    dw N_G5, 400,  N_G5, 400,  N_F5, 400,  N_F5, 400,  N_E5, 400,  N_E5, 400,  N_D5, 800
    dw N_REST, 100
    dw N_G5, 400,  N_G5, 400,  N_F5, 400,  N_F5, 400,  N_E5, 400,  N_E5, 400,  N_D5, 800
    dw N_REST, 100
    dw N_C5, 400,  N_C5, 400,  N_G5, 400,  N_G5, 400,  N_A5, 400,  N_A5, 400,  N_G5, 800
    dw N_REST, 100
    dw N_F5, 400,  N_F5, 400,  N_E5, 400,  N_E5, 400,  N_D5, 400,  N_D5, 400,  N_C5, 800
    dw SONG_END, 0

; ------------------------------------------------------------------------------
; Song 3: Ode to Joy (Beethoven's 9th Symphony)
; ------------------------------------------------------------------------------
Song_OdeToJoy:
    dw N_E5, 380,  N_E5, 380,  N_F5, 380,  N_G5, 380
    dw N_G5, 380,  N_F5, 380,  N_E5, 380,  N_D5, 380
    dw N_C5, 380,  N_C5, 380,  N_D5, 380,  N_E5, 380
    dw N_E5, 550,  N_D5, 220,  N_D5, 750
    dw N_REST, 100
    dw N_E5, 380,  N_E5, 380,  N_F5, 380,  N_G5, 380
    dw N_G5, 380,  N_F5, 380,  N_E5, 380,  N_D5, 380
    dw N_C5, 380,  N_C5, 380,  N_D5, 380,  N_E5, 380
    dw N_D5, 550,  N_C5, 220,  N_C5, 750
    dw SONG_END, 0

; ------------------------------------------------------------------------------
; Song 4: Jingle Bells (Concert Pitch)
; ------------------------------------------------------------------------------
Song_JingleBells:
    dw N_E5, 300,  N_E5, 300,  N_E5, 600
    dw N_REST, 100
    dw N_E5, 300,  N_E5, 300,  N_E5, 600
    dw N_REST, 100
    dw N_E5, 300,  N_G5, 300,  N_C5, 400,  N_D5, 200,  N_E5, 800
    dw N_REST, 150
    dw N_F5, 300,  N_F5, 300,  N_F5, 400,  N_F5, 200
    dw N_F5, 300,  N_E5, 300,  N_E5, 300,  N_E5, 200,  N_E5, 200
    dw N_E5, 300,  N_D5, 300,  N_D5, 300,  N_E5, 300,  N_D5, 600,  N_G5, 600
    dw SONG_END, 0

; ------------------------------------------------------------------------------
; Song 5: Mary Had a Little Lamb (Concert Pitch)
; ------------------------------------------------------------------------------
Song_MaryHadALittleLamb:
    dw N_E5, 350,  N_D5, 350,  N_C5, 350,  N_D5, 350
    dw N_E5, 350,  N_E5, 350,  N_E5, 700
    dw N_D5, 350,  N_D5, 350,  N_D5, 700
    dw N_E5, 350,  N_G5, 350,  N_G5, 700
    dw N_E5, 350,  N_D5, 350,  N_C5, 350,  N_D5, 350
    dw N_E5, 350,  N_E5, 350,  N_E5, 350,  N_E5, 350
    dw N_D5, 350,  N_D5, 350,  N_E5, 350,  N_D5, 350,  N_C5, 900
    dw SONG_END, 0

; ------------------------------------------------------------------------------
; Song 6: London Bridge Is Falling Down (Concert Pitch)
; ------------------------------------------------------------------------------
Song_LondonBridge:
    dw N_G5, 400,  N_A5, 200,  N_G5, 300,  N_F5, 300
    dw N_E5, 300,  N_F5, 300,  N_G5, 600
    dw N_D5, 300,  N_E5, 300,  N_F5, 600
    dw N_E5, 300,  N_F5, 300,  N_G5, 600
    dw N_G5, 400,  N_A5, 200,  N_G5, 300,  N_F5, 300
    dw N_E5, 300,  N_F5, 300,  N_G5, 600
    dw N_D5, 400,  N_G5, 400,  N_E5, 400,  N_C5, 800
    dw SONG_END, 0

; ------------------------------------------------------------------------------
; Song Metadata Tables
; ------------------------------------------------------------------------------
song_table:
    dw Song_HappyBirthday
    dw Song_TwinkleTwinkle
    dw Song_OdeToJoy
    dw Song_JingleBells
    dw Song_MaryHadALittleLamb
    dw Song_LondonBridge

song_titles:
    dw str_title_song1
    dw str_title_song2
    dw str_title_song3
    dw str_title_song4
    dw str_title_song5
    dw str_title_song6

str_title_song1     db "Happy Birthday (Concert)", 0
str_title_song2     db "Twinkle Twinkle Little Star", 0
str_title_song3     db "Ode to Joy (Beethoven 9th)", 0
str_title_song4     db "Jingle Bells (High-Hz)", 0
str_title_song5     db "Mary Had a Little Lamb", 0
str_title_song6     db "London Bridge Is Falling Down", 0
