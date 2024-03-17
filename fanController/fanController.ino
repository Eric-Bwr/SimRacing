const int FAN_LEFT_PIN = 3;
const int FAN_RIGHT_PIN = 6;
const int FAN_LEFT_MIN = 60;
const int FAN_LEFT_MAX = 255;
const int FAN_RIGHT_MIN = 10;
const int FAN_RIGHT_MAX = 220;

void setup() {
  Serial.begin(9600);
  pinMode(FAN_LEFT_PIN, OUTPUT);
  pinMode(FAN_RIGHT_PIN, OUTPUT);
}

void loop() {
   if (Serial.available() > 0) {
    int speed = Serial.parseInt();
    Serial.read();
    setFanSpeed(speed);
  }
  delay(100);
}

void setFanSpeed(int percent){
  int percentClamped = clamp(percent, 0, 100);
  int pwm = map(percentClamped, 0, 100, FAN_LEFT_MIN, FAN_LEFT_MAX);
  
  analogWrite(FAN_LEFT_PIN, pwm);

  percentClamped = clamp(percent, 0, 100);
  pwm = map(percentClamped, 0, 100, FAN_RIGHT_MIN, FAN_RIGHT_MAX);

  analogWrite(FAN_RIGHT_PIN, pwm);
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