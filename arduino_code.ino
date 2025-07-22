#include <Servo.h>

Servo servoX;
Servo servoY;

String inputString = "";

const int frameWidth = 640;
const int frameHeight = 480;

// Motor pinleri
const int IN1 = 2;
const int IN2 = 3;
const int IN3 = 4;
const int IN4 = 5;
const int ENA = 6;
const int ENB = 11;

void setup() {
  Serial.begin(9600);
  servoX.attach(9);
  servoY.attach(10);

  // Servolar başlangıçta ortaya
  servoX.write(90);
  servoY.write(90);

  // Motor pin çıkış
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  Serial.println("Servo ve motor sistemi başlatıldı.");
}

void loop() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      processInput(inputString);
      inputString = "";
    } else {
      inputString += inChar;
    }
  }
}

void processInput(String data) {
  data.trim();
  int firstComma = data.indexOf(',');
  int secondComma = data.indexOf(',', firstComma + 1);

  if (firstComma > 0 && secondComma > firstComma) {
    int posX = data.substring(0, firstComma).toInt();
    int posY = data.substring(firstComma + 1, secondComma).toInt();
    char motorCommand = data.charAt(secondComma + 1);

    int servoPosX = map(posX, 0, frameWidth, 0, 180);
    int servoPosY = map(posY, 0, frameHeight, 0, 180);
    servoX.write(servoPosX);
    servoY.write(servoPosY);

    Serial.print("ServoX: ");
    Serial.print(servoPosX);
    Serial.print(" | ServoY: ");
    Serial.print(servoPosY);
    Serial.print(" | Motor: ");
    Serial.println(motorCommand);

    controlMotor(motorCommand);
  }
}

void controlMotor(char cmd) {
  if (cmd == 'W') {
    // İleri
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENA, 100);
    analogWrite(ENB, 100);
  } else if (cmd == 'S') {
    // Geri
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENA, 100);
    analogWrite(ENB, 100);
  } else if (cmd == 'A') {
    // Sol
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENA, 100);
    analogWrite(ENB, 100);
  } else if (cmd == 'D') {
    // Sağ
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENA, 100);
    analogWrite(ENB, 100);
  } else {
    // Dur
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
  }
}
