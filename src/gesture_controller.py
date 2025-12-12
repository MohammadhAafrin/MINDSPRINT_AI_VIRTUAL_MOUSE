import math
import time
import pyautogui # type: ignore

class GestureController:
    def __init__(self):
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0  # make all PyAutoGUI actions instant

        self.last_click_time = 0
        self.last_double_click_time = 0
        self.last_right_click_time = 0

    # ------------------------------
    # UTILITY: Distance
    # ------------------------------
    @staticmethod
    def distance(p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    # ------------------------------
    # LEFT CLICK
    # ------------------------------
    def detect_click(self, thumb, index):
        if self.distance(thumb, index) < 35:
            now = time.time()
            # reduced threshold for faster click response
            if now - self.last_click_time > 0.2:
                pyautogui.click()
                self.last_click_time = now

    # ------------------------------
    # DOUBLE CLICK
    # ------------------------------
    def detect_double_click(self, thumb, index):
        if self.distance(thumb, index) < 30:
            now = time.time()
            # reduced threshold for faster double click
            if now - self.last_double_click_time > 0.4 and now - self.last_click_time > 0.15:
                pyautogui.doubleClick()
                self.last_double_click_time = now

    # ------------------------------
    # RIGHT CLICK
    # ------------------------------
    def detect_right_click(self, thumb, middle):
        if self.distance(thumb, middle) < 35:
            now = time.time()
            # reduced threshold for faster right click
            if now - self.last_right_click_time > 0.3:
                pyautogui.rightClick()
                self.last_right_click_time = now

    # ------------------------------
    # SCROLLING
    # ------------------------------
    def detect_scroll(self, fingers):
        """
        Scroll up/down by comparing index and middle finger tips
        """
        index_tip = fingers[8]
        middle_tip = fingers[12]
        diff_y = index_tip[1] - middle_tip[1]

        # Reduced threshold for faster response
        if abs(diff_y) < 10:
            return

        if diff_y < 0:
            pyautogui.scroll(150)
        else:
            pyautogui.scroll(-150)

    # ------------------------------
    # DRAG & DROP
    # ------------------------------
    def detect_drag(self, thumb, index, hold_status):
        dist = self.distance(thumb, index)

        # Start drag
        if dist < 25 and not hold_status:
            pyautogui.mouseDown()
            return True

        # Release drag
        if dist >= 25 and hold_status:
            pyautogui.mouseUp()
            return False

        return hold_status
