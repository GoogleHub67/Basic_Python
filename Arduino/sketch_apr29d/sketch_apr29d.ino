#include <Servo.h>
Servo lidServo;
int trigPin = 9;
int echoPin = 10;
int servoPin = 11;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  lidServo.attach(servoPin);
  lidServo.write(0); // Closed
}

void loop() {
  long duration;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.034 / 2;
  
  if (distance < 30) {
    lidServo.write(90); // Open
    delay(3000);
    lidServo.write(0); // Close
  }
  delay(500);
}