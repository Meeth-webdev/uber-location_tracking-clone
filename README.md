# 🚗 Uber Live Location Tracking Backend

Real-time driver location tracking system built with Django Channels and Redis Pub/Sub for Uber-like live tracking functionality.

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Channels](https://img.shields.io/badge/Django%20Channels-092E20?style=for-the-badge&logo=django&logoColor=white)](https://channels.readthedocs.io/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Core Features](#-core-features)
- [Technology Stack](#-technology-stack)
- [How It Works](#-how-it-works)
- [Key Components](#-key-components)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [WebSocket Protocol](#-websocket-protocol)
- [Data Models](#-data-models)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📋 Project Overview

Real-time driver location tracking system built with Django Channels and Redis Pub/Sub for Uber-like live tracking functionality. Customers can follow a driver's position live on a map while a ride is in progress, with every subscribed client receiving updates instantly.

---

## 🎯 Core Features

1. **Real-time driver location updates** — low-latency location streaming over WebSockets
2. **Live ride tracking for customers** — customers subscribe to a ride and watch the driver move
3. **WebSocket-based communication** — persistent bidirectional connections via Django Channels
4. **Redis Pub/Sub for message broadcasting** — efficient fan-out to all subscribers of a ride channel
5. **Location history persistence** — recent locations stored in MongoDB, latest position mirrored to the ORM
6. **Scalable architecture** — Redis pub/sub decouples publishers from subscribers so clients can scale horizontally

---

## 🏗️ Technology Stack

| Technology         | Purpose                            |
| ------------------ | ---------------------------------- |
| 🐍 Django           | Backend framework & ORM            |
| 🔌 Django Channels  | WebSocket handling (ASGI)          |
| 🎨 Redis            | Pub/Sub message broadcasting       |
| 🍃 MongoDB          | Location history storage (pymongo) |
| 🌐 ASGI             | Async application interface        |
| ⚡ Daphne / Uvicorn | ASGI server                        |

---

## 🔄 How It Works

```text
Customer books ride
      │
      ▼
WebSocket connection established ──► ws/ride/<ride_id>/
      │
      ▼
Driver sends location ──► published to Redis channel ride_<ride_id>
      │
      ▼
All subscribed users ◄── receive real-time updates
      │
      ▼
Location history persisted to MongoDB + ORM
```

---

## ⚡ Key Components

1. **Redis Pub/Sub** — broadcasts location updates to every client subscribed to a ride's channel
2. **Django Channels** — manages WebSocket connections and the consumer lifecycle
3. **Channel Layers** — group-based real-time communication between consumers
4. **LiveLocationService** — service layer that persists locations to MongoDB and syncs the latest position to the `DriverLocation` ORM model

---

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Redis** — running and reachable (default: `localhost:6379`)
- **MongoDB** — running and reachable (connection string configured via settings)
- **pip** (or any Python package manager)

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd uber

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install django channels channels-redis redis pymongo daphne
```

> **Note:** `settings.py` and `manage.py` are git-ignored in this repository. On a fresh clone, restore them from your environment or scaffold a Django project (`django-admin startproject uber`) before continuing.

---

## ⚙️ Configuration

The application reads configuration from Django settings. The following values are used by the codebase:

| Setting                  | Used by                     | Default / Notes                        |
| ------------------------ | --------------------------- | -------------------------------------- |
| `MONGO_DB_URI`           | `db_connection.py`          | MongoDB connection string              |
| `MONGO_DB_NAME`          | `db_connection.py`          | MongoDB database name                  |
| `CHANNEL_LAYERS`         | Channel layer communication | Redis-backed channel layer recommended |
| `DJANGO_SETTINGS_MODULE` | ASGI/WSGI entrypoints       | `uber.settings`                        |

**Redis** is currently configured in `redis_manager.py` to connect to `localhost:6379` (db `0`). MongoDB and Redis must both be running before starting the server.

---

## 🚀 Running the Application

The project is served as an ASGI application (`uber.asgi:application`). Use an ASGI server such as Daphne or Uvicorn:

```bash
# Using Daphne
daphne -b 0.0.0.0 -p 8000 uber.asgi:application

# Using Uvicorn
uvicorn uber.asgi:application --host 0.0.0.0 --port 8000
```

Then connect a WebSocket client to `ws://localhost:8000/ws/ride/<ride_id>/`.

---

## 🔌 WebSocket Protocol

**Endpoint:** `ws/ride/<ride_id>/`
**Consumer:** `OptimizedDriverLocationConsumer`

On connect, the consumer subscribes to the Redis channel `ride_<ride_id>`. Clients send JSON messages; a location update is published to Redis (and broadcast to all subscribers) when the message has:

```json
{
  "type": "location_update",
  "lat": 37.7749,
  "lng": -122.4194
}
```

Every message published on `ride_<ride_id>` is pushed back to all connected WebSocket clients for that ride.

---

## 🗄️ Data Models

| Model            | Description                                                                  |
| ---------------- | ---------------------------------------------------------------------------- |
| `User`           | Users with a `user_type` (customer/driver) and `phone_number`                |
| `Ride`           | Ride linking a customer and a driver, with a `status` (default: `requested`) |
| `DriverLocation` | Latest known driver position, with `last_updated` timestamp                  |

Recent location history is stored in the MongoDB collection `live_location` via `LiveLocationService`.

---

## 📁 Project Structure

```text
uber/
├── uber/                      # Django project package
│   ├── asgi.py                # ASGI entrypoint (uber.asgi:application)
│   ├── wsgi.py                # WSGI entrypoint
│   ├── settings.py            # Project settings (git-ignored)
│   └── urls.py                # HTTP routes (admin)
├── driver_location/           # Core tracking app
│   ├── routing.py             # WebSocket route: ws/ride/<ride_id>/
│   ├── consumers_redis.py     # OptimizedDriverLocationConsumer
│   ├── consumers.py           # Legacy channel-layer consumers (not routed)
│   ├── redis_manager.py       # Redis Pub/Sub manager (singleton)
│   ├── services.py            # LiveLocationService (MongoDB + ORM)
│   ├── db_connection.py       # MongoDB connection (singleton)
│   ├── models.py              # User, Ride, DriverLocation
│   └── tests.py               # Test suite
└── README.md
```

---

## 🧪 Testing

Run the test suite with Django's test runner:

```bash
python manage.py test
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This repository currently ships **no LICENSE file**, so usage terms are undefined. Add a `LICENSE` file to define the terms under which this project may be used.

---

**Built for scalable, real-time location tracking with efficient message broadcasting**.
