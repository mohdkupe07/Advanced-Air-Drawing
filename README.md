# 🎨 Advanced Air Drawing

An AI-powered Virtual Whiteboard that enables users to draw in the air using hand gestures and a webcam. The system uses Computer Vision and Hand Tracking to provide a touch-free drawing experience, allowing users to write, sketch, erase, and interact with a virtual canvas in real time.

---

## 🚀 Overview

Advanced Air Drawing is a gesture-controlled drawing application built using Python, OpenCV, and MediaPipe. Instead of using a mouse, stylus, or touchscreen, users can draw naturally in the air using their hand movements captured through a webcam.

The project leverages real-time hand landmark detection to recognize gestures and translate them into drawing actions, creating an intuitive Human-Computer Interaction (HCI) experience.

---

## ✨ Features

* ✍️ Draw in the air using finger gestures
* 🎨 Multiple color selection options
* 📏 Adjustable brush thickness
* 🧽 Gesture-based eraser functionality
* 🖐️ Clear entire canvas using hand gesture
* ⌨️ Keyboard shortcuts for quick controls
* 📷 Real-time hand tracking with MediaPipe
* ⚡ Smooth and responsive drawing experience
* 🖥️ Webcam-based interaction (No additional hardware required)

---

## 🛠️ Tech Stack

| Technology | Purpose                            |
| ---------- | ---------------------------------- |
| Python     | Core Programming Language          |
| OpenCV     | Image Processing & Webcam Handling |
| MediaPipe  | Hand Landmark Detection & Tracking |
| NumPy      | Numerical Operations               |

---

## 📋 How It Works

1. Webcam captures live video feed.
2. MediaPipe detects hand landmarks in real time.
3. Finger positions are analyzed to identify gestures.
4. Gestures control drawing, erasing, color selection, and canvas operations.
5. OpenCV renders the virtual canvas and updates drawings dynamically.

---

## 🎯 Supported Gestures

| Gesture           | Action         |
| ----------------- | -------------- |
| Index Finger Up   | Draw           |
| Two Fingers Up    | Selection Mode |
| Eraser Gesture    | Erase Drawing  |
| Open Palm         | Clear Canvas   |
| Keyboard Shortcut | Reset Canvas   |

---

## 💡 Applications

* Virtual Whiteboards
* Online Teaching & Learning
* Interactive Presentations
* Touchless Human-Computer Interaction
* Smart Classrooms
* Creative Digital Art

---

## 📂 Project Structure

```bash
Advanced-Air-Drawing/
│
├── hand_tracker.py
├── main.py
├── requirements.txt
├── README.md
└── assets/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/mohdkupe07/Advanced-Air-Drawing.git
```

### Navigate to Project Folder

```bash
cd Advanced-Air-Drawing
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python main.py
```

---

## 📸 Demo

Add screenshots or GIF demonstrations here.

Example:

* Air Drawing Mode
* Color Selection
* Eraser Mode
* Canvas Reset

---

## 📚 Learning Outcomes

This project helped me gain practical experience in:

* Computer Vision
* Hand Landmark Detection
* Gesture Recognition
* Human-Computer Interaction (HCI)
* Real-Time Video Processing
* AI-Based User Interfaces

---

## 🔮 Future Enhancements

* Shape Drawing Recognition
* Handwriting Recognition
* Multi-Hand Support
* Save Canvas as Image
* AI-Powered Shape Correction
* Collaborative Online Whiteboard

---

## 👨‍💻 Author

**Mohammed Asif Kupe**

B.E. Computer Science & Engineering (Data Science)

M.G.M.'s College of Engineering & Technology, Navi Mumbai

GitHub: https://github.com/mohdkupe07

---

⭐ If you found this project useful, consider giving it a star on GitHub.
