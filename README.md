# 🖱️ GestureMouse
### Production-Grade Hand Gesture Mouse Controller using Computer Vision

Transform your webcam into a responsive, gesture-controlled mouse powered by modern computer vision and Human-Computer Interaction (HCI) principles.

GestureMouse is a production-oriented Python application that uses the **MediaPipe Tasks API** to detect hand landmarks in real time and convert natural hand gestures into mouse movements, clicks, dragging, and scrolling.

Unlike basic gesture mouse implementations that directly map finger positions to the cursor, GestureMouse introduces a deterministic gesture engine, adaptive motion filtering, and robust state management to create a smooth and reliable desktop experience.

---

# 📌 Features

- 🎯 Real-time hand tracking using MediaPipe Tasks API
- 🖱️ Smooth cursor movement
- 🤏 Single click using pinch gesture
- 📦 Stable click-and-drag support
- 📜 Velocity-based scrolling
- 🧠 Deterministic Finite State Machine (FSM)
- 🌊 Adaptive Kinematic Motion Filtering
- 🧲 Schmitt Trigger Hysteresis
- ⚙️ Floating-point scroll accumulators
- 🛑 Emergency gesture kill switch
- 🖥️ Linux compatible
- 🚀 Lightweight and responsive

---

# 📷 Demo

> *(Add your GIF or screenshot here)*

Example:

```
docs/demo.gif
```

or

```markdown
![Demo](docs/demo.gif)
```

---

# 🚀 Technology Stack

| Technology | Purpose |
|------------|----------|
| Python | Core application |
| OpenCV | Webcam capture & visualization |
| MediaPipe Tasks API | Hand landmark detection |
| NumPy | Mathematical computation |
| PyAutoGUI | Mouse control |
| Virtual Environment | Dependency isolation |

---

# 🏗️ Project Architecture

```
Webcam
   │
   ▼
OpenCV Camera Capture
   │
   ▼
MediaPipe Hand Landmarker
   │
   ▼
Gesture Feature Extraction
   │
   ▼
Deterministic FSM
   │
   ├─────────────► Click
   ├─────────────► Drag
   ├─────────────► Scroll
   └─────────────► Move Cursor
                    │
                    ▼
Adaptive Kinematic Filter
                    │
                    ▼
Linux Mouse Controller
                    │
                    ▼
Operating System Cursor
```

---

# 🧠 Core Engineering Concepts

## 1. Deterministic Finite State Machine (FSM)

GestureMouse is built around a deterministic finite state machine rather than continuously checking gestures independently.

The FSM ensures that only one valid interaction is active at a time.

Benefits:

- Eliminates gesture conflicts
- Prevents accidental clicks
- Prevents click while scrolling
- Prevents drag interruptions
- Stable state transitions
- Temporal debouncing

Example states:

```
Idle

↓

Move

↓

Click

↓

Drag

↓

Scroll

↓

Idle
```

---

## 2. Adaptive Kinematic Filtering

Traditional gesture controllers often suffer from:

- cursor jitter
- lag
- shaky movement

GestureMouse measures hand velocity and dynamically changes smoothing.

Slow movement

↓

Heavy smoothing

↓

Pixel-level precision

Fast movement

↓

Minimal smoothing

↓

Instant response

Benefits

- Smooth precision
- Fast navigation
- No noticeable lag

---

## 3. Schmitt Trigger Hysteresis

Dragging is difficult because tiny finger movement can accidentally release the object.

GestureMouse uses dual thresholds.

Example

```
Pinch Distance

< 25 px

↓

Start Drag


Keep Holding

↓

Drag continues


Release only if

> 40 px
```

This prevents accidental drag cancellation.

---

## 4. Scroll Accumulator

Instead of sending integer scroll events directly,

GestureMouse accumulates floating-point motion.

This produces

- smoother scrolling
- consistent wheel events
- natural feel

Especially optimized for Linux.

---

## 5. Hardware Kill Switch

Closing your hand into a fist immediately:

- freezes cursor
- disables gesture processing
- prevents accidental input

Useful when repositioning your hand.

---

# ✋ Gesture Commands

| Gesture | Action |
|----------|--------|
| ☝️ Index Finger | Cursor Movement |
| 🤏 Thumb + Index Pinch | Left Click |
| 🤏 Hold Pinch | Drag & Drop |
| ✌️ Index + Middle Finger | Vertical Scroll |
| ✊ Closed Fist | drag or to move text |

---

# 📂 Project Structure

```
GestureMouse/

│
├── gesture_mouse.py
├── hand_landmarker.task
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
└── docs/
    ├── screenshots/
    └── demo.gif
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/utkarsh-raut/GestureMouse.git
```

Move inside the project

```bash
cd GestureMouse
```

---

## Create Virtual Environment

```bash
python3 -m venv venv
```

Activate

Linux

```bash
source venv/bin/activate
```

Windows

```cmd
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install opencv-python mediapipe pyautogui numpy
```

or

```bash
pip install -r requirements.txt
```

---

# 📥 Download MediaPipe Model

Download the official MediaPipe Hand Landmarker model.

```bash
wget -q https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
```

Place it in the project root.

Project should look like

```
GestureMouse/

gesture_mouse.py

hand_landmarker.task
```

---

# ▶️ Run

```bash
python3 gesture_mouse.py
```

---

# 🎮 Controls

Move Cursor

```
Index Finger
```

Click

```
Quick Pinch
```

Drag

```
Hold Pinch
```

Scroll

```
Index + Middle Finger
```

Emergency Stop

```
Closed Fist
```

Exit

```
ESC

or

CTRL + C
```

---

# 🧩 Internal Components

## SystemConfig

Stores configurable parameters.

Examples

- camera size
- smoothing constants
- thresholds
- filter settings
- FSM timing

---

## AdaptiveKinematicFilter

Responsible for

- velocity calculation
- exponential moving average
- adaptive smoothing

---

## LinuxMouseController

Handles

- cursor movement
- screen bounds
- scroll accumulation
- click dispatch
- drag operations

---

## GestureFSM

Processes

- finger states
- pinch detection
- scroll mode
- drag mode
- transition rules

Outputs clean user intent.

---

# 💡 Why GestureMouse?

Most open-source gesture mouse projects suffer from:

- Cursor shaking
- False clicks
- Random drags
- Lag
- Gesture conflicts
- Poor user experience

GestureMouse addresses these issues through engineering-focused solutions rather than simple coordinate mapping.

---

# 🔮 Future Improvements

- Multi-monitor support
- Right click gesture
- Volume control
- Brightness control
- Gesture customization
- Virtual keyboard
- Air drawing
- Presentation mode
- Gaming mode
- Gesture recording
- User calibration
- Cross-platform optimization

---

# 🤝 Contributing

Contributions are welcome.

If you'd like to improve GestureMouse:

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Add feature"
```

4. Push

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Utkarsh Raut**

M.Sc. Computer Science

GitHub

**https://github.com/utkarsh-raut**

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future development.
