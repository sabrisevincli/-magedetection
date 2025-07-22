import cv2
import os
import numpy as np

base_path = r"C:\Users\smfse\OneDrive\Masaüstü\project_folder"
os.chdir(base_path)

dataset_path = "dataset"
if not os.path.exists(dataset_path):
    print("Dataset klasörü bulunamadı!")
    exit()

faces = []
labels = []
label_map = {}

for idx, person_name in enumerate(os.listdir(dataset_path)):
    label_map[idx] = person_name
    person_dir = os.path.join(dataset_path, person_name)
    for img_name in os.listdir(person_dir):
        img_path = os.path.join(person_dir, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            faces.append(img)
            labels.append(idx)

if not faces:
    print("Hiç yüz verisi bulunamadı!")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(labels))
recognizer.save("trainer.yml")

with open("labels.txt", "w") as f:
    for idx, name in label_map.items():
        f.write(f"{idx}:{name}\n")

print("Eğitim tamamlandı.")
