# 🖱️ GestureMouse: Production-Grade HCI Engine

**Transform your webcam into a high-performance, gesture-driven trackpad.**

GestureMouse is an advanced Human-Computer Interaction (HCI) engine built in Python. Unlike basic coordinate-mapping scripts, this project utilizes a **Deterministic Finite State Machine (FSM)** and **Adaptive Kinematic Filtering** to provide a native, hardware-level mouse experience without the jitter, false clicks, or dropped drags common in optical tracking.

Built with **MediaPipe Tasks API**, **OpenCV**, and **PyAutoGUI**.

---

## ✨ Engineering Features

* 🧠 **Deterministic Finite State Machine (FSM):** Strict gesture prioritization and temporal debouncing prevent input collisions (e.g., trying to click and scroll simultaneously).
* 🧲 **Schmitt Trigger Hysteresis:** Dual-threshold drag logic requires a tight pinch to *engage* a drag, but allows a relaxed hold to *maintain* it, eliminating dropped windows due to micro-finger twitches.
* 🌊 **Adaptive Kinematic Filtering:** Dynamically calculates hand velocity to apply heavy smoothing when moving slowly (for pixel-perfect precision) and zero smoothing during rapid swipes (to eliminate lag).
* ⚙️ **OS Input Accumulators:** Converts continuous floating-point hand displacements into discrete hardware ticks, ensuring buttery-smooth scrolling (specifically optimized for Linux/Ubuntu environments).
* 🛑 **Hardware Kill-Switch:** Instantly drop all tracking and freeze the cursor by closing your hand into a fist.

---

## ✋ Gesture Command Manual

| Gesture | Posture | Action |
| :--- | :--- | :--- |
| **Navigate** | ☝️ **Index Finger Extended** | Move your hand to drive the cursor. The adaptive filter stabilizes micro-movements automatically. |
| **Click / Drag** | 🤏 **Pinch (Thumb + Index)** | **Click:** Tap thumb and index together quickly.<br>**Drag:** Pinch, hold, and move. Release to drop. |
| **Scroll** | ✌️ **Index + Middle Extended** | Move your hand **up/down** to scroll relatively. Speed correlates to your physical hand velocity. |
| **Drag** | ✊ **Closed Fist** | to move / drag text |

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/utkarsh-raut/GestureMouse.git](https://github.com/utkarsh-raut/GestureMouse.git)
cd GestureMouse
