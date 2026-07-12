#include <Servo.h>

Servo lidServo;
int trigPin = 5;  // HC-SR04 Trigger → D5
int echoPin = 6;  // HC-SR04 Echo → D6
int servoPin = 9; // SG90 Signal → D9

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  lidServo.attach(servoPin);
  lidServo.write(0);  // Lid closed
  Serial.begin(9600); // Debug monitor
}

void loop() {
  // Ultrasonic pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.034 / 2;
  
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println("cm");
  
  // Open if hand < 30cm
  if (distance < 30 && distance > 0) {
    lidServo.write(90);  // Open lid
    delay(3000);         // Wait 3 sec
    lidServo.write(0);   // Close lid
  }
  
  delay(500);  // Check 2x per second
}