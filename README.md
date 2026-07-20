# DRO — Dispatch Route Optimizer

Веб-платформа (диспетчерская панель) для оптимизации логистики сбора вторичного сырья.

Проект подготовлен для Республиканского молодежного хакатона «Tech Vision 2026»
(направление Smart City & GreenTech, трек Waste Management).

## Структура репозитория

```
├── backend/               # Серверная часть (Python / FastAPI)
│   ├── app/
│   │   ├── api/           # Эндпоинты для датчиков и фронтенда
│   │   ├── core/          # Настройки и конфигурации
│   │   ├── db/             # Миграции и модели базы данных (PostgreSQL + PostGIS)
│   │   └── services/      # Алгоритм оптимизации (VRP solver, OR-Tools)
│   ├── requirements.txt
│   └── main.py
│
├── frontend/              # Клиентская часть (React)
│   ├── public/
│   ├── src/
│   │   ├── components/    # Карта, карточка бака, аналитика
│   │   ├── hooks/         # Кастомные хуки для запросов к API
│   │   ├── store/         # Redux Toolkit
│   │   └── App.jsx
│   ├── package.json
│   └── README.md
│
├── hardware_iot/          # Прошивка для ESP32
│   └── esp32_sensor/
│       └── esp32_sensor.ino
│
├── docs/                  # Техническая документация
└── README.md
```

## Быстрый старт

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### IoT-прошивка

Откройте `hardware_iot/esp32_sensor/esp32_sensor.ino` в Arduino IDE,
укажите SSID/пароль Wi-Fi и адрес API-эндпоинта, загрузите на плату ESP32.

## Стек технологий

- **Frontend**: React.js, Leaflet.js / Mapbox GL JS, Redux Toolkit
- **Backend**: Python, FastAPI, SciPy / OR-Tools (VRP)
- **IoT**: ESP32 + HC-SR04, MQTT (Eclipse Mosquitto) или HTTP POST
- **DB**: PostgreSQL + PostGIS, TimescaleDB (логи датчиков)
