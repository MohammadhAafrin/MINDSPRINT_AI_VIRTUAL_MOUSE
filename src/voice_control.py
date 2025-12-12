import speech_recognition as sr # type: ignore
import pyttsx3 # type: ignore
import pyautogui # type: ignore

class VoiceControl:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=3)
                command = self.recognizer.recognize_google(audio).lower()
                return command
        except:
            return ""

    def process_command(self, cmd):
        if "click" in cmd:
            pyautogui.click()
            self.speak("Clicked")

        elif "double click" in cmd:
            pyautogui.doubleClick()

        elif "right click" in cmd:
            pyautogui.rightClick()

        elif "scroll up" in cmd:
            pyautogui.scroll(200)

        elif "scroll down" in cmd:
            pyautogui.scroll(-200)

        elif "stop" in cmd:
            self.speak("Stopping voice control")
            return False

        return True
