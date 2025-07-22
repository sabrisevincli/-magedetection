import cv2
import serial
import time
import os
import tkinter as tk
from threading import Thread
from ultralytics import YOLO
import keyboard

# Seri Port (COM3)
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# Sabit klasör
base_path = r"C:\Users\smfse\OneDrive\Masaüstü\project_folder"
os.chdir(base_path)

# YOLO modeli yükle
model = YOLO("yolov8n.pt")
class_names = model.names
selected_class = [list(class_names.values())[0]]

# Seçim arayüzü (scroll bar)
def gui_thread():
    def set_target(name):
        selected_class[0] = name
        print(f"Seçilen sınıf: {name}")

    gui = tk.Tk()
    gui.title("YOLO Nesne Seçimi")
    gui.geometry("300x500")

    canvas = tk.Canvas(gui)
    scrollbar = tk.Scrollbar(gui, orient="vertical", command=canvas.yview)
    frame = tk.Frame(canvas)

    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for idx in class_names:
        btn = tk.Button(frame, text=class_names[idx], width=30, command=lambda n=class_names[idx]: set_target(n))
        btn.pack(pady=2)

    gui.mainloop()

# GUI thread başlat
t = Thread(target=gui_thread, daemon=True)
t.start()

# Kamera başlat
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    results = model(frame)

    motor_cmd = 'Z'
    if keyboard.is_pressed('w'):
        motor_cmd = 'W'
    elif keyboard.is_pressed('s'):
        motor_cmd = 'S'
    elif keyboard.is_pressed('a'):
        motor_cmd = 'A'
    elif keyboard.is_pressed('d'):
        motor_cmd = 'D'

    found = False

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0].item())
            cls_name = class_names[cls_id]

            if cls_name == selected_class[0]:
                found = True
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                data = f"{cx},{cy},{motor_cmd}\n"
                ser.write(data.encode('utf-8'))
                print(f"{cls_name.upper()} GÖNDERİLDİ: {data.strip()}")

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, cls_name, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                break

    if not found:
        print("Seçilen nesne bulunamadı, servo komut gönderilmiyor.")
        data = f"320,240,{motor_cmd}\n"
        ser.write(data.encode('utf-8'))

    cv2.imshow("YOLO Object Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
