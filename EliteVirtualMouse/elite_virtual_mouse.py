import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math


class EliteVirtualMouse:
    def __init__(self):
        # Hardware-optimized settings
        self.screen_w, self.screen_h = pyautogui.size()
        self.cam_w, self.cam_h = 640, 480  # Balanced resolution

        # Precision tuning
        self.corner_boost = 0.28  # Enhanced edge reach (+28%)
        self.bottom_boost = 0.45  # Improved bottom reach (+45%)
        self.deadzone_radius = 0.12  # Smaller deadzone for more control

        # Performance mastery
        self.smoothing = 0.35  # Ultra-responsive yet stable
        self.prev_x, self.prev_y = 0.5, 0.5

        # Gesture perfection
        self.click_thresh = 0.055  # Pixel-perfect click detection
        self.scroll_thresh = 0.18  # Intentional scrolling
        self.right_click_hold = 0.9  # Faster right-click
        self.click_cooldown = 0.25  # Natural click rhythm

        # Advanced MediaPipe config
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75,
            static_image_mode=False
        )

        # Professional camera setup
        self.cap = cv2.VideoCapture(0)
        self._configure_high_perf_camera()

        # State-of-the-art tracking
        self.last_click_time = 0
        self.right_click_start = None
        self.last_scroll_time = 0
        self.scroll_active = False

    def _configure_high_perf_camera(self):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cam_w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cam_h)
        self.cap.set(cv2.CAP_PROP_FPS, 60)  # High refresh rate
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        # Camera warmup with validation
        for _ in range(10):
            ret, _ = self.cap.read()
            if not ret:
                raise RuntimeError("Professional-grade camera initialization failed")

    def run(self):
        try:
            fps_counter = FPSCounter()
            while True:
                start_time = time.perf_counter()

                # Elite frame processing
                ret, frame = self.cap.read()
                if not ret:
                    self._handle_camera_failure()
                    continue

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Military-grade hand tracking
                try:
                    results = self.hands.process(rgb)
                except Exception as e:
                    print(f"Tracking exception: {e}")
                    continue

                display = frame.copy()
                self._draw_pro_ui(display)

                if results.multi_hand_landmarks:
                    try:
                        hand = results.multi_hand_landmarks[0]
                        self._process_elite_gestures(hand, display, start_time)
                    except Exception as e:
                        print(f"Gesture processing error: {e}")

                # Show professional diagnostics
                fps_counter.update()
                cv2.putText(display, f"FPS: {fps_counter.fps:.1f}", (self.cam_w - 120, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                cv2.imshow("Elite Virtual Mouse Pro", display)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            self._professional_cleanup()

    def _process_elite_gestures(self, hand, display, frame_time):
        landmarks = hand.landmark
        index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
        middle_tip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

        # Tactical cursor movement
        self._precision_move(index_tip, display)

        # Special forces gesture detection
        current_time = time.time()
        self._sniper_click_detection(index_tip, thumb_tip, display, current_time)
        self._jet_scroll_detection(index_tip, middle_tip, display, current_time)

        # Visual intelligence
        mp.solutions.drawing_utils.draw_landmarks(
            display, hand, self.mp_hands.HAND_CONNECTIONS)

    def _precision_move(self, index_tip, display):
        raw_x = np.clip(index_tip.x * (1 + self.corner_boost) - (self.corner_boost / 2), 0, 1)
        raw_y = np.clip(index_tip.y * (1 + self.bottom_boost) - (self.bottom_boost / 3), 0, 1)

        # Deadzone ops
        center_dist = math.hypot(raw_x - 0.5, raw_y - 0.5)
        if center_dist < self.deadzone_radius:
            cv2.circle(display, (int(raw_x * self.cam_w), int(raw_y * self.cam_h)),
                       int(self.deadzone_radius * self.cam_w), (0, 0, 255), 1)
            return

        # Radar-grade smoothing
        smooth_x = self.prev_x * self.smoothing + raw_x * (1 - self.smoothing)
        smooth_y = self.prev_y * self.smoothing + raw_y * (1 - self.smoothing)
        self.prev_x, self.prev_y = smooth_x, smooth_y

        # Mission-critical cursor placement
        screen_x = int(smooth_x * self.screen_w)
        screen_y = int(smooth_y * self.screen_h)

        try:
            pyautogui.moveTo(screen_x, screen_y, _pause=False, duration=0)
        except pyautogui.FailSafeException:
            pass

    def _sniper_click_detection(self, index_tip, thumb_tip, display, current_time):
        pinch_dist = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)

        # Combat-ready visual feedback
        if pinch_dist < self.click_thresh * 1.5:
            color = (0, 0, 255) if pinch_dist < self.click_thresh else (0, 165, 255)
            cv2.circle(display,
                       (int(index_tip.x * self.cam_w), int(index_tip.y * self.cam_h)),
                       30, color, 2)

        # Tactical click operations
        if pinch_dist < self.click_thresh:
            if current_time - self.last_click_time > self.click_cooldown:
                pyautogui.click()
                self.last_click_time = current_time
        elif pinch_dist < self.click_thresh * 1.5:
            if self.right_click_start is None:
                self.right_click_start = current_time
            elif current_time - self.right_click_start > self.right_click_hold:
                pyautogui.rightClick()
                self.right_click_start = None
                self.last_click_time = current_time
        else:
            self.right_click_start = None

    def _jet_scroll_detection(self, index_tip, middle_tip, display, current_time):
        scroll_dist = middle_tip.y - index_tip.y

        if abs(scroll_dist) > self.scroll_thresh:
            if not self.scroll_active or current_time - self.last_scroll_time > 0.1:
                scroll_amount = int(50 * (abs(scroll_dist) / self.scroll_thresh))
                pyautogui.scroll(scroll_amount if scroll_dist > 0 else -scroll_amount)
                self.last_scroll_time = current_time
                self.scroll_active = True

                # Stealth visual feedback
                cv2.circle(display,
                           (int(index_tip.x * self.cam_w), int(index_tip.y * self.cam_h)),
                           35, (255, 255, 0), 2)
        else:
            self.scroll_active = False

    def _draw_pro_ui(self, frame):
        overlay = frame.copy()
        cv2.rectangle(overlay, (8, 8), (400, 160), (50, 50, 50), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        pro_tips = [
            "ELITE MODE ACTIVATED",
            "Move: Precision index tracking",
            "Click: Quick pinch (0.25s cooldown)",
            "Right-Click: Hold pinch (0.9s)",
            "Scroll: Index-middle finger distance",
            "Deadzone: Red center area",
            "Press Q for tactical retreat"
        ]

        for i, text in enumerate(pro_tips):
            color = (0, 255, 255) if i == 0 else (0, 200, 255)
            cv2.putText(frame, text, (10, 30 + i * 22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    def _handle_camera_failure(self):
        print("Camera failure - initiating emergency protocol")
        time.sleep(1)
        self.cap.release()
        self._configure_high_perf_camera()

    def _professional_cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.hands.close()
        print("Mission complete. Resources secured.")


class FPSCounter:
    def __init__(self):
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()

    def update(self):
        self.frame_count += 1
        elapsed = time.time() - self.start_time
        if elapsed > 0.5:  # Update FPS twice per second
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.start_time = time.time()


if __name__ == "__main__":
    print("Initializing Elite Virtual Mouse System...")
    mouse = EliteVirtualMouse()
    mouse.run()



# Copyright (C) 2025 Vihanga Arunalu  
# Contact: vihangaarunalu10@gmail.com
# License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.html)  
