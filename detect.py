import cv2
import serial
import time
import numpy as np
import os
import tkinter as tk
from threading import Thread
import keyboard

# COM3 üzerinden seri port
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# Sabit klasör yolu
base_path = r"C:\Users\smfse\OneDrive\Masaüstü\project_folder"
os.chdir(base_path)

# Model ve etiket kontrolü
if not os.path.exists("trainer.yml") or not os.path.exists("labels.txt"):
    print("Model veya label dosyası eksik!")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# Etiketleri oku
label_map = {}
with open("labels.txt", "r") as f:
    for line in f:
        idx, name = line.strip().split(":")
        label_map[int(idx)] = name

selected_person = [list(label_map.values())[0]]
switching = [False]
last_switch_time = [0]

def gui_thread():
    def change_target(name):
        if selected_person[0] != name:
            selected_person[0] = name
            switching[0] = True
            last_switch_time[0] = time.time()
            print(f"Kişi değişti: {name}")
    gui = tk.Tk()
    gui.title("Kişi Seçimi")
    for name in label_map.values():
        btn = tk.Button(gui, text=name, width=20, height=2, command=lambda n=name: change_target(n))
        btn.pack(pady=5)
    gui.mainloop()

t = Thread(target=gui_thread, daemon=True)
t.start()

# Kamera aç
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Klavyeden motor kontrolü:
    motor_cmd = 'Z'
    if keyboard.is_pressed('w'):
        motor_cmd = 'W'
    elif keyboard.is_pressed('s'):
        motor_cmd = 'S'
    elif keyboard.is_pressed('a'):
        motor_cmd = 'A'
    elif keyboard.is_pressed('d'):
        motor_cmd = 'D'

    if switching[0]:
        if time.time() - last_switch_time[0] < 0.2:
            cv2.imshow("Detect", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
            continue
        else:
            switching[0] = False

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    target_found = False

    for (x, y, w, h) in faces:
        roi = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
        id_, conf = recognizer.predict(roi)
        name = label_map[id_] if conf < 80 else "Unknown"

        if name == selected_person[0]:
            target_found = True
            cx = x + w//2
            cy = y + h//2
            data = f"{cx},{cy},{motor_cmd}\n"
            ser.write(data.encode('utf-8'))
            print(f"GÖNDERİLEN: {data.strip()}")

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            break

    if not target_found:
        print("Seçilen kişi bulunamadı, servo komut gönderilmiyor.")
        data = f"320,240,{motor_cmd}\n"
        ser.write(data.encode('utf-8'))  # Ortada beklet servo yine motor hareketi devam etsin

    cv2.imshow("Detect", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
