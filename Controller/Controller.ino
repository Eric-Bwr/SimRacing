const int FAN_LEFT_PIN = 3;
const int FAN_RIGHT_PIN = 6;

const int FAN_LEFT_MIN = 20;
const int FAN_LEFT_MAX = 255;
const int FAN_RIGHT_MIN = 20;
const int FAN_RIGHT_MAX = 255;

const int VIBE_LPWM_PIN = 9;
const int VIBE_RPWM_PIN = 10;
const int VIBE_MIN = 0;
const int VIBE_MAX = 255;

void setup() {
  Serial.begin(9600);
  pinMode(FAN_LEFT_PIN, OUTPUT);
  pinMode(FAN_RIGHT_PIN, OUTPUT);
  pinMode(VIBE_LPWM_PIN, OUTPUT);
  pinMode(VIBE_RPWM_PIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    int commaIndex = input.indexOf(',');
    if (commaIndex > 0) {
      int speed = input.substring(0, commaIndex).toInt();
      int rpm = input.substring(commaIndex + 1).toInt();
      setSpeed(speed, FAN_LEFT_MIN, FAN_LEFT_MAX, FAN_LEFT_PIN);
      setSpeed(speed, FAN_RIGHT_MIN, FAN_RIGHT_MAX, FAN_RIGHT_PIN);

      setSpeed(rpm, VIBE_MIN, VIBE_MAX, VIBE_LPWM_PIN);
      analogWrite(VIBE_RPWM_PIN, 0);
    }
  }
  delay(100);
}

void setSpeed(int percent, int min, int max, int pin) {
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
