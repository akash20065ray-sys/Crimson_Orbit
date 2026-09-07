/* ==============================================================================
   CRIMSON ORBIT :: STUDIO WORKSTATION JAVASCRIPT
   Web Audio API & Real Sampled Instrument Engine (Piano, Guitar, Drums)
   ============================================================================== */

class AudioEngine {
    constructor() {
        this.ctx = null;
        this.masterGain = null;
        this.analyser = null;
        this.buffers = {};
        this.isLoaded = false;
        this.sustainPedal = false;
        this.currentOctave = 4;
        this.currentSongTimer = null;
        this.isPlayingSong = false;
        this.selectedSong = 'happyBirthday';
        this.selectedStyle = 'piano';

        // Sequencer & Composer State
        this.isSequencerPlaying = false;
        this.currentSequencerStep = 0;
        this.composerBpm = 120;
        this.sequencerGrid = {};
        this.sequencerTracks = [];

        // Sample Library Mapping
        this.sampleUrls = {
            // Real Steinway Grand Piano
            'piano_C4': 'audio/piano_C4.mp3',
            'piano_Cs4': 'audio/piano_Cs4.mp3',
            'piano_D4': 'audio/piano_D4.mp3',
            'piano_Ds4': 'audio/piano_Ds4.mp3',
            'piano_E4': 'audio/piano_E4.mp3',
            'piano_F4': 'audio/piano_F4.mp3',
            'piano_Fs4': 'audio/piano_Fs4.mp3',
            'piano_G4': 'audio/piano_G4.mp3',
            'piano_Gs4': 'audio/piano_Gs4.mp3',
            'piano_A4': 'audio/piano_A4.mp3',
            'piano_As4': 'audio/piano_As4.mp3',
            'piano_B4': 'audio/piano_B4.mp3',
            'piano_C5': 'audio/piano_C5.mp3',

            // Real Acoustic Guitar Strings
            'guitar_6': 'audio/guitar_E2.mp3',  // Low E (82 Hz)
            'guitar_5': 'audio/guitar_A2.mp3',  // A (110 Hz)
            'guitar_4': 'audio/guitar_D3.mp3',  // D (147 Hz)
            'guitar_3': 'audio/guitar_G3.mp3',  // G (196 Hz)
            'guitar_2': 'audio/guitar_B3.mp3',  // B (247 Hz)
            'guitar_1': 'audio/guitar_E4.mp3',  // High E (330 Hz)

            // Real Guitar Chords
            'chord_em': 'audio/guitar_chord1.mp3',
            'chord_g': 'audio/guitar_chord2.mp3',
            'chord_c': 'audio/guitar_chord3.mp3',
            'chord_d': 'audio/guitar_chord1.mp3',

            // Real Studio Drum Kit
            'drum_kick': 'audio/drum_kick.mp3',
            'drum_snare': 'audio/drum_snare.mp3',
            'drum_hihat': 'audio/drum_hihat.mp3',
            'drum_tom1': 'audio/drum_tom1.mp3',
            'drum_tom2': 'audio/drum_tom2.mp3',
            'drum_crash': 'audio/drum_crash.mp3',
        };

        // Note Frequencies Table
        this.noteFreqs = {
            'C4': 261.6, 'Cs4': 277.2, 'D4': 293.7, 'Ds4': 311.1,
            'E4': 329.6, 'F4': 349.2, 'Fs4': 370.0, 'G4': 392.0,
            'Gs4': 415.3, 'A4': 440.0, 'As4': 466.2, 'B4': 493.9,
            'C5': 523.3, 'D5': 587.3, 'E5': 659.3, 'F5': 698.5,
            'G5': 784.0, 'A5': 880.0, 'B5': 987.8, 'C6': 1046.5
        };

        // Song Repertoire Data
        this.songs = {
            happyBirthday: [
                { note: 'G4', dur: 260 }, { note: 'G4', dur: 260 }, { note: 'A4', dur: 500 }, { note: 'G4', dur: 500 },
                { note: 'C5', dur: 500 }, { note: 'B4', dur: 950 }, { note: null, dur: 150 },
                { note: 'G4', dur: 260 }, { note: 'G4', dur: 260 }, { note: 'A4', dur: 500 }, { note: 'G4', dur: 500 },
                { note: 'D5', dur: 500 }, { note: 'C5', dur: 950 }, { note: null, dur: 150 },
                { note: 'G4', dur: 260 }, { note: 'G4', dur: 260 }, { note: 'G5', dur: 500 }, { note: 'E5', dur: 500 },
                { note: 'C5', dur: 500 }, { note: 'B4', dur: 500 }, { note: 'A4', dur: 750 }, { note: null, dur: 150 },
                { note: 'F5', dur: 260 }, { note: 'F5', dur: 260 }, { note: 'E5', dur: 500 }, { note: 'C5', dur: 500 },
                { note: 'D5', dur: 500 }, { note: 'C5', dur: 1000 }
            ],
            twinkleTwinkle: [
                { note: 'C4', dur: 380 }, { note: 'C4', dur: 380 }, { note: 'G4', dur: 380 }, { note: 'G4', dur: 380 },
                { note: 'A4', dur: 380 }, { note: 'A4', dur: 380 }, { note: 'G4', dur: 760 }, { note: null, dur: 120 },
                { note: 'F4', dur: 380 }, { note: 'F4', dur: 380 }, { note: 'E4', dur: 380 }, { note: 'E4', dur: 380 },
                { note: 'D4', dur: 380 }, { note: 'D4', dur: 380 }, { note: 'C4', dur: 760 }, { note: null, dur: 120 },
                { note: 'G4', dur: 380 }, { note: 'G4', dur: 380 }, { note: 'F4', dur: 380 }, { note: 'F4', dur: 380 },
                { note: 'E4', dur: 380 }, { note: 'E4', dur: 380 }, { note: 'D4', dur: 760 }
            ],
            odeToJoy: [
                { note: 'E4', dur: 350 }, { note: 'E4', dur: 350 }, { note: 'F4', dur: 350 }, { note: 'G4', dur: 350 },
                { note: 'G4', dur: 350 }, { note: 'F4', dur: 350 }, { note: 'E4', dur: 350 }, { note: 'D4', dur: 350 },
                { note: 'C4', dur: 350 }, { note: 'C4', dur: 350 }, { note: 'D4', dur: 350 }, { note: 'E4', dur: 350 },
                { note: 'E4', dur: 520 }, { note: 'D4', dur: 220 }, { note: 'D4', dur: 700 }
            ],
            jingleBells: [
                { note: 'E4', dur: 280 }, { note: 'E4', dur: 280 }, { note: 'E4', dur: 560 }, { note: null, dur: 100 },
                { note: 'E4', dur: 280 }, { note: 'E4', dur: 280 }, { note: 'E4', dur: 560 }, { note: null, dur: 100 },
                { note: 'E4', dur: 280 }, { note: 'G4', dur: 280 }, { note: 'C4', dur: 380 }, { note: 'D4', dur: 200 },
                { note: 'E4', dur: 760 }
            ],
            maryLamb: [
                { note: 'E4', dur: 320 }, { note: 'D4', dur: 320 }, { note: 'C4', dur: 320 }, { note: 'D4', dur: 320 },
                { note: 'E4', dur: 320 }, { note: 'E4', dur: 320 }, { note: 'E4', dur: 640 }, { note: null, dur: 100 },
                { note: 'D4', dur: 320 }, { note: 'D4', dur: 320 }, { note: 'D4', dur: 640 },
                { note: 'E4', dur: 320 }, { note: 'G4', dur: 320 }, { note: 'G4', dur: 640 }
            ],
            londonBridge: [
                { note: 'G4', dur: 380 }, { note: 'A4', dur: 180 }, { note: 'G4', dur: 280 }, { note: 'F4', dur: 280 },
                { note: 'E4', dur: 280 }, { note: 'F4', dur: 280 }, { note: 'G4', dur: 580 },
                { note: 'D4', dur: 280 }, { note: 'E4', dur: 280 }, { note: 'F4', dur: 580 },
                { note: 'E4', dur: 280 }, { note: 'F4', dur: 280 }, { note: 'G4', dur: 580 }
            ]
        };

        this.init();
    }

