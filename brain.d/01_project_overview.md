# 📌 01. Project Overview & Mission

## Academic Identity
* **Project Name:** Crimson Orbit – Musical Band & Low-Latency Audio Workstation
* **Institution:** Vishwakarma Institute of Technology (VIT), Pune
* **Department:** Department of Multidisciplinary Engineering / AI & DS
* **Academic Year:** 2025–2026 | Course Project Group 9
* **Faculty Guide:** Prof. Gopal Upadhye
* **Students:** Krishna Aher, Sanskar Bhargude, Ghansham Agaldare, Hari Birare, Akash Kumar

## The Big Idea
To bridge the 40-year gap between **bare-metal 16-bit 8086 Assembly computing** and **modern WebAudio/WebAssembly digital signal processing**.

## Core Problem
Traditional retro computing is trapped in two extremes:
1. **Physical 1-Bit PC Speakers:** Extremely authentic and cycle-accurate, but acoustically limited to harsh, monophonic square waves.
2. **Heavy Monolithic Virtual Machines (v86, DOSBox):** Require >140 MB of RAM, emulate full motherboards, and introduce 60–120ms of audio delay.

## The Crimson Orbit Solution
* A custom 16-bit real-mode assembly kernel running bare-metal on raw hardware with an in-RAM song composer (`composer.asm`).
* A targeted WebAssembly bus-cycle interceptor that traps audio port writes (`OUT 42h`, `OUT 61h`) into a 4-byte micro-packet.
* A modern Web Audio API studio that resynthesizes these pulses into multi-timbral instruments (Steinway Piano, Martin Guitar, Ludwig Drums) with sub-12ms latency.
