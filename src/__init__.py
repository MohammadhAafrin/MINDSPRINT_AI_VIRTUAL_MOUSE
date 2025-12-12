import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import cv2 # type: ignore
import pyautogui # type: ignore

# Import your modules
from hand_tracker import HandTracker # type: ignore
from gesture_controller import GestureController # type: ignore
from eye_tracker import EyeTracker # type: ignore
from voice_control import VoiceControl # type: ignore

# Initialize
hand_tracker = HandTracker()
gesture = GestureController()
eye_scroll = EyeTracker()
voice = VoiceControl()

pyautogui.FAILSAFE = False

def main():
    print("🔥 Starting AI Virtual Mouse...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Cannot open webcam")
        return

    hold_status = False
    screen_w, screen_h = pyautogui.size()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Cannot read frame")
            break

        frame = cv2.flip(frame, 1)
        cam_h, cam_w = frame.shape[:2]

        # ---- Hand Tracking ----
        coords, _ = hand_tracker.get_hand_landmarks(frame)
        if coords:
            thumb = coords[4]
            index = coords[8]
            middle = coords[12]

            # ---- Cursor Movement ----
            x = int(index[0] * screen_w / cam_w)
            y = int(index[1] * screen_h / cam_h)
            x = max(0, min(screen_w, x))
            y = max(0, min(screen_h, y))
            pyautogui.moveTo(x, y)

            # ---- Clicks ----
            gesture.detect_click(thumb, index)
            gesture.detect_double_click(thumb, index)
            gesture.detect_right_click(thumb, middle)

            # ---- Drag & Drop ----
            hold_status = gesture.detect_drag(thumb, index, hold_status)

        # ---- Eye Scroll ----
        scroll_dir = eye_scroll.detect_eye_scroll(frame)
        if scroll_dir == "up":
            pyautogui.scroll(150)
        elif scroll_dir == "down":
            pyautogui.scroll(-150)

        # ---- Voice Commands ----
        try:
            command = voice.listen()
            if command:
                print("🎤 Voice Command:", command)
                voice.process_command(command)
        except Exception as e:
            # ignore errors like no microphone detected
            pass

        # ---- Show Webcam ----
        cv2.imshow("AI Virtual Mouse", frame)

        # ---- Quit on ESC ----
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("👋 Virtual Mouse Closed.")


if __name__ == "__main__":
    main()




