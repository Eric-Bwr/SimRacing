const int FAN_PIN = 3;
const int FAN_MIN = 100;
const int FAN_MAX = 255;

void setup() {
  Serial.begin(9600);
  pinMode(FAN_PIN, OUTPUT);
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
  int pwm = map(percentClamped, 0, 100, FAN_MIN, FAN_MAX);
  
  if (pwm < 5) {
    pwm = 5;
  }
  
  analogWrite(FAN_PIN, pwm);
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