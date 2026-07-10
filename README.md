# Gesture Mouse Control  
**AI-Inspired Gesture-Based Mouse Control using Computer Vision**

Control your computer’s mouse using natural hand gestures in real time, no hardware beyond a webcam required.

This project explores **gesture-based human–computer interaction (HCI)** by translating hand movements into full OS-level mouse control, including cursor movement, clicking, dragging, scrolling, and adaptive precision control.

Built entirely in **Python** using **computer vision and intelligent intent detection**.

## Features

### Core Controls
- 👉 **Index finger** — Move cursor
- 🤏 **Pinch (tap)** — Left click
- 🤏 **Pinch (hold)** — Drag & drop
- ✌️ **Index + Middle** — Scroll
- ⌨️ **Spacebar** — Pause / Unpause
- ⎋ **ESC** — Exit program

---

### Intelligent Interaction (Advanced)
- **Adaptive cursor speed**
  - Fast hand motion → fast cursor
  - Slow/steady motion → precision control
- **Slowdown zones**
  - Automatic precision near screen edges
- **Gesture confidence scoring**
  - Reduces accidental actions
- **Intent detection with hysteresis**
  - Prevents gesture flickering
  - Chooses the most likely action each frame
- **Virtual FOV expansion**
  - Makes narrow laptop webcams feel wider

---

### Live HUD
- Current intent (MOVE / SCROLL / CLICK / DRAG / IDLE)
- Gesture confidence bar
- FPS (performance monitoring)
- Pinch distance
- Adaptive gain & velocity diagnostics

---

## Tech Stack

| Technology | Purpose |
|----------|--------|
| **Python** | Core application logic |
| **OpenCV** | Webcam input & visualization |
| **MediaPipe Hands** | Real-time hand landmark tracking (21 points) |
| **PyAutoGUI** | OS-level mouse control |
| **Math / Geometry (Python)** | Gesture detection, smoothing, and velocity calculations |
| **HCI Principles** | Adaptive speed, confidence, intent modeling |

---

## How It Works (High Level)

1. Webcam feed captured using OpenCV  
2. MediaPipe detects and tracks hand landmarks in real time  
3. Landmarks are analyzed to compute:
   - Finger states
   - Pinch distance
   - Hand velocity
4. A confidence-based intent system selects the most likely gesture
5. Cursor movement uses:
   - Smoothing
   - Adaptive gain
   - Edge slowdown zones
6. PyAutoGUI sends mouse events to the OS

---

## Hardware Notes
- Works with built-in laptop webcams (tested on ROG Zephyrus G14)
- No GPU required
- Higher camera resolution (720p) improves tracking stability

---

## Current Capabilities
- Full mouse replacement
- Real-time performance (~30–60 FPS)
- Robust against noisy gestures
- Designed for extensibility

---

## Planned Enhancements
- Gesture classifier using machine learning
- Auto-calibration wizard
- Right-click & double-click gestures
- Per-application gesture profiles
- Gesture analytics & heatmaps

---

## Key Things I Learned From Developing This Project
- Computer vision fundamentals
- Real-time system design
- Human–computer interaction principles
- Intelligent input modeling
- Practical OS automation

---
