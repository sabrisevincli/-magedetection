import cv2
import os
import sys

base_path = r"C:\Users\smfse\OneDrive\Masaüstü\project_folder"
os.chdir(base_path)

if len(sys.argv) < 2:
    print("İsim parametresi verilmedi!")
    exit()

name = sys.argv[1]
path = os.path.join("dataset", name)
os.makedirs(path, exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
count = 0

while count < 100:
    ret, frame = cap.read()
    if not ret:
        continue
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200, 200))
        cv2.imwrite(f"{path}/{count}.jpg", roi)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"{count}/100", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        break

    cv2.imshow("Collecting Faces", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
