import cv2
import serial
import time
import numpy as np
import os
import tkinter as tk
from threading import Thread
import keyboard

# Seri Port (COM3)
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# Sabit klasör yolu
base_path = r"C:\Users\smfse\OneDrive\Masaüstü\project_folder"
os.chdir(base_path)

# Renk aralıkları (HSV)
color_ranges = {
    "red": [
        (np.array([0, 100, 100]), np.array([10, 255, 255])),
        (np.array([160, 100, 100]), np.array([179, 255, 255]))
    ],
    "green": [
        (np.array([40, 50, 50]), np.array([80, 255, 255]))
    ],
    "blue": [
        (np.array([100, 150, 0]), np.array([140, 255, 255]))
    ]
}

selected_color = ["red"]

def color_gui():
    def set_color(c):
        selected_color[0] = c
        print(f"Renk değiştirildi: {c}")
    gui = tk.Tk()
    gui.title("Renk Seçimi")
    gui.geometry("300x300")
    tk.Button(gui, text="Kırmızı", font=("Arial", 14), width=20, command=lambda: set_color("red")).pack(pady=10)
    tk.Button(gui, text="Yeşil", font=("Arial", 14), width=20, command=lambda: set_color("green")).pack(pady=10)
    tk.Button(gui, text="Mavi", font=("Arial", 14), width=20, command=lambda: set_color("blue")).pack(pady=10)
    gui.mainloop()

# Arayüz başlat
t = Thread(target=color_gui, daemon=True)
t.start()

# Kamera başlat
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Motor kontrolünü oku
    motor_cmd = 'Z'
    if keyboard.is_pressed('w'):
        motor_cmd = 'W'
    elif keyboard.is_pressed('s'):
        motor_cmd = 'S'
    elif keyboard.is_pressed('a'):
        motor_cmd = 'A'
    elif keyboard.is_pressed('d'):
        motor_cmd = 'D'

    mask = None
    for lower, upper in color_ranges[selected_color[0]]:
        current_mask = cv2.inRange(hsv, lower, upper)
        mask = current_mask if mask is None else cv2.bitwise_or(mask, current_mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea, default=None)

    if largest_contour is not None and cv2.contourArea(largest_contour) > 500:
        (x, y, w, h) = cv2.boundingRect(largest_contour)
        cx = x + w // 2
        cy = y + h // 2
        data = f"{cx},{cy},{motor_cmd}\n"
        ser.write(data.encode('utf-8'))
        print(f"{selected_color[0].upper()} GÖNDERİLDİ: {data.strip()}")

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
    else:
        print(f"{selected_color[0].upper()} nesne bulunamadı.")
        data = f"320,240,{motor_cmd}\n"
        ser.write(data.encode('utf-8'))

    cv2.imshow("Color Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
