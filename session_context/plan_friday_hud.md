# Implementation Plan: F.R.I.D.A.Y. "Living" Desktop HUD

## Goal Description
You requested a dedicated, "living" graphical interface for F.R.I.D.A.Y. that you can place on any of your four monitors. It must feature visual feedback when you or F.R.I.D.A.Y. speaks (like an orb or connecting dots), a lightweight avatar, and system widgets. Most importantly, it must have **extremely low GPU usage** (CPU-driven) to ensure all GPU VRAM and compute is strictly reserved for running local AI models.

## Proposed Technology Stack (CPU-First Design)
Instead of using a web-based UI (like Electron) which spawns heavy Chromium processes, or a 3D engine (Unity/Unreal), I propose building this using **PyQt6** and native 2D QPainter rendering. 
- **Graphics**: `QPainter` uses CPU rasterization. Drawing an audio-reactive orb or connecting dots costs essentially 0% GPU and <1% CPU.
- **Audio Reactivity**: We will use the `sounddevice` and `numpy` libraries to run a background thread that captures the RMS (Root Mean Square) volume of your microphone in real-time, mapping that volume directly to the size and glow of the orb.
- **Windowing**: The app will be "frameless" (no Windows title bar), giving it a sleek, holographic widget feel on your desktop.

## User Review Required
> [!IMPORTANT]
> **Dependency Additions:** This requires installing `PyQt6`, `sounddevice`, and `numpy`. Are you okay with adding these libraries to the environment?
> 
> **Avatar Design:** The "avatar" will be a central digital orb that shifts between "listening" (dots reacting to your mic) and "speaking" (pulsing to F.R.I.D.A.Y.'s TTS output). If you have a specific static image you want for the avatar, let me know, otherwise, I will create a minimalist, high-tech geometric orb.

## Proposed Changes

### 1. New Dependencies
#### [MODIFY] requirements.txt
```text
PyQt6
sounddevice
numpy
```

### 2. Audio Processing Engine
#### [NEW] `friday_engine/senses/audio_monitor.py`
A lightweight background thread that safely samples the default microphone in 50ms chunks without blocking the main engine, emitting the volume amplitude to the UI.

### 3. The Visual HUD
#### [NEW] `friday_engine/gui/hud.py`
Will contain the main PyQt6 Application:
*   **`FridayHUD (QMainWindow)`**: Frameless, dark-themed, draggable window.
*   **`OrbVisualizer (QWidget)`**: A custom widget overriding `paintEvent`. It will draw connecting dots or concentric circles. It subscribes to the `AudioMonitor` and redraws at 30 FPS based on the volume level.
*   **`StatusWidgets (QDockWidget)`**: Side panels displaying:
    *   Current Global Goal / Active Task
    *   Sub-agent Status (Idle, Coding, Researching)
    *   Local Model RAM/VRAM usage

### 4. Core Engine Integration
#### [MODIFY] `friday_engine/core/engine.py`
Add a command or startup flag to launch the PyQt6 HUD in a separate multiprocessing process or thread so it doesn't block the asynchronous LLM ReAct loop.

## Verification Plan

### Automated Tests
*   Ensure `import PyQt6` resolves correctly.
*   Test `audio_monitor.py` to ensure it successfully captures microphone hardware levels without crashing or blocking.

### Manual Verification
1.  Run the HUD script.
2.  Drag the frameless window to a secondary monitor.
3.  Speak into the microphone and visually verify that the geometric orb expands/reacts to voice amplitude in real-time with zero latency.
4.  Check Task Manager to verify GPU usage is at 0% and CPU usage is minimal.
