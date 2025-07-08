from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse

import cv2
import time
import smtplib
import threading
import logging
import requests

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ultralytics import YOLO

from .forms import RegisterForm

# CẤU HÌNH VÀ FLAG TÙY CHỌN
USE_ESP32 = True  # Bật/tắt gửi request đến ESP32
USE_EMAIL  = True  # Bật/tắt gửi email thông báo

ESP32_IP = "http://172.20.10.6" 
EMAIL_SENDER       = "your_gmail@gmail.com"
EMAIL_SENDER_PW    = "your_pw"

# CẤU HÌNH LOG & MODEL AI
logging.getLogger("ultralytics").setLevel(logging.ERROR)
model = YOLO("yolo11n.pt")

# PHẦN XỬ LÝ TÀI KHOẢN (REGISTER, LOGIN, LOGOUT)
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, "Đăng ký thất bại. Vui lòng kiểm tra lại thông tin.")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('video')
        else:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu.")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('login')

# PHẦN GỬI THÔNG BÁO (EMAIL & ESP32)
def send_email_notification(receiver_email, subject, body):
    #Gửi email thông báo đồng bộ.
    message = MIMEMultipart()
    message["From"] = EMAIL_SENDER
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL_SENDER, EMAIL_SENDER_PW)
        server.sendmail(EMAIL_SENDER, receiver_email, message.as_string())
        server.quit()
    except Exception as e:
        print("Email sending error:", e)

def send_email_async(receiver_email, subject, body):
    #Gửi email bất đồng bộ nếu flag USE_EMAIL được bật.
    if USE_EMAIL:
        threading.Thread(
            target=send_email_notification,
            args=(receiver_email, subject, body)
        ).start()

def send_esp32_request(endpoint):
    #Gửi request đến ESP32 đồng bộ.
    try:
        requests.get(f"{ESP32_IP}/{endpoint}")
    except Exception as e:
        print("Lỗi kết nối ESP32!", e)

def send_esp32_async(endpoint):
    #Gửi request đến ESP32 bất đồng bộ nếu flag USE_ESP32 được bật.
    if USE_ESP32:
        threading.Thread(
            target=send_esp32_request,
            args=(endpoint,)
        ).start()

# PHẦN STREAM VIDEO VỚI XỬ LÝ AI
def generate_frames(user_email):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #cap = cv2.VideoCapture('http://172.20.10.5:8080/video')  # IP Camera

    person_detected_previous = False
    last_email_time = 0
    email_cooldown = 60
    frame_count = 0
    results = None

    while True:
        success, frame = cap.read()
        if not success:
            break
        # Resize frame
        frame = cv2.resize(frame, (640, 480))
        frame_count += 1
        # Xử lý AI frame 
        if frame_count % 15 == 0:
            results = model(frame)

        detected_person = False
        if results is not None:
            for r in results:
                boxes = r.boxes
                if boxes is not None and len(boxes) > 0:
                    for i, box in enumerate(boxes.xyxy):
                        if int(boxes.cls[i].item()) == 0:  # 'person' id = 0
                            detected_person = True
                            x1, y1, x2, y2 = map(int, box.tolist())
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(
                                frame, "Person", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2
                            )
        # Xử lý gửi thông báo khi có người xuất hiện (hoặc mất người)
        if detected_person and not person_detected_previous:
            current_time = time.time()
            if current_time - last_email_time > email_cooldown:
                subject = "Cảnh báo: Phát hiện người"
                body = "Hệ thống camera an ninh của bạn vừa phát hiện có người trong khung hình."
                send_email_async(user_email, subject, body)
                last_email_time = current_time
            send_esp32_async("person_detected")
        elif not detected_person and person_detected_previous:
            send_esp32_async("led_off")

        person_detected_previous = detected_person

        ret, buffer = cv2.imencode(".jpg", frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@login_required
def video_feed(request):
    user_email = request.user.email
    return StreamingHttpResponse(
        generate_frames(user_email),
        content_type="multipart/x-mixed-replace; boundary=frame"
    )

@login_required
def video_page(request):
    return render(request, "video.html")