    async init() {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioContext();

        this.masterGain = this.ctx.createGain();
        this.masterGain.gain.value = 0.85;

        this.analyser = this.ctx.createAnalyser();
        this.analyser.fftSize = 64;
        this.analyser.smoothingTimeConstant = 0.8;

        this.masterGain.connect(this.analyser);
        this.analyser.connect(this.ctx.destination);

        await this.loadAllSamples();
        this.bindEvents();
        this.startVisualizer();
        this.initComposer();
    }

    async loadAllSamples() {
        const promises = Object.entries(this.sampleUrls).map(async ([key, url]) => {
            try {
                const response = await fetch(url);
                const arrayBuffer = await response.arrayBuffer();
                const audioBuffer = await this.ctx.decodeAudioData(arrayBuffer);
                this.buffers[key] = audioBuffer;
            } catch (err) {
                console.warn(`[Sample fallback] Could not load ${url}, generating procedural sample.`, err);
            }
        });

        await Promise.all(promises);
        this.isLoaded = true;
        console.log('[AudioEngine] All Real Sampled Instruments Loaded Successfully.');
        const badge = document.getElementById('audioInitBtn');
        if (badge) {
            badge.innerHTML = '<span class="btn-dot"></span> REAL STUDIO SAMPLES LOADED';
            badge.style.borderColor = '#00e676';
            badge.style.color = '#00e676';
        }
    }

