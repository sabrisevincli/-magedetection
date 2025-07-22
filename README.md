Image processing ile servo motorlu hedef takip sistemi
# Bitirme Projesi: Servo Takipli Robot Araba

## 🎯 Proje Amacı
Görüntü işleme (image processing) kullanarak nesne takibi yapan, servo motorlarla yön değiştiren bir robot araba tasarlandı.

## ⚙️ Kullanılan Teknolojiler
- Arduino UNO
- Python (OpenCV)
- Servo motor (SG90)
- Telefon kamerası ip görüntü paylaşarak alındı.
- L298N motor sürücü
- Şasi
- Motorlar
- HC-05 bluetooth modülü

## 🔧 Çalışma Prensibi
Kamera görüntüsünden renk/nesne algılanır → Python işleme yapar → Seri port bluetooth ile ile Arduino'ya veri gönderilir Ser → Servo yönlendirir.


## 👤 Geliştirici
**Sabri Sevinçli** 
**Emre Yağcı** 
**Bünyamin Eren** 
**Tayfun Karataş** 
– Marmara Üniversitesi, Elektronik Teknolojisi

# Graduation Project: Servo-Based Object Tracking Robot Car

## 🎯 Project Objective  
A robot car was designed to track objects using image processing and to steer using servo motors.

## ⚙️ Technologies Used  
- Arduino UNO  
- Python (OpenCV)  
- Servo Motor (SG90)  
- Smartphone camera (video stream via IP)  
- L298N Motor Driver  
- Chassis  
- DC Motors  
- HC-05 Bluetooth Module  

## 🔧 Working Principle  
The smartphone camera captures video, and color/object detection is performed via Python using OpenCV.  
The processed tracking data is sent over Bluetooth (HC-05) to the Arduino via serial communication.  
The Arduino controls the servo motors to follow the detected object accordingly.

## 👤 Developers  
**Sabri Sevinçli** – Marmara University, Department of Electronic Technology  
**Emre Yağcı** – Marmara University, Department of Electronic Technology  
**Bünyamin Eren** – Marmara University, Department of Electronic Technology  
**Tayfun Karataş** – Marmara University, Department of Electronic Technology



