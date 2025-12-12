import cv2 # type: ignore
import mediapipe as mp # type: ignore

class HandTracker:
    def __init__(self, detection_conf=0.7, max_hands=1, debug=False):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.debug = debug

    def get_hand_landmarks(self, frame):
        # Check valid frame
        if frame is None or frame.size == 0:
            return None, None

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        if result.multi_hand_landmarks:
            landmarks = result.multi_hand_landmarks[0]
            h, w, c = frame.shape

            coords = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks.landmark]

            # Optional: draw landmarks on frame for debugging
            if self.debug:
                self.mp_draw.draw_landmarks(frame, landmarks, mp.solutions.hands.HAND_CONNECTIONS)
                cv2.imshow("Hand Tracking", frame)

            return coords, landmarks

        return None, None
