# ⚡ 05. The Targeted Micro-Interception Protocol

## The 4-Byte Micro-Packet Definition

When an `OUT 42h, AL` or `OUT 61h, AL` instruction is executed in the 8086 CPU, the bus trap captures the data and serializes it:

```
+---------------+---------------+---------------+---------------+
|  BYTE 0 (CMD) |  BYTE 1 (DIV) |  BYTE 2 (DIV) |  BYTE 3 (DUR) |
|  Command Code |  Divisor LSB  |  Divisor MSB  | Duration/Velo |
+---------------+---------------+---------------+---------------+
```

### Protocol Fields:
1. **Command (`CMD` - 1 Byte):**
   * `0x00` = `NOTE_OFF` (Port 61h bits 0/1 cleared)
   * `0x01` = `NOTE_ON` (Port 61h bits 0/1 set, tone active)
   * `0x02` = `NOISE_BURST` (Galois LFSR noise trigger for percussion)
2. **Divisor Low Byte (`DIV_LO` - 1 Byte):**
   * First byte written to Port 42h.
3. **Divisor High Byte (`DIV_HI` - 1 Byte):**
   * Second byte written to Port 42h.
4. **Duration / Velocity (`DURATION` - 1 Byte):**
   * Step quantization code (`0x01`=150ms, `0x02`=300ms, `0x03`=600ms, `0x04`=1000ms).

## Frequency Reconstruction Equation
$$\text{Divisor} = (\text{Byte 2} \ll 8) \mid \text{Byte 1}$$
$$\text{Frequency (Hz)} = \frac{1,193,180}{\text{Divisor}}$$

## RAM Song Tape Serialization
In `Source/composer.asm`, songs are stored as an array of 16-bit words:
```assembly
Song_CustomUser:
    dw 440, 300    ; Note 1: 440 Hz, 300 ms
    dw 523, 600    ; Note 2: 523 Hz, 600 ms
    dw 0FFFFh, 0   ; EOF Marker
```
The bridge deserializes this with `DataView.getUint16(offset, true)` directly into the Web Sequencer array.
