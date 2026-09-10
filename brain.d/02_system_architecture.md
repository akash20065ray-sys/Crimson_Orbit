# 🏛️ 02. System Architecture & Hardware Specifications

## 3-Tier Layered Architecture

```
+-----------------------------------------------------------------------------------+
|  LAYER 1: BARE-METAL 16-BIT 8086 REAL-MODE ASSEMBLY ENGINE                       |
|  - Intel 8253 PIT Timer (Channel 2 Freq Divisors: 1,193,180 / f)                  |
|  - Intel 8255 PPI Port 61h Speaker Gate Control (Bits 0 & 1)                      |
|  - In-RAM 60-Note Composer Tape Buffer (composer.asm)                             |
|  - Galois 16-Bit LFSR White Noise Generator (speaker.asm)                         |
+-----------------------------------------------------------------------------------+
                                         │  Port I/O Bus Cycles (OUT 42h, OUT 61h)
                                         ▼
+-----------------------------------------------------------------------------------+
|  LAYER 2: LOW-LATENCY WEBASSEMBLY (Wasm) INTERCEPTION BRIDGE                      |
|  - Targeted Bus-Cycle Micro-Packet (<CMD, DIV_LO, DIV_HI, DURATION>)              |
|  - Sub-12ms Round-Trip Audio Latency (vs. 60–120ms legacy full VM)                |
|  - Ultra-lightweight footprint (~12.4 MB vs. >150 MB QEMU/v86)                   |
|  - Zero-Copy Ring Buffer via SharedArrayBuffer & AudioWorklet                     |
+-----------------------------------------------------------------------------------+
                                         │  WebAudio API Graph Dispatch
                                         ▼
+-----------------------------------------------------------------------------------+
|  LAYER 3: MULTI-TIMBRAL ACOUSTIC RESYNTHESIS & WEB STUDIO                         |
|  - WebAudio DSP Engine (44.1 kHz 16-bit PCM multi-timbral synthesis)             |
|  - Dual-Engine Toggle: Authentic 1-Bit Square Wave vs. Acoustic Resynthesis      |
|  - Acoustic Models: Steinway Piano, Martin Acoustic Guitar, Ludwig Drum Kit      |
|  - 16-Step Dual Matrix Sequencer & Real-Time FFT Spectrum Visualizer              |
+-----------------------------------------------------------------------------------+
```

## Hardware Ports Summary
* **Port 43h:** PIT Control Word Register (`0B6h` = Channel 2, LSB/MSB, Mode 3, Binary)
* **Port 42h:** PIT Channel 2 Data Port (Divisor byte stream)
* **Port 61h:** PPI System Control Port B (Bit 0 = Gate 2, Bit 1 = Speaker Data)
* **Base Clock:** $1,193,180\text{ Hz}$ derived from $\frac{14.31818\text{ MHz}}{12}$
