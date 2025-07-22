import cv2
import serial
import time
import os
import keyboard

# Seri port ayarı
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# Yüz tanıma
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    motor_command = "Z"  # Default: stop

    if keyboard.is_pressed('w'):
        motor_command = "W"
    elif keyboard.is_pressed('s'):
        motor_command = "S"
    elif keyboard.is_pressed('a'):
        motor_command = "A"
    elif keyboard.is_pressed('d'):
        motor_command = "D"

    for (x, y, w, h) in faces:
        cx = x + w//2
        cy = y + h//2

        data = f"{cx},{cy},{motor_command}\n"
        ser.write(data.encode('utf-8'))
        print(f"GÖNDERİLEN: {data.strip()}")

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        break

    cv2.imshow("Tracking + Motor Kontrol", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
