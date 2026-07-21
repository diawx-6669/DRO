/*
  DRO — прошивка для Arduino Uno + HC-SR04
  (без Wi-Fi — Uno его не поддерживает)

  Каждую секунду измеряет расстояние до кучи мусора и печатает
  одно число в Serial. Дальше это число забирает Python-скрипт
  serial_bridge.py и сам отправляет на сервер по интернету.
*/

const int TRIG_PIN = 9;
const int ECHO_PIN = 10;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // таймаут 30мс
  float distanceCm = duration * 0.0343 / 2.0;

  Serial.println(distanceCm, 1); // одно число, один знак после запятой

  delay(1000);
}
