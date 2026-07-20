/*
  DRO — Dispatch Route Optimizer
  Прошивка датчика заполнения контейнера (ESP32 + HC-SR04)

  Логика:
  1. Просыпается из Deep Sleep каждые 30 минут.
  2. Замеряет расстояние до кучи сырья ультразвуковым датчиком.
  3. Считывает уровень заряда батареи.
  4. Отправляет данные на backend (HTTP POST) или в MQTT-брокер.
  5. Снова уходит в Deep Sleep.
*/

#include <WiFi.h>
#include <HTTPClient.h>

// ---- Настройки Wi-Fi и API ----
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* API_ENDPOINT = "http://YOUR_BACKEND_HOST:8000/api/bins/telemetry";
const int BIN_ID = 1; // уникальный ID контейнера, задается при установке

// ---- Пины датчика HC-SR04 ----
const int TRIG_PIN = 5;
const int ECHO_PIN = 18;
const int BATTERY_PIN = 34; // аналоговый вход для измерения напряжения батареи

// ---- Параметры бака ----
const float BIN_HEIGHT_CM = 100.0; // высота контейнера от датчика до дна
const uint64_t SLEEP_INTERVAL_US = 30ULL * 60ULL * 1000000ULL; // 30 минут

float measureDistanceCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // таймаут 30мс
  return duration * 0.0343 / 2.0; // скорость звука ~343 м/с
}

float readBatteryLevelPercent() {
  int raw = analogRead(BATTERY_PIN);
  float voltage = (raw / 4095.0) * 3.3 * 2; // делитель напряжения 1:1
  float percent = (voltage - 3.0) / (4.2 - 3.0) * 100.0; // диапазон Li-Ion 3.0–4.2В
  return constrain(percent, 0, 100);
}

void sendTelemetry(float fillPercent, float batteryPercent) {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(API_ENDPOINT);
  http.addHeader("Content-Type", "application/json");

  String payload = "{\"bin_id\":" + String(BIN_ID) +
                    ",\"fill_percent\":" + String(fillPercent, 1) +
                    ",\"battery_level\":" + String(batteryPercent, 1) + "}";

  int responseCode = http.POST(payload);
  Serial.printf("Telemetry sent. Response code: %d\n", responseCode);
  http.end();
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 15000) {
    delay(300);
  }

  float distanceCm = measureDistanceCm();
  float fillPercent = constrain((1.0 - (distanceCm / BIN_HEIGHT_CM)) * 100.0, 0, 100);
  float batteryPercent = readBatteryLevelPercent();

  Serial.printf("Fill: %.1f%%, Battery: %.1f%%\n", fillPercent, batteryPercent);

  sendTelemetry(fillPercent, batteryPercent);

  WiFi.disconnect(true);
  esp_sleep_enable_timer_wakeup(SLEEP_INTERVAL_US);
  esp_deep_sleep_start();
}

void loop() {
  // не используется: вся логика в setup(), т.к. плата уходит в Deep Sleep
}
