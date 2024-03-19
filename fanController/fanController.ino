const int FAN_LEFT_PIN = 3;
const int FAN_RIGHT_PIN = 6;
const int FAN_LEFT_MIN = 10;
const int FAN_LEFT_MAX = 255;
const int FAN_RIGHT_MIN = 10;
const int FAN_RIGHT_MAX = 255;

void setup() {
  Serial.begin(9600);
  pinMode(FAN_LEFT_PIN, OUTPUT);
  pinMode(FAN_RIGHT_PIN, OUTPUT);
}

void loop() {
   if (Serial.available() > 0) {
    int speed = Serial.parseInt();
    Serial.read();
    setFanSpeed(speed, FAN_LEFT_MIN, FAN_LEFT_MAX, FAN_LEFT_PIN);
    setFanSpeed(speed, FAN_RIGHT_MIN, FAN_RIGHT_MAX, FAN_RIGHT_PIN);
  }
  delay(100);
}

void setFanSpeed(int percent, int min, int max, int pin){
  int percentClamped = clamp(percent, 0, 100);
  int pwm = map(percentClamped, 0, 100, min, max);
  analogWrite(pin, pwm);
}

int clamp(int value, int minVal, int maxVal) {
  if (value < minVal) {
    return minVal;
  } else if (value > maxVal) {
    return maxVal;
  } else {
    return value;
  }
}
