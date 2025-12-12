import cv2 # type: ignore
import pyautogui # type: ignore
import sys
import os
import threading

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from hand_tracker import HandTracker
from gesture_controller import GestureController
from voice_control import VoiceControl
from eye_tracker import EyeTracker

class VirtualMouse:
    def __init__(self):
        self.tracker = HandTracker(debug=False)
        self.controller = GestureController()
        self.voice = VoiceControl()
        self.eyes = EyeTracker()

        self.dragging = False
        self.screen_w, self.screen_h = pyautogui.size()
        self.prev_x, self.prev_y = 0, 0
        self.smoothening = 2  # smaller = faster cursor
        pyautogui.PAUSE = 0  # remove PyAutoGUI delay

        # Voice command
        self.voice_cmd = None
        self.voice_thread = threading.Thread(target=self._listen_voice, daemon=True)
        self.voice_thread.start()

    def _listen_voice(self):
        while True:
            try:
                cmd = self.voice.listen()
                if cmd:
                    self.voice_cmd = cmd
            except Exception as e:
                print("Voice control error:", e)

    def start(self):
        cap = cv2.VideoCapture(0)
        # Reduce resolution for speed
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not cap.isOpened():
            print("❌ Error: Could not access webcam")
            return

        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                continue

            frame = cv2.flip(frame, 1)
            cam_h, cam_w = frame.shape[:2]

            # --- HAND TRACKING ---
            coords, landmarks = self.tracker.get_hand_landmarks(frame)
            if coords:
                thumb = coords[4]
                index = coords[8]
                middle = coords[12]

                # Smooth cursor movement
                x = int(index[0] * self.screen_w / cam_w)
                y = int(index[1] * self.screen_h / cam_h)
                x = self.prev_x + (x - self.prev_x) // self.smoothening
                y = self.prev_y + (y - self.prev_y) // self.smoothening
                pyautogui.moveTo(x, y)
                self.prev_x, self.prev_y = x, y

                # GESTURE CONTROL
                self.controller.detect_click(thumb, index)
                self.controller.detect_double_click(thumb, index)
                self.controller.detect_right_click(thumb, middle)
                self.controller.detect_scroll(coords)
                self.dragging = self.controller.detect_drag(thumb, index, self.dragging)

            # --- EYE SCROLL ---
            scroll_dir = self.eyes.detect_eye_scroll(frame)
            if scroll_dir == "up":
                pyautogui.scroll(150)
            elif scroll_dir == "down":
                pyautogui.scroll(-150)

            # --- VOICE COMMAND ---
            if self.voice_cmd:
                if not self.voice.process_command(self.voice_cmd):
                    break
                self.voice_cmd = None  # reset after processing

            # Show webcam window
            cv2.imshow("AI Virtual Mouse", frame)

            # Quit on Q key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
