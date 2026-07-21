"""
DRO — мост между Arduino Uno (по USB) и backend на Railway.

Что делает:
1. Слушает Serial-порт, куда Uno шлёт одно число в секунду (расстояние в см).
2. Переводит расстояние в % заполнения контейнера.
3. Раз в 5 секунд отправляет POST на backend — /api/bins/telemetry.

Запуск:
    pip install pyserial requests
    python serial_bridge.py

Компьютер с подключённым по USB Arduino должен быть включён
и скрипт запущен всё то время, пока нужны живые данные на карте.
"""

import re
import time

import requests
import serial

# --- Настройки: поменяй под себя ---

SERIAL_PORT = "/dev/tty.usbmodem14101"  # см. инструкцию ниже, как найти свой порт
BAUD_RATE = 9600

BIN_ID = 1  # id контейнера в БД, к которому привязан этот датчик (1-8 — тестовые баки)
BIN_HEIGHT_CM = 100.0  # высота контейнера от датчика до дна — подставь свою

API_URL = "https://dro-production.up.railway.app/api/bins/telemetry"
SEND_INTERVAL_SEC = 5  # не спамим backend чаще, чем раз в 5 секунд


def distance_to_fill_percent(distance_cm: float) -> float:
    percent = (1 - distance_cm / BIN_HEIGHT_CM) * 100
    return max(0.0, min(100.0, percent))


def main():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    time.sleep(2)  # ждём, пока Arduino перезагрузится после открытия порта

    print(f"Слушаю {SERIAL_PORT}, отправляю на {API_URL} (bin_id={BIN_ID})")

    last_sent = 0.0

    while True:
        raw_line = ser.readline().decode("utf-8", errors="ignore").strip()
        match = re.search(r"-?\d+(\.\d+)?", raw_line)
        if not match:
            continue

        distance_cm = float(match.group(0))
        fill_percent = distance_to_fill_percent(distance_cm)

        now = time.time()
        if now - last_sent < SEND_INTERVAL_SEC:
            continue
        last_sent = now

        try:
            response = requests.post(
                API_URL,
                json={
                    "bin_id": BIN_ID,
                    "fill_percent": round(fill_percent, 1),
                    "battery_level": 100.0,  # Uno от розетки/USB, батареи нет — шлём заглушку
                },
                timeout=5,
            )
            print(
                f"Расстояние: {distance_cm:.1f} см -> заполнение: {fill_percent:.1f}% "
                f"| ответ сервера: {response.status_code}"
            )
        except requests.RequestException as e:
            print(f"Не удалось отправить данные: {e}")


if __name__ == "__main__":
    main()
