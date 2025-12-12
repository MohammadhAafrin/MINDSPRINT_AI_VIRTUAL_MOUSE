import cv2 # type: ignore
import numpy as np # type: ignore

class GestureAIModel:
    def __init__(self):
        print("⚠️ Dummy Gesture Model Loaded (no dataset)")

    def predict(self, frame, bbox):
        # Extract ROI
        x, y, w, h = bbox
        roi = frame[y:y+h, x:x+w]

        if roi.size == 0:
            return None

        # SIMPLE BRIGHTNESS-BASED FAKE PREDICTION
        brightness = roi.mean()

        if brightness < 80:
            return "click"
        elif brightness < 120:
            return "scroll_down"
        else:
            return None
