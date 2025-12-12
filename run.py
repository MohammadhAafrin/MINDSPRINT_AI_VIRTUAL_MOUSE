import cv2 # type: ignore
import pyautogui # type: ignore
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from hand_tracker import HandTracker # type: ignore
from gesture_controller import GestureController # type: ignore
from eye_tracker import EyeTracker # type: ignore
from voice_control import VoiceControl # type: ignore
from gesture_ai_model import GestureAIModel # type: ignore

hand_tracker = HandTracker()
gesture = GestureController()
eye_scroll = EyeTracker()
voice = VoiceControl()
gesture_ai = GestureAIModel()

pyautogui.FAILSAFE = False

def main():
    print("🔥 AI Virtual Mouse with Eye + Gesture Dataset Starting...")
    cap = cv2.VideoCapture(0)

    screen_w, screen_h = pyautogui.size()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        cam_h, cam_w = frame.shape[:2]

        coords, hand_lm = hand_tracker.get_hand_landmarks(frame)

        # ----------------------------------
        # EYE SCROLLING (ALWAYS ACTIVE)
        # ----------------------------------
        scroll_dir = eye_scroll.detect_eye_scroll(frame)
        if scroll_dir == "up":
            print("👁️ Scroll UP (Eye)")
            pyautogui.scroll(150)
        elif scroll_dir == "down":
            print("👁️ Scroll DOWN (Eye)")
            pyautogui.scroll(-150)

        # ----------------------------------
        # HAND GESTURES + AI MODEL
        # ----------------------------------
        if coords and hand_lm:
            x_list = [pt[0] for pt in coords]
            y_list = [pt[1] for pt in coords]
            x1, y1 = min(x_list), min(y_list)
            x2, y2 = max(x_list), max(y_list)
            bbox = (x1, y1, x2 - x1, y2 - y1)

            # Predict gesture using dataset model
            gesture_name = gesture_ai.predict(frame, bbox)
            print("Gesture:", gesture_name)

            # Dataset-based gesture actions
            if gesture_name == "click":
                pyautogui.click()
            elif gesture_name == "double_click":
                pyautogui.doubleClick()
            elif gesture_name == "right_click":
                pyautogui.rightClick()
            elif gesture_name == "scroll_up":
                pyautogui.scroll(150)
            elif gesture_name == "scroll_down":
                pyautogui.scroll(-150)
            elif gesture_name == "drag":
                pyautogui.mouseDown()
            else:
                pyautogui.mouseUp()

            # Cursor movement
            index = coords[8]
            px = int(index[0] * screen_w / cam_w)
            py = int(index[1] * screen_h / cam_h)
            pyautogui.moveTo(px, py)

        cv2.imshow("AI Virtual Mouse (Deep Learning + Eye Scroll)", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
