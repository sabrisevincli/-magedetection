import cv2
import os
from ultralytics import YOLO

# Sabit klasör
base_path = r"C:\Users\smfse\OneDrive\Masaüstü\project_folder"
os.chdir(base_path)

# YOLO modeli yükle
model = YOLO("yolov8n.pt")
class_names = model.names

# Kamera başlat
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    results = model(frame)

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0].item())
            cls_name = class_names[cls_id]
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(frame, cls_name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("YOLOv8 Full Detection (Görüntü Üzerinde)", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
