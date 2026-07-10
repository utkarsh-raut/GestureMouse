"""
Real-time Gesture-Based Human-Computer Interaction (HCI) Engine
Built with MediaPipe Tasks API, PyAutoGUI, and Adaptive Filtering.
"""

import time
import math
import collections
import cv2
import pyautogui
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# -------------------------------------------------------------------------
# 1. System Configuration
# -------------------------------------------------------------------------
class SystemConfig:
    # Camera Settings
    CAM_INDEX = 0
    FRAME_W = 1280
    FRAME_H = 720
    
    # MediaPipe Asset Path
    MODEL_PATH = "hand_landmarker.task"
    
    # Kinematics & Filtering Parameters
    FILTER_ALPHA_MIN = 0.60   
    FILTER_ALPHA_MAX = 0.15   
    VELOCITY_THRESHOLD_MIN = 0.003
    VELOCITY_THRESHOLD_MAX = 0.045
    DEADZONE_RADIUS_PX = 3    
    
    # Dual-Threshold Hysteresis (Schmitt Trigger)
    PINCH_ENGAGE_DIST = 0.055  
    PINCH_RELEASE_DIST = 0.075 
    
    # Scroll Configuration (Linux Tick Optimization)
    SCROLL_THRESHOLD_Y = 0.012
    SCROLL_ACCUM_TARGET = 1.0
    SCROLL_GAIN = 18.0
    
    # State Engine Stability
    DEBOUNCE_FRAMES = 3

# -------------------------------------------------------------------------
# 2. Mathematical Kinematics & Filtering Engine
# -------------------------------------------------------------------------
class AdaptiveKinematicFilter:
    def __init__(self, alpha_min, alpha_max, v_min, v_max):
        self.alpha_min = alpha_min
        self.alpha_max = alpha_max
        self.v_min = v_min
        self.v_max = v_max
        self.stored_x = None
        self.stored_y = None
        self.last_time = time.time()

    def filter(self, target_x, target_y):
        now = time.time()
        dt = max(1e-6, now - self.last_time)
        self.last_time = now

        if self.stored_x is None or self.stored_y is None:
            self.stored_x = target_x
            self.stored_y = target_y
            return target_x, target_y

        inst_velocity = math.hypot(target_x - self.stored_x, target_y - self.stored_y) / dt
        
        if inst_velocity <= self.v_min:
            t = 0.0
        elif inst_velocity >= self.v_max:
            t = 1.0
        else:
            t = (inst_velocity - self.v_min) / (self.v_max - self.v_min)

        current_alpha = self.alpha_min + t * (self.alpha_max - self.alpha_min)
        
        self.stored_x = current_alpha * target_x + (1.0 - current_alpha) * self.stored_x
        self.stored_y = current_alpha * target_y + (1.0 - current_alpha) * self.stored_y
        
        return self.stored_x, self.stored_y

# -------------------------------------------------------------------------
# 3. OS Integration & Scroll Abstraction Layer
# -------------------------------------------------------------------------
class LinuxMouseController:
    def __init__(self, config: SystemConfig):
        self.config = config
        self.screen_w, self.screen_h = pyautogui.size()
        self.scroll_bucket = 0.0
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.0

    def move_to(self, target_x, target_y):
        safe_x = max(0, min(self.screen_w - 1, int(target_x)))
        safe_y = max(0, min(self.screen_h - 1, int(target_y)))
        
        cx, cy = pyautogui.position()
        if math.hypot(safe_x - cx, safe_y - cy) > self.config.DEADZONE_RADIUS_PX:
            pyautogui.moveTo(safe_x, safe_y)

    def set_drag_state(self, hold: bool):
        if hold:
            pyautogui.mouseDown()
        else:
            pyautogui.mouseUp()

    def inject_scroll(self, velocity_y):
        self.scroll_bucket += (velocity_y * self.config.SCROLL_GAIN)
        ticks = int(self.scroll_bucket / self.config.SCROLL_ACCUM_TARGET)
        
        if ticks != 0:
            pyautogui.scroll(ticks)
            self.scroll_bucket -= (ticks * self.config.SCROLL_ACCUM_TARGET)

    def reset_accumulators(self):
        self.scroll_bucket = 0.0

# -------------------------------------------------------------------------
# 4. Deterministic Finite State Machine (FSM)
# -------------------------------------------------------------------------
class GestureEngineState:
    FIST_KILL = 0
    SCROLLING = 1
    DRAGGING  = 2
    NAVIGATING = 3
    IDLE       = 4