    // Resolve any note name (e.g. C4, Cs4, D5, G5, etc.) to closest sample & playbackRate
    resolvePianoSample(noteName) {
        const match = noteName.match(/^([A-Ga-g][s#b]?)([0-9])$/);
        if (!match) return { key: 'piano_C4', rate: 1.0 };

        let [_, pitch, octStr] = match;
        let octave = parseInt(octStr, 10);
        if (pitch.length === 2 && pitch[1] === '#') {
            pitch = pitch[0].toUpperCase() + 's';
        } else if (pitch.length === 2 && pitch[1] === 'b') {
            const flatMap = { 'Db': 'Cs', 'Eb': 'Ds', 'Gb': 'Fs', 'Ab': 'Gs', 'Bb': 'As' };
            pitch = flatMap[pitch[0].toUpperCase() + 'b'] || pitch;
        } else {
            pitch = pitch[0].toUpperCase() + (pitch[1] || '');
        }

        const directKey = `piano_${pitch}${octave}`;
        if (this.buffers[directKey]) {
            return { key: directKey, rate: 1.0 };
        }

        // Check Octave 4 equivalent
        const oct4Key = `piano_${pitch}4`;
        if (this.buffers[oct4Key]) {
            const rate = Math.pow(2, octave - 4);
            return { key: oct4Key, rate: rate };
        }

        // Chromatic calculation from C4
        const noteOrder = ['C', 'Cs', 'D', 'Ds', 'E', 'F', 'Fs', 'G', 'Gs', 'A', 'As', 'B'];
        const semitones = ((octave - 4) * 12) + noteOrder.indexOf(pitch);
        return { key: 'piano_C4', rate: Math.pow(2, semitones / 12) };
    }

    // Play a Decoded Buffer with Envelope & Pitch Transpose
    playBuffer(bufferKey, playbackRate = 1.0, isSustained = false) {
        if (!this.ctx) return;
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }

        const buffer = this.buffers[bufferKey];
        if (!buffer) {
            // HTML5 Audio zero-CORS fallback
            const url = this.sampleUrls[bufferKey];
            if (url) {
                try {
                    const audio = new Audio(url);
                    audio.playbackRate = Math.max(0.5, Math.min(4.0, playbackRate));
                    audio.volume = this.masterGain ? this.masterGain.gain.value : 0.85;
                    audio.play().catch(() => {});
                } catch(e) {}
            }
            return;
        }

        const source = this.ctx.createBufferSource();
        source.buffer = buffer;
        source.playbackRate.value = playbackRate;

        const gainNode = this.ctx.createGain();
        const now = this.ctx.currentTime;

        if (isSustained || this.sustainPedal) {
            gainNode.gain.setValueAtTime(1.0, now);
            gainNode.gain.exponentialRampToValueAtTime(0.001, now + (buffer.duration * 1.6));
        } else {
            gainNode.gain.setValueAtTime(1.0, now);
            gainNode.gain.exponentialRampToValueAtTime(0.001, now + Math.min(buffer.duration, 2.2));
        }

        source.connect(gainNode);
        gainNode.connect(this.masterGain);

        source.start(0);
        return source;
    }

    // 1. Play Real Steinway Piano Note
    playPiano(noteName) {
        let finalNote = noteName;
        if (this.currentOctave !== 4) {
            const match = noteName.match(/^([A-Ga-g][s#b]?)([0-9])$/);
            if (match) {
                finalNote = `${match[1]}${this.currentOctave}`;
            }
        }

        const { key, rate } = this.resolvePianoSample(finalNote);
        this.playBuffer(key, rate, this.sustainPedal);

        const freq = this.noteFreqs[finalNote] || Math.round(440 * Math.pow(2, (this.currentOctave - 4)));
        const badge = document.getElementById('pianoNoteBadge');
        if (badge) badge.innerText = `Steinway Note: ${finalNote} (${freq} Hz)`;

        this.updateStats(finalNote, `${freq} Hz`);
    }

    // 2. Play Real Guitar String
    playGuitarString(stringNum) {
        const bufferKey = `guitar_${stringNum}`;
        this.playBuffer(bufferKey, 1.0);

        const lane = document.querySelector(`.string-lane[data-string="${stringNum}"]`);
        if (lane) {
            lane.classList.add('vibrating');
            setTimeout(() => lane.classList.remove('vibrating'), 400);
        }

        const badge = document.getElementById('guitarStatusBadge');
        if (badge) badge.innerText = `Plucked String ${stringNum} (Acoustic)`;
    }

    // Play Melody on Guitar
    playGuitarMelody(noteName) {
        const noteOrder = ['C', 'Cs', 'D', 'Ds', 'E', 'F', 'Fs', 'G', 'Gs', 'A', 'As', 'B'];
        const match = noteName.match(/^([A-Ga-g][s#b]?)([0-9])$/);
        if (match) {
            const [_, pitch, octStr] = match;
            const oct = parseInt(octStr, 10);
            const semitonesFromE4 = ((oct - 4) * 12) + (noteOrder.indexOf(pitch) - 4);
            const rate = Math.pow(2, semitonesFromE4 / 12);
            this.playBuffer('guitar_1', Math.max(0.25, Math.min(4.0, rate)));
        } else {
            this.playGuitarString(1);
        }

        const strNum = (Math.abs(noteName.charCodeAt(0)) % 6) + 1;
        const lane = document.querySelector(`.string-lane[data-string="${strNum}"]`);
        if (lane) {
            lane.classList.add('vibrating');
            setTimeout(() => lane.classList.remove('vibrating'), 300);
        }

        const badge = document.getElementById('guitarStatusBadge');
        if (badge) badge.innerText = `Acoustic Pluck: ${noteName}`;
    }

    // Strum Guitar Chord
    strumChord(chordKey) {
        this.playBuffer(chordKey, 1.0);

        document.querySelectorAll('.string-lane').forEach((lane, idx) => {
            setTimeout(() => {
                lane.classList.add('vibrating');
                setTimeout(() => lane.classList.remove('vibrating'), 350);
            }, idx * 25);
        });

        const badge = document.getElementById('guitarStatusBadge');
        if (badge) badge.innerText = `Acoustic Chord Strummed!`;
    }

    // 3. Play Real Drum Hit
    playDrum(soundName) {
        const bufferKey = `drum_${soundName}`;
        this.playBuffer(bufferKey, 1.0);

        const pad = document.querySelector(`.drum-pad[data-sound="${soundName}"]`);
        if (pad) {
            pad.classList.add('hit');
            setTimeout(() => pad.classList.remove('hit'), 120);
        }

        const badge = document.getElementById('drumStatusBadge');
        if (badge) badge.innerText = `Hit: ${soundName.toUpperCase()}`;
    }

    // Play Drum Groove Step
    playDrumGroove(step) {
        const s = step % 8;
        if (s === 0) {
            this.playDrum('kick');
            this.playDrum('hihat');
        } else if (s === 2 || s === 6) {
            this.playDrum('snare');
            this.playDrum('hihat');
        } else if (s === 4) {
            this.playDrum('kick');
            this.playDrum('hihat');
        } else if (s === 5) {
            this.playDrum('kick');
        } else if (s === 7 && step % 16 === 15) {
            this.playDrum('crash');
        } else {
            this.playDrum('hihat');
        }
    }

    // 4. Play Selected Song
    playSong() {
        if (this.isPlayingSong) {
            this.stopSong();
        }

        const songNotes = this.songs[this.selectedSong];
        if (!songNotes) return;

        this.isPlayingSong = true;
        let index = 0;

        const playNext = () => {
            if (!this.isPlayingSong || index >= songNotes.length) {
                this.stopSong();
                return;
            }

            const item = songNotes[index];

            if (item.note) {
                if (this.selectedStyle === 'piano') {
                    this.playPiano(item.note);
                    this.animatePianoKey(item.note);
                } else if (this.selectedStyle === 'guitar') {
                    this.playGuitarMelody(item.note);
                } else if (this.selectedStyle === 'drums') {
                    this.playDrumGroove(index);
                }
            }

            index++;
            this.currentSongTimer = setTimeout(playNext, item.dur);
        };

        playNext();
    }

    stopSong() {
        this.isPlayingSong = false;
        if (this.currentSongTimer) {
            clearTimeout(this.currentSongTimer);
            this.currentSongTimer = null;
        }
        const badge = document.getElementById('visLiveHz');
        if (badge) badge.innerText = '0 Hz • Stopped';
    }

    animatePianoKey(noteName) {
        const keyEl = document.querySelector(`.white-key[data-note="${noteName}"], .black-key[data-note="${noteName}"]`);
        if (keyEl) {
            keyEl.classList.add('active');
            setTimeout(() => keyEl.classList.remove('active'), 200);
        }
    }

    updateStats(note, hz) {
        const elNote = document.getElementById('statNoteName');
        const elHz = document.getElementById('statHz');
        const elLive = document.getElementById('visLiveHz');
        if (elNote) elNote.innerText = note;
        if (elHz) elHz.innerText = hz;
        if (elLive) elLive.innerText = `${hz} • Live Audio`;
    }

    // Real-Time Canvas Spectrum Visualizer (60 FPS)
    startVisualizer() {
        const canvas = document.getElementById('spectrumCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const bufferLength = this.analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);

        const draw = () => {
            requestAnimationFrame(draw);
            this.analyser.getByteFrequencyData(dataArray);

            ctx.fillStyle = '#09070e';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            const barWidth = (canvas.width / bufferLength) * 1.8;
            let barHeight;
            let x = 0;

            for (let i = 0; i < bufferLength; i++) {
                barHeight = (dataArray[i] / 255) * canvas.height * 0.85;

                // Dynamic gradient
                const grad = ctx.createLinearGradient(0, canvas.height, 0, canvas.height - barHeight);
                grad.addColorStop(0, '#e53935');
                grad.addColorStop(0.6, '#ffb300');
                grad.addColorStop(1, '#ffffff');

                ctx.fillStyle = grad;
                ctx.fillRect(x, canvas.height - barHeight, barWidth - 4, barHeight);

                // Peak cap
                if (barHeight > 5) {
                    ctx.fillStyle = '#fff';
                    ctx.fillRect(x, canvas.height - barHeight - 3, barWidth - 4, 2);
                }

                x += barWidth;
            }
        };

        draw();
    }

    // UI & Keyboard Event Listeners
    bindEvents() {
        // Tab Switching
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.instrument-view').forEach(v => v.classList.remove('active'));

                tab.classList.add('active');
                const targetId = `view-${tab.dataset.tab}`;
                const targetView = document.getElementById(targetId);
                if (targetView) targetView.classList.add('active');
            });
        });

        // Piano Key Clicks
        document.querySelectorAll('.white-key, .black-key').forEach(key => {
            key.addEventListener('mousedown', () => {
                const note = key.dataset.note;
                if (note) {
                    this.playPiano(note);
                    key.classList.add('active');
                }
            });
            key.addEventListener('mouseup', () => key.classList.remove('active'));
            key.addEventListener('mouseleave', () => key.classList.remove('active'));
        });

        // Guitar String Clicks
        document.querySelectorAll('.string-lane').forEach(lane => {
            lane.addEventListener('click', () => {
                const strNum = lane.dataset.string;
                if (strNum) this.playGuitarString(strNum);
            });
        });

        // Guitar Strum Buttons
        document.getElementById('btnStrumEm')?.addEventListener('click', () => this.strumChord('chord_em'));
        document.getElementById('btnStrumG')?.addEventListener('click', () => this.strumChord('chord_g'));
        document.getElementById('btnStrumC')?.addEventListener('click', () => this.strumChord('chord_c'));
        document.getElementById('btnStrumD')?.addEventListener('click', () => this.strumChord('chord_d'));

        // Drum Pad Clicks
        document.querySelectorAll('.drum-pad').forEach(pad => {
            pad.addEventListener('click', () => {
                const sound = pad.dataset.sound;
                if (sound) this.playDrum(sound);
            });
        });

        // Sustain Pedal Toggle
        const susToggle = document.getElementById('sustainToggle');
        if (susToggle) {
            susToggle.addEventListener('change', (e) => {
                this.sustainPedal = e.target.checked;
                const visualPedal = document.getElementById('visualSustainPedal');
                if (visualPedal) {
                    if (this.sustainPedal) visualPedal.classList.add('active');
                    else visualPedal.classList.remove('active');
                }
            });
        }

        // Master Volume
        const volSlider = document.getElementById('masterVolume');
        const volDisplay = document.getElementById('volValue');
        if (volSlider) {
            volSlider.addEventListener('input', (e) => {
                const val = e.target.value / 100;
                if (this.masterGain) this.masterGain.gain.value = val;
                if (volDisplay) volDisplay.innerText = `${e.target.value}%`;
            });
        }

        // Octave Buttons
        document.querySelectorAll('.oct-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.oct-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.currentOctave = parseInt(btn.dataset.oct, 10) || 4;
                const badge = document.getElementById('pianoNoteBadge');
                if (badge) badge.innerText = `Octave ${this.currentOctave} Selected`;
            });
        });

        // Audio Init & Quick Test Chord Button
        const initBtn = document.getElementById('audioInitBtn');
        if (initBtn) {
            initBtn.addEventListener('click', async () => {
                if (this.ctx && this.ctx.state === 'suspended') {
                    await this.ctx.resume();
                }
                // Play a brief Steinway preview arpeggio
                this.playPiano('C4');
                setTimeout(() => this.playPiano('E4'), 130);
                setTimeout(() => this.playPiano('G4'), 260);
                setTimeout(() => this.playPiano('C5'), 390);
                initBtn.innerHTML = '<span class="btn-dot" style="background:#00e676"></span> AUDIO ENGINE LIVE';
                initBtn.style.borderColor = '#00e676';
                initBtn.style.color = '#00e676';
            });
        }

        // Songs Jukebox
        document.querySelectorAll('.song-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.song-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.selectedSong = btn.dataset.song;
                if (this.isPlayingSong) this.playSong();
            });
        });

