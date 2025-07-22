import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import shutil

base_path = r"C:\Users\smfse\OneDrive\Masaüstü\project_folder"
current_process = None

def stop_current():
    global current_process
    if current_process and current_process.poll() is None:
        current_process.terminate()
        current_process = None

def run_collect():
    stop_current()
    popup = tk.Toplevel(root)
    popup.title("Collect")
    popup.geometry("300x200")

    tk.Label(popup, text="İsim giriniz:").pack(pady=10)
    entry = tk.Entry(popup)
    entry.pack(pady=10)

    def start():
        name = entry.get().strip()
        if not name:
            messagebox.showwarning("Uyarı", "İsim giriniz.")
            return
        global current_process
        current_process = subprocess.Popen(
            ["python", os.path.join(base_path, "collect.py"), name],
            cwd=base_path
        )
        popup.destroy()

    tk.Button(popup, text="Başla", command=start).pack(pady=10)

def run_train():
    stop_current()
    global current_process
    current_process = subprocess.Popen(
        ["python", os.path.join(base_path, "train.py")],
        cwd=base_path
    )

def run_detect():
    stop_current()
    global current_process
    current_process = subprocess.Popen(
        ["python", os.path.join(base_path, "detect.py")],
        cwd=base_path
    )

def run_tracking():
    stop_current()
    global current_process
    current_process = subprocess.Popen(
        ["python", os.path.join(base_path, "tracking.py")],
        cwd=base_path
    )

def run_color_tracking():
    stop_current()
    global current_process
    current_process = subprocess.Popen(
        ["python", os.path.join(base_path, "color_tracking.py")],
        cwd=base_path
    )

def run_yolo_object_tracking():
    stop_current()
    global current_process
    current_process = subprocess.Popen(
        ["python", os.path.join(base_path, "yolo_object_tracking.py")],
        cwd=base_path
    )

def run_yolo_full_detection():
    stop_current()
    global current_process
    current_process = subprocess.Popen(
        ["python", os.path.join(base_path, "yolo_full_detection.py")],
        cwd=base_path
    )

def run_reset():
    stop_current()
    dataset_path = os.path.join(base_path, "dataset")
    trainer_path = os.path.join(base_path, "trainer.yml")
    label_path = os.path.join(base_path, "labels.txt")
    if os.path.exists(dataset_path):
        shutil.rmtree(dataset_path)
    if os.path.exists(trainer_path):
        os.remove(trainer_path)
    if os.path.exists(label_path):
        os.remove(label_path)
    os.makedirs(dataset_path, exist_ok=True)
    messagebox.showinfo("Reset", "Tüm veriler sıfırlandı.")

root = tk.Tk()
root.title("Yüz & Nesne Takip Sistemi")
root.geometry("400x800")

tk.Label(root, text="Kontrol Paneli", font=("Arial", 16, "bold")).pack(pady=20)

tk.Button(root, text="Collect", width=25, height=2, command=run_collect).pack(pady=5)
tk.Button(root, text="Train", width=25, height=2, command=run_train).pack(pady=5)
tk.Button(root, text="Detect (Yüz)", width=25, height=2, command=run_detect).pack(pady=5)
tk.Button(root, text="Tracking (Klasik)", width=25, height=2, command=run_tracking).pack(pady=5)
tk.Button(root, text="Color Tracking (Renk)", width=25, height=2, command=run_color_tracking).pack(pady=5)
tk.Button(root, text="YOLOv8 Object Tracking (Servo)", width=25, height=2, command=run_yolo_object_tracking).pack(pady=5)
tk.Button(root, text="YOLOv8 Full Detection (Görüntü)", width=25, height=2, command=run_yolo_full_detection).pack(pady=5)
tk.Button(root, text="Reset", width=25, height=2, command=run_reset).pack(pady=5)

root.mainloop()
