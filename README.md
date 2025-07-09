# AI Security Camera with ESP32 & Gmail Notification

This project is an AI-powered security system using YOLOv11 for human detection, Django for backend and video streaming, and ESP32 for physical alerts. When a person is detected in the camera feed, the system sends real-time notifications via Gmail and activates connected devices (e.g., LEDs or buzzers) using ESP32.

---

## 🛠️ Features

- Live video streaming from Webcam/IP Camera.
- Human detection using YOLOv11.
- Visual alerts (bounding boxes) in the video feed.
- Real-time Gmail email notifications.
- ESP32 integration for physical warnings (e.g., blinking LED, sound).
- Web-based interface for login, register, and video monitoring.
- Built with Django + OpenCV + YOLOv11 + MySQL.

---

## 📂 Project Structure

```bash
Ai_security_cam_Django_Esp32_Gmail/
│
├── Docs/                         # Documentation files
├── project_cam/
│   ├── camera/                  # Django app (YOLO, video processing)
│   ├── code_esp/                # ESP32 source code
│   └── project_cam/             # Django main project
│
└── Video_images/                # Screenshots and diagrams
```

---

## 📷 System Architecture

### Component Diagram
<img src="Video_images/Pic%201%20Component%20diagram%20-%20module%20structure%20of%20the%20software.png" width="50%">

### Logical Architecture
<img src="Video_images/Pic%202%20Logical%20architecture.png" width="50%">

### Physical Architecture
<img src="Video_images/Pic%203%20Physical%20architecture.png" width="50%">

### Operation Sequences

- Procedure 1  
  <img src="Video_images/Pic%204%20Procedure%20Operation%20Sequence%201.png" width="50%">

- Procedure 2  
  <img src="Video_images/Pic%205%20Procedure%20Operation%20Sequence%202.png" width="50%">

---

## 🖥️ Web Interface Screenshots

### Registration Form
<img src="Video_images/Pic%206%20Registration%20form%20screenshot.png" width="50%">

### Login Form
<img src="Video_images/Pic%207%20Login%20form%20screenshot.png" width="50%">

### Video Feed with Detection
<img src="Video_images/Pic%208%20Video%20screenshot%20with%20people%20framed.png" width="50%">

### Gmail Notification Example
<img src="Video_images/Pic%209%20Screenshot%20of%20Received%20warning%20mail.png" width="50%">

---

## 🔧 ESP32 Interaction

### ESP32 when person detected
<img src="Video_images/Pic%2010%20ESP32%20receives%20notification%20of%20presence%20and%20displays%20warning.png" width="50%">

### ESP32 when no person
<img src="Video_images/Pic%2011%20ESP32%20received%20no%20person%20notification.png" width="50%">

---