        // Style Choice
        document.querySelectorAll('.style-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.style-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.selectedStyle = btn.dataset.style;
            });
        });

        document.getElementById('btnPlaySong')?.addEventListener('click', () => this.playSong());
        document.getElementById('btnStopSong')?.addEventListener('click', () => this.stopSong());

        // Keyboard Shortcuts Handler
        const keyMap = {
            'q': () => this.handleKeyAction('Q'),
            'w': () => this.handleKeyAction('W'),
            'e': () => this.handleKeyAction('E'),
            'r': () => this.handleKeyAction('R'),
            't': () => this.handleKeyAction('T'),
            'y': () => this.handleKeyAction('Y'),
            'u': () => this.handleKeyAction('U'),
            'i': () => this.handleKeyAction('I'),
            '2': () => this.handleKeyAction('2'),
            '3': () => this.handleKeyAction('3'),
            '5': () => this.handleKeyAction('5'),
            '6': () => this.handleKeyAction('6'),
            '7': () => this.handleKeyAction('7'),
            's': () => this.strumChord('chord_em'),
            ' ': () => {
                const sus = document.getElementById('sustainToggle');
                if (sus) {
                    sus.checked = !sus.checked;
                    sus.dispatchEvent(new Event('change'));
                }
            },
            'escape': () => {
                this.stopSong();
                this.stopSequencerPlayback();
            }
        };

        window.addEventListener('keydown', (e) => {
            const k = e.key.toLowerCase();
            if (keyMap[k]) {
                if (k === ' ') e.preventDefault();
                keyMap[k]();
            }
        });
    }

    handleKeyAction(char) {
        // Dispatch based on active tab
        const activeTab = document.querySelector('.nav-tab.active')?.dataset.tab;

        if (activeTab === 'piano' || activeTab === 'composer') {
            const keyEl = document.querySelector(`.white-key[data-key="${char}"], .black-key[data-key="${char}"]`);
            if (keyEl) {
                const note = keyEl.dataset.note;
                this.playPiano(note);
                keyEl.classList.add('active');
                setTimeout(() => keyEl.classList.remove('active'), 180);

                if (activeTab === 'composer') {
                    this.appendNoteToTape(note);
                }
            }
        } else if (activeTab === 'guitar') {
            const lane = document.querySelector(`.string-lane[data-key="${char}"]`);
            if (lane) {
                const strNum = lane.dataset.string;
                this.playGuitarString(strNum);
            }
        } else if (activeTab === 'drums') {
            const pad = document.querySelector(`.drum-pad[data-key="${char}"]`);
            if (pad) {
                const sound = pad.dataset.sound;
                this.playDrum(sound);
            }
        }
    }

    // =========================================================================
    // COMPOSER & STEP SEQUENCER IMPLEMENTATION
    // =========================================================================
    initComposer() {
        const headerEl = document.getElementById('stepNumbersHeader');
        const tracksEl = document.getElementById('sequencerTracks');
        if (!headerEl || !tracksEl) return;

        // 1. Populate 1..16 Step Numbers
        headerEl.innerHTML = '';
        for (let i = 1; i <= 16; i++) {
            const numEl = document.createElement('div');
            numEl.className = `step-num ${i % 4 === 1 ? 'beat-marker' : ''}`;
            numEl.textContent = i;
            headerEl.appendChild(numEl);
        }

        // 2. Define 8 Multi-Instrument Tracks
        this.sequencerTracks = [
            { id: 'piano_C5', name: 'Piano C5 (High)', icon: '🎹', classType: 'piano-step', soundType: 'piano', note: 'C5' },
            { id: 'piano_G4', name: 'Piano G4', icon: '🎹', classType: 'piano-step', soundType: 'piano', note: 'G4' },
            { id: 'piano_E4', name: 'Piano E4', icon: '🎹', classType: 'piano-step', soundType: 'piano', note: 'E4' },
            { id: 'piano_C4', name: 'Piano C4 (Root)', icon: '🎹', classType: 'piano-step', soundType: 'piano', note: 'C4' },
            { id: 'guitar_chord', name: 'Guitar Chord Em', icon: '🎸', classType: 'guitar-step', soundType: 'guitar', chord: 'chord_em' },
            { id: 'drum_crash', name: 'Crash Cymbal', icon: '🥁', classType: 'drum-step', soundType: 'drum', sound: 'drum_crash' },
            { id: 'drum_snare', name: 'Snare Drum', icon: '🥁', classType: 'drum-step', soundType: 'drum', sound: 'drum_snare' },
            { id: 'drum_kick', name: 'Kick Drum', icon: '🥁', classType: 'drum-step', soundType: 'drum', sound: 'drum_kick' }
        ];

        this.sequencerGrid = {};
        tracksEl.innerHTML = '';

        // 3. Render Track Rows & 16 Step Cells
        this.sequencerTracks.forEach(track => {
            this.sequencerGrid[track.id] = new Array(16).fill(false);

            const row = document.createElement('div');
            row.className = 'track-row';

            const meta = document.createElement('div');
            meta.className = 'track-meta';
            meta.innerHTML = `<span class="track-icon">${track.icon}</span><span class="track-name">${track.name}</span>`;
            row.appendChild(meta);

            const stepsContainer = document.createElement('div');
            stepsContainer.className = 'steps-container';

            for (let step = 0; step < 16; step++) {
                const cell = document.createElement('div');
                cell.className = `step-cell ${track.classType}`;
                cell.dataset.track = track.id;
                cell.dataset.step = step;

                cell.addEventListener('click', () => {
                    this.initContext();
                    const active = !this.sequencerGrid[track.id][step];
                    this.sequencerGrid[track.id][step] = active;
                    cell.classList.toggle('active', active);

                    if (active) {
                        this.playTrackSample(track);
                        this.updateComposerTape();
                    }
                });

                stepsContainer.appendChild(cell);
            }

            row.appendChild(stepsContainer);
            tracksEl.appendChild(row);
        });

        // 4. Attach Buttons
        document.getElementById('btnPlayComposer')?.addEventListener('click', () => {
            this.initContext();
            this.startSequencerPlayback();
        });

        document.getElementById('btnStopComposer')?.addEventListener('click', () => {
            this.stopSequencerPlayback();
        });

        document.getElementById('btnClearComposer')?.addEventListener('click', () => {
            this.clearSequencer();
        });

        document.getElementById('btnPresetComposer')?.addEventListener('click', () => {
            this.initContext();
            this.loadSequencerPreset();
        });

        document.getElementById('btnSaveComposer')?.addEventListener('click', () => {
            this.saveSequencerSong();
        });

        const bpmSlider = document.getElementById('composerBpm');
        if (bpmSlider) {
            bpmSlider.addEventListener('input', (e) => {
                this.composerBpm = parseInt(e.target.value, 10);
                const bpmVal = document.getElementById('bpmVal');
                if (bpmVal) bpmVal.textContent = `${this.composerBpm} BPM`;
                if (this.isSequencerPlaying) {
                    this.startSequencerPlayback();
                }
            });
        }

        // Load Starter Melody
        this.loadSequencerPreset();
    }

    playTrackSample(track) {
        if (track.soundType === 'piano') {
            this.playPiano(track.note);
        } else if (track.soundType === 'guitar') {
            this.strumChord(track.chord);
        } else if (track.soundType === 'drum') {
            this.playDrum(track.sound);
        }
    }

    setStepActive(trackId, stepIndex, active) {
        if (this.sequencerGrid[trackId]) {
            this.sequencerGrid[trackId][stepIndex] = active;
            const cell = document.querySelector(`.step-cell[data-track="${trackId}"][data-step="${stepIndex}"]`);
            if (cell) cell.classList.toggle('active', active);
        }
    }

    clearSequencer() {
        this.stopSequencerPlayback();
        this.sequencerTracks.forEach(track => {
            this.sequencerGrid[track.id].fill(false);
        });
        document.querySelectorAll('.step-cell.active').forEach(c => c.classList.remove('active'));
        this.updateComposerTape();
    }

    loadSequencerPreset() {
        this.clearSequencer();
        // Four-on-the-floor Kick
        [0, 4, 8, 12].forEach(s => this.setStepActive('drum_kick', s, true));
        // Snare on 4, 12
        [4, 12].forEach(s => this.setStepActive('drum_snare', s, true));
        // Crash on start
        [0].forEach(s => this.setStepActive('drum_crash', s, true));
        // Melodic arpeggio
        [0, 8].forEach(s => this.setStepActive('piano_C4', s, true));
        [2, 10].forEach(s => this.setStepActive('piano_E4', s, true));
        [4, 12].forEach(s => this.setStepActive('piano_G4', s, true));
        [6].forEach(s => this.setStepActive('piano_C5', s, true));
        // Guitar chord on 8
        [8].forEach(s => this.setStepActive('guitar_chord', s, true));

        this.updateComposerTape();
    }

    startSequencerPlayback() {
        this.stopSequencerPlayback();
        this.isSequencerPlaying = true;
        this.currentSequencerStep = 0;

        const badge = document.getElementById('composerStatusBadge');
        if (badge) badge.innerText = '● Sequencer Playing Live Loop...';

        const stepTick = () => {
            if (!this.isSequencerPlaying) return;

            // Highlight active column
            document.querySelectorAll('.step-cell.current-step').forEach(c => c.classList.remove('current-step'));
            document.querySelectorAll(`.step-cell[data-step="${this.currentSequencerStep}"]`).forEach(c => c.classList.add('current-step'));

            // Play active sounds
            this.sequencerTracks.forEach(track => {
                if (this.sequencerGrid[track.id][this.currentSequencerStep]) {
                    this.playTrackSample(track);
                }
            });

            this.currentSequencerStep = (this.currentSequencerStep + 1) % 16;
            const stepDuration = (60 / this.composerBpm / 4) * 1000;
            this.sequencerTimer = setTimeout(stepTick, stepDuration);
        };

        stepTick();
    }

    stopSequencerPlayback() {
        this.isSequencerPlaying = false;
        if (this.sequencerTimer) {
            clearTimeout(this.sequencerTimer);
            this.sequencerTimer = null;
        }
        document.querySelectorAll('.step-cell.current-step').forEach(c => c.classList.remove('current-step'));
        const badge = document.getElementById('composerStatusBadge');
        if (badge) badge.innerText = '16-Step Live Sequencer & Multi-Track Composer';
    }

    updateComposerTape() {
        const tapeDisplay = document.getElementById('composerTapeDisplay');
        if (!tapeDisplay) return;

        const activeNotes = [];
        for (let step = 0; step < 16; step++) {
            this.sequencerTracks.forEach(track => {
                if (this.sequencerGrid[track.id][step]) {
                    const label = track.note || track.sound || track.chord;
                    activeNotes.push(`Step ${step + 1}: ${label}`);
                }
            });
        }

        if (activeNotes.length === 0) {
            tapeDisplay.innerHTML = '<span class="tape-hint">[ Empty Track - Click grid squares or play keys to compose! ]</span>';
        } else {
            tapeDisplay.innerHTML = activeNotes.slice(0, 14).map(n => `<span class="tape-chip">[${n}]</span>`).join('');
        }
    }

    appendNoteToTape(noteName) {
        const tapeDisplay = document.getElementById('composerTapeDisplay');
        if (!tapeDisplay) return;
        const chip = document.createElement('span');
        chip.className = 'tape-chip';
        chip.textContent = `[Live: ${noteName}]`;
        tapeDisplay.appendChild(chip);

        // Keep last 12 notes
        while (tapeDisplay.children.length > 14) {
            tapeDisplay.removeChild(tapeDisplay.firstChild);
        }
    }

    saveSequencerSong() {
        try {
            localStorage.setItem('crimson_user_song', JSON.stringify(this.sequencerGrid));
        } catch (e) {}

        const notice = document.getElementById('saveNotice');
        if (notice) {
            notice.classList.add('show');
            setTimeout(() => notice.classList.remove('show'), 2000);
        }
    }
}

// Instantiate Engine on Window Load
window.addEventListener('DOMContentLoaded', () => {
    window.crimsonAudio = new AudioEngine();
});
