AI Virtual Mouse is an advanced human–computer interaction system that replaces physical mouse input with hand gestures, eye tracking, and voice commands. Using Python, OpenCV, MediaPipe, and TensorFlow Lite, it enables cursor movement, clicking, scrolling, drag-and-drop, and voice-based actions in real time. Designed to be fast, accurate, and cross-platform, this project offers a touchless, modern way to control any computer.

🖱️ AI Virtual Mouse — Gesture, Eye & Voice Controlled Mouse

A fully AI-powered virtual mouse system that allows users to control the computer cursor using hand gestures, eye tracking, and voice commands. Built with Python, OpenCV, MediaPipe, TensorFlow Lite, and integrated gesture models, this project eliminates the need for traditional hardware and makes human-computer interaction more natural and accessible.

🚀 Features : 

✋ Hand Gesture Control
Index finger cursor movement
Pinch gesture → Left Click
Double-pinch → Double Click
Right-hand gesture → Right Click
Two-finger scroll gestures
Pinch-hold drag → Drag & Drop

👁️ Eye Tracking
Eye-controlled cursor movement
Eye-blink actions
Eye-based scrolling

🎤 Voice Commands
Perform actions like “click”, “scroll”, “open browser”, etc.

📦 Cross Platform
Works on Windows, macOS, and Linux

⚡ Lightweight & Real-time
Uses TFLite models for fast inference
Highly optimized for CPU-only systems

🧠 Tech Stack
Python
OpenCV
MediaPipe
TensorFlow Lite / XNNPACK
PyAudio / SpeechRecognition
Hand Landmark Detection
Eye Tracking Model
Custom Gesture Recognition Logic

📂 Project Structure
project/
│── run.py
│── src/
│   ├── virtual_mouse.py
│   ├── gestures_ai_model.py
        gesture_controller.py
        hand_tracker.py
│   ├── eye_tracker/
│   ── voice_control.py/


🎯 Use Cases

Accessibility for users with physical limitations

Touchless computing

Gaming (gesture-based control)

Smart virtual assistants

Human–computer interaction research

📸 Demo

(Include demo GIFs/screenshots here)

🛠️ How to Run
pip install -r requirements.txt
python run.py

⭐ Contributions

PRs and feature improvements are welcome!

