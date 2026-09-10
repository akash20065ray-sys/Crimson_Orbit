/* ==============================================================================
   CRIMSON ORBIT :: TARGETED MICRO-INTERCEPTION BRIDGE (bridge.js)
   Hardware-to-Software Virtualization Bridge & 4-Byte Micro-Packet Engine
   Intel 8253 PIT (Port 42h) & Intel 8255 PPI (Port 61h) Bus Cycle Interceptor
   ============================================================================== */

(function(window) {
    'use strict';

    const PIT_MASTER_FREQ = 1193180; // 1.19318 MHz Master Clock (14.31818 MHz / 12)
    const PACKET_SIZE = 4;           // 4-Byte Micro-Packet

    // Command Codes
    const CMD_NOTE_OFF    = 0x00;
    const CMD_NOTE_ON     = 0x01;
    const CMD_NOISE_BURST = 0x02;    // Galois LFSR Percussion Trigger

    class MicroInterceptionBridge {
        constructor() {
            this.port42_lsb = 0;
            this.port42_msb = 0;
            this.port42_expect_msb = false;
            this.port61_state = 0x00;
            this.currentDivisor = 0;
            this.currentFrequency = 0;
            this.isSpeakerEnabled = false;

            // Performance & Latency Telemetry
            this.metrics = {
                packetCount: 0,
                totalLatencyMs: 0,
                lastLatencyMs: 0,
                minLatencyMs: 9999,
                maxLatencyMs: 0,
                history: []
            };

            // Event Listeners for UI HUD
            this.busListeners = [];

            // Pre-compiled 8086 RAM Tape Song Offsets in Floppy Image (new2.flp)
            // Kernel loaded at sector 1 (Offset 0x200), songs located in songs.asm
            this.FLOPPY_SECTOR_SIZE = 512;
            this.SONG_CUSTOM_USER_OFFSET = 0x3A00; // Offset inside floppy image
        }

        /**
         * Subscribe a listener to live 8086 bus cycle activity
         */
        onBusActivity(callback) {
            this.busListeners.push(callback);
        }

        _notifyBusActivity(eventType, details) {
            this.busListeners.forEach(cb => {
                try { cb(eventType, details); } catch (e) { console.error(e); }
            });
        }

        /**
         * Intercept an OUT instruction to 8086 I/O Port
         * @param {number} port - 0x42 (PIT Ch2) or 0x61 (PPI Port B)
         * @param {number} value - 8-bit register value (AL)
         * @param {number} durationMs - Optional step duration in ms
         */
        interceptOut(port, value, durationMs = 300) {
            const t0 = performance.now();
            value = value & 0xFF;

            if (port === 0x42) {
                // Intel 8253 PIT Channel 2 receives LSB then MSB
                if (!this.port42_expect_msb) {
                    this.port42_lsb = value;
                    this.port42_expect_msb = true;
                } else {
                    this.port42_msb = value;
                    this.port42_expect_msb = false;

                    // Reconstruct 16-bit divisor
                    this.currentDivisor = (this.port42_msb << 8) | this.port42_lsb;
                    if (this.currentDivisor > 0) {
                        this.currentFrequency = Math.round(PIT_MASTER_FREQ / this.currentDivisor);
                    } else {
                        this.currentFrequency = 0;
                    }
                }
            } else if (port === 0x61) {
                // PPI Port 61h: Bit 0 = Gate 2, Bit 1 = Speaker Data
                this.port61_state = value;
                const gate = (value & 0x01) !== 0;
                const speaker = (value & 0x02) !== 0;
                this.isSpeakerEnabled = gate && speaker;
            }

            // Construct 4-Byte Micro-Packet
            const cmd = this.isSpeakerEnabled ? CMD_NOTE_ON : CMD_NOTE_OFF;
            const packet = this.serializeMicroPacket(
                cmd,
                this.port42_lsb,
                this.port42_msb,
                Math.min(255, Math.round(durationMs / 10)) // Quantized duration (10ms units)
            );

            const t1 = performance.now();
            const latencyMs = Math.max(0.05, t1 - t0);

            // Record Metrics
            this.metrics.packetCount++;
            this.metrics.lastLatencyMs = latencyMs;
            this.metrics.totalLatencyMs += latencyMs;
            if (latencyMs < this.metrics.minLatencyMs) this.metrics.minLatencyMs = latencyMs;
            if (latencyMs > this.metrics.maxLatencyMs) this.metrics.maxLatencyMs = latencyMs;

            // Broadcast to HUD
            this._notifyBusActivity('BUS_CYCLE', {
                port: '0x' + port.toString(16).toUpperCase().padStart(2, '0'),
                value: '0x' + value.toString(16).toUpperCase().padStart(2, '0'),
                divisor: this.currentDivisor,
                frequency: this.currentFrequency,
                speakerState: this.isSpeakerEnabled,
                latencyMs: latencyMs,
                packet: Array.from(packet),
                avgLatencyMs: (this.metrics.totalLatencyMs / this.metrics.packetCount).toFixed(2)
            });

            return {
                packet: packet,
                frequency: this.currentFrequency,
                enabled: this.isSpeakerEnabled,
                latencyMs: latencyMs
            };
        }

        /**
         * Serialize an event into the formal 4-Byte Micro-Packet
         * Format: <CMD, DIV_LSB, DIV_MSB, DURATION>
         */
        serializeMicroPacket(cmd, divLsb, divMsb, durationByte) {
            const buffer = new Uint8Array(PACKET_SIZE);
            buffer[0] = cmd & 0xFF;
            buffer[1] = divLsb & 0xFF;
            buffer[2] = divMsb & 0xFF;
            buffer[3] = durationByte & 0xFF;
            return buffer;
        }

        /**
         * Deserializes a 4-Byte Micro-Packet
         */
        deserializeMicroPacket(packetBuffer) {
            if (packetBuffer.length < 4) return null;
            const cmd = packetBuffer[0];
            const divLsb = packetBuffer[1];
            const divMsb = packetBuffer[2];
            const duration = packetBuffer[3] * 10; // Convert 10ms units to ms

            const divisor = (divMsb << 8) | divLsb;
            const frequency = divisor > 0 ? Math.round(PIT_MASTER_FREQ / divisor) : 0;

            return {
                command: cmd,
                divisor: divisor,
                frequency: frequency,
                durationMs: duration
            };
        }

        /**
         * Convenience helper: Converts Frequency (Hz) to 8086 PIT Divisor and dispatches bus cycle
         */
        dispatchTone(frequencyHz, durationMs = 300) {
            if (!frequencyHz || frequencyHz <= 0) {
                // Mute
                this.interceptOut(0x61, 0x00, durationMs);
                return;
            }

            const divisor = Math.round(PIT_MASTER_FREQ / frequencyHz);
            const lsb = divisor & 0xFF;
            const msb = (divisor >> 8) & 0xFF;

            // 1. Send Divisor LSB then MSB to Port 42h
            this.interceptOut(0x42, lsb, durationMs);
            this.interceptOut(0x42, msb, durationMs);

            // 2. Enable Speaker via Port 61h (bits 0 and 1 = 0x03)
            return this.interceptOut(0x61, 0x03, durationMs);
        }

        /**
         * Deserializes an In-RAM 8086 Song Tape from raw ArrayBuffer (e.g. new2.flp or kernel.bin)
         * Data structure in assembly (Source/composer.asm & songs.asm):
         * Array of 16-bit word pairs: [Frequency, Duration], terminated by 0xFFFF, 0
         */
        parseAssemblySongTape(arrayBuffer, byteOffset = 0) {
            const view = new DataView(arrayBuffer);
            const notes = [];
            let ptr = byteOffset;

            while (ptr + 4 <= arrayBuffer.byteLength) {
                const freq = view.getUint16(ptr, true);     // Little-endian
                const dur  = view.getUint16(ptr + 2, true);

                if (freq === 0xFFFF) break; // End of Song Tape Marker

                notes.push({
                    frequency: freq,
                    durationMs: dur
                });
                ptr += 4;
            }

            return notes;
        }

        /**
         * Serializes Web Sequencer notes into raw 16-bit 8086 Assembly memory bytes
         * Format: dw Freq, Dur ... dw 0FFFFh, 0
         */
        exportToAssemblyTape(notesArray) {
            const buffer = new ArrayBuffer((notesArray.length + 1) * 4);
            const view = new DataView(buffer);
            let ptr = 0;

            for (let i = 0; i < notesArray.length; i++) {
                const n = notesArray[i];
                view.setUint16(ptr, n.frequency || 0, true);
                view.setUint16(ptr + 2, n.durationMs || 300, true);
                ptr += 4;
            }

            // EOF Marker
            view.setUint16(ptr, 0xFFFF, true);
            view.setUint16(ptr + 2, 0, true);

            return new Uint8Array(buffer);
        }
    }

    // Export globally
    window.MicroInterceptionBridge = MicroInterceptionBridge;
    window.bridge = new MicroInterceptionBridge();

})(window);