class GestureFSM:
    def __init__(self, config: SystemConfig):
        self.cfg = config
        self.current_state = GestureEngineState.IDLE
        self.pinch_active = False
        self.prev_scroll_y = None
        self.debounce_buffer = collections.deque(maxlen=config.DEBOUNCE_FRAMES)

    def process_frame(self, landmarks, controller: LinuxMouseController, filter_engine: AdaptiveKinematicFilter):
        hand = landmarks[0]
        
        wrist = hand[0]
        thumb_tip = hand[4]
        idx_tip = hand[8]
        mid_tip = hand[12]
        
        current_pinch_dist = math.hypot(idx_tip.x - thumb_tip.x, idx_tip.y - thumb_tip.y)
        
        def is_curled(tip, pip): return hand[tip].y > hand[pip].y
        
        # 1. Evaluate Pinch Hysteresis First
        if self.pinch_active:
            if current_pinch_dist > self.cfg.PINCH_RELEASE_DIST:
                self.pinch_active = False
        else:
            if current_pinch_dist < self.cfg.PINCH_ENGAGE_DIST:
                self.pinch_active = True

        # 2. Extract Structural Features (Fist is mutually exclusive with Pinch)
        raw_fist = all(is_curled(i, i - 2) for i in [8, 12, 16, 20]) and not self.pinch_active
        raw_scroll = (not is_curled(8, 6) and not is_curled(12, 10) and is_curled(16, 14) and is_curled(20, 18))

        # 3. State Mapping priority
        if raw_fist:
            candidate = GestureEngineState.FIST_KILL
        elif raw_scroll:
            candidate = GestureEngineState.SCROLLING
        elif self.pinch_active:
            candidate = GestureEngineState.DRAGGING
        elif not is_curled(8, 6):
            candidate = GestureEngineState.NAVIGATING
        else:
            candidate = GestureEngineState.IDLE

        # Temporal Debounce Filtering
        self.debounce_buffer.append(candidate)
        if len(self.debounce_buffer) == self.cfg.DEBOUNCE_FRAMES and len(set(self.debounce_buffer)) == 1:
            validated_state = self.debounce_buffer[0]
        else:
            validated_state = self.current_state 

        # Handle State Transitions
        if validated_state != self.current_state:
            if self.current_state == GestureEngineState.DRAGGING:
                controller.set_drag_state(False)
            if self.current_state == GestureEngineState.SCROLLING:
                self.prev_scroll_y = None
                controller.reset_accumulators()
            self.current_state = validated_state

        # Execute State Behavior
        if validated_state == GestureEngineState.FIST_KILL:
            pass 
            
        elif validated_state == GestureEngineState.SCROLLING:
            current_y = idx_tip.y
            if self.prev_scroll_y is not None:
                dy = current_y - self.prev_scroll_y
                if abs(dy) > self.cfg.SCROLL_THRESHOLD_Y:
                    controller.inject_scroll(-dy)
            self.prev_scroll_y = current_y
            
        elif validated_state == GestureEngineState.DRAGGING:
            controller.set_drag_state(True)
            fx, fy = filter_engine.filter(idx_tip.x, idx_tip.y)
            controller.move_to(fx * controller.screen_w, fy * controller.screen_h)
            
        elif validated_state == GestureEngineState.NAVIGATING:
            fx, fy = filter_engine.filter(idx_tip.x, idx_tip.y)
            controller.move_to(fx * controller.screen_w, fy * controller.screen_h)
            
        elif validated_state == GestureEngineState.IDLE:
            pass

# -------------------------------------------------------------------------
# 5. Core Pipeline Runtime
# -------------------------------------------------------------------------
class CoreGestureEngine:
    def __init__(self):
        self.cfg = SystemConfig()
        self.controller = LinuxMouseController(self.cfg)
        self.filter = AdaptiveKinematicFilter(
            self.cfg.FILTER_ALPHA_MIN, self.cfg.FILTER_ALPHA_MAX,
            self.cfg.VELOCITY_THRESHOLD_MIN, self.cfg.VELOCITY_THRESHOLD_MAX
        )
        self.fsm = GestureFSM(self.cfg)
        self.latest_landmarks = None

    def _async_callback(self, result: vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
        if result.hand_landmarks:
            self.latest_landmarks = result.hand_landmarks
        else:
            self.latest_landmarks = None

    def run(self):
        base_options = python.BaseOptions(model_asset_path=self.cfg.MODEL_PATH)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=self._async_callback,
            num_hands=1
        )
        
        detector = vision.HandLandmarker.create_from_options(options)
        cap = cv2.VideoCapture(self.cfg.CAM_INDEX)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cfg.FRAME_W)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cfg.FRAME_H)

        print("[SYSTEM INFO] Runtime Initialized Successfully. Press ESC inside frame to terminate.")

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)
            
            detector.detect_async(mp_image, int(time.time() * 1000))

            if self.latest_landmarks:
                self.fsm.process_frame(self.latest_landmarks, self.controller, self.filter)
                
                state_labels = {0: "FIST_LOCK", 1: "SCROLLING", 2: "DRAGGING", 3: "NAVIGATING", 4: "IDLE"}
                current_label = state_labels.get(self.fsm.current_state, "UNKNOWN")
                cv2.putText(frame, f"State: {current_label}", (20, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                idx = self.latest_landmarks[0][8]
                h, w, _ = frame.shape
                cv2.circle(frame, (int(idx.x * w), int(idx.y * h)), 8, (255, 0, 0), -1)

            # DECOUPLED PREVIEW: Resize output frame for display, leaving AI feed untouched
            display_w = int(self.cfg.FRAME_W * 0.5)
            display_h = int(self.cfg.FRAME_H * 0.5)
            preview_frame = cv2.resize(frame, (display_w, display_h))

            cv2.imshow("Production HCI Engine Framework", preview_frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        detector.close()

if __name__ == "__main__":
    engine = CoreGestureEngine()
    engine.run()
