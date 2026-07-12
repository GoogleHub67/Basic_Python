#include <Servo.h>
Servo lidServo;
int trigPin = 5, echoPin = 6, servoPin = 9;

void setup() {
  pinMode(trigPin, OUTPUT); pinMode(echoPin, INPUT);
  lidServo.attach(servoPin); lidServo.write(0);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trigPin, LOW); delayMicroseconds(2);
  digitalWrite(trigPin, HIGH); delayMicroseconds(10); digitalWrite(trigPin, LOW);
  int distance = pulseIn(echoPin, HIGH) * 0.034 / 2;
  
  Serial.println(distance);
  if (distance < 30 && distance > 0) {
    lidServo.write(90); delay(3000); lidServo.write(0);
  }
  delay(500);
}