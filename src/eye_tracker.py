import cv2 # type: ignore
import numpy as np # type: ignore

class EyeTracker:
    def __init__(self, debug=False):
        self.debug = debug

    def detect_eye_scroll(self, frame):
        """
        Detects up/down eye movement based on brightness differences in upper and lower thirds of the frame.
        Returns:
            "up"   -> if eyes are looking up
            "down" -> if eyes are looking down
            None   -> if no significant movement detected
        """
        # Check for valid frame
        if frame is None or frame.size == 0:
            return None

        h, w = frame.shape[:2]

        # Split frame into top and bottom thirds
        upper = frame[:h // 3]
        lower = frame[2 * h // 3:]

        # Convert to grayscale
        upper_gray = cv2.cvtColor(upper, cv2.COLOR_BGR2GRAY)
        lower_gray = cv2.cvtColor(lower, cv2.COLOR_BGR2GRAY)

        # Calculate mean brightness
        brightness_upper = np.mean(upper_gray)
        brightness_lower = np.mean(lower_gray)

        # Debug: show the two regions
        if self.debug:
            cv2.imshow("Upper Region", upper_gray)
            cv2.imshow("Lower Region", lower_gray)

        # Adaptive threshold: relative brightness difference
        if brightness_upper < brightness_lower - 10:
            return "up"
        elif brightness_lower < brightness_upper - 10:
            return "down"

        return None
