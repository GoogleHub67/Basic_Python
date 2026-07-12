#include <Servo.h>

Servo lidServo;  // Creates servo object
int trigPin = 5; // Ultrasonic trigger pin
int echoPin = 6; // Ultrasonic echo pin  
int servoPin = 9; // Servo signal pin

void setup() {
  pinMode(trigPin, OUTPUT);  // Trigger as output
  pinMode(echoPin, INPUT);   // Echo as input
  lidServo.attach(servoPin); // Attach servo
  lidServo.write(0);         // Lid starts closed (0 degrees)
  Serial.begin(9600);        // For debugging (optional)
}

void loop() {
  // Send ultrasonic pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Read echo time
  long duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.034 / 2; // Convert to cm
  
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
  
  // Open lid if hand < 30cm
  if (distance < 30 && distance > 0) {
    lidServo.write(90);  // Open lid (90 degrees)
    delay(3000);         // Keep open 3 seconds
    lidServo.write(0);   // Close lid
  }
  
  delay(500);  // Check every half second
}