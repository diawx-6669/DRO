# Мост Arduino Uno → DRO backend

Arduino Uno не умеет в Wi-Fi, поэтому данные идут так:

```
HC-SR04 → Arduino Uno → USB-кабель → компьютер → Python-скрипт → интернет → Railway → карта
```

## Шаг 1. Прошей Uno

Открой `uno_sensor.ino` в Arduino IDE, подключи HC-SR04:
- `TRIG` → пин 9
- `ECHO` → пин 10
- `VCC` → 5V, `GND` → GND

Загрузи скетч на плату.

## Шаг 2. Найди свой Serial-порт

**Mac:**
```bash
ls /dev/tty.usb*
```
Обычно что-то вроде `/dev/tty.usbmodem14101` или `/dev/tty.usbserial-XXXX`.

**Windows:**
Диспетчер устройств → «Порты (COM и LPT)» → найди `COMx` (например `COM3`).

**Linux:**
```bash
ls /dev/ttyUSB* /dev/ttyACM*
```

## Шаг 3. Настрой и запусти мост

Открой `serial_bridge.py`, поменяй:
- `SERIAL_PORT` — на найденный в шаге 2
- `BIN_ID` — id контейнера из базы, к которому привязан этот датчик (1–8 — тестовые баки из `/api/bins/seed`)
- `BIN_HEIGHT_CM` — реальную высоту твоего контейнера в см

Затем:
```bash
pip install -r requirements.txt
python serial_bridge.py
```

Пока скрипт запущен и Arduino подключена — соответствующий бак на карте диспетчерской
будет обновляться реальными показаниями каждые 5 секунд.

## Важно

- Закрой Arduino IDE Serial Monitor перед запуском скрипта — один порт не может
  использовать сразу два приложения.
- Если хочешь несколько датчиков одновременно — запусти несколько копий скрипта
  с разными `SERIAL_PORT` и `BIN_ID`.
