# 🚗 Uber Live Location Tracking Backend

Real-time driver location tracking system built with Django Channels and Redis Pub/Sub for Uber-like live tracking functionality. Drivers push GPS coordinates over WebSockets, updates are broadcast instantly via Redis pub/sub, and location history is persisted to MongoDB while structured data lives in Django ORM models.

## 📋 Project Overview

- 🚗 Built for a ride-booking system — drivers stream GPS coordinates while customers track rides live
- 📡 Real-time delivery over WebSockets with Redis pub/sub fan-out
- 💾 Dual persistence — structured data (users, rides, locations) in Django ORM; location history in MongoDB
- 🔌 Django Channels handles the WebSocket protocol over ASGI

## 🏗️ Technology Stack

- 🐍 **Python / Django 5.x** — backend framework
- 🔌 **Django Channels** — WebSocket handling over ASGI
- 🎨 **Redis** — pub/sub messaging between connected clients
- 🍃 **MongoDB** — durable location-history storage
- 🗄️ **Django ORM** — users, rides, and structured location records

> 📦 Dependency versions are not pinned in this repository: `manage.py`, `settings.py`, and dependency manifests are **git-ignored**, so the checkout contains application code only.

## ⚙️ How It Works

1. **Connect** — A driver opens `ws/ride/<ride_id>/`; the routing layer hands the socket to `OptimizedDriverLocationConsumer`
2. **Subscribe** — On connect, the consumer subscribes to the Redis channel for that ride (`ride_{ride_id}`)
3. **Publish** — Driver location updates are published to the ride's Redis channel
4. **Broadcast** — The Redis manager fans each update out to every subscriber of the ride, so all connected clients receive updates in real time
5. **Persist** — Each location is written to MongoDB in a background thread, building durable history
6. **Query** — The service layer exposes current and recent location queries (not part of the wired runtime path); structured records come from Django ORM

Note the real-time path runs through the Redis consumer and `Redis_Manager`; `LiveLocationService` runs on the persistence path inside the background write thread, and the channel-layer consumers in `consumers.py` are not wired by the current routing.

## 📁 Project Layout

```
uber/
├── uber/                        # Django project package
│   ├── asgi.py                  # ASGI entrypoint — Channels serves WebSockets here
│   ├── wsgi.py                  # WSGI entrypoint
│   └── urls.py                  # URL configuration
└── driver_location/             # Core Django app
    ├── models.py                # User, Ride, DriverLocation ORM models
    ├── routing.py               # ws/ride/<ride_id>/ → Redis-backed consumer
    ├── consumers_redis.py       # WebSocket consumer backed by Redis pub/sub
    ├── consumers.py             # Channel-layer consumers (not wired by routing)
    ├── redis_manager.py         # Redis pub/sub + threaded MongoDB persistence
    ├── services.py              # LiveLocationService — store/read locations
    ├── db_connection.py         # MongoDB connection singleton
    ├── driver_views.py          # HTTP views (stub)
    ├── admin.py                 # Django admin (default scaffold — no models registered)
    ├── tests.py                 # Test stubs
    └── migrations/              # Django migrations (package only — none committed)
```

## 🔧 Configuration Prerequisites

The application code is committed here, but running it requires the following services and settings. `manage.py`, `settings.py`, and dependency manifests are **git-ignored** — this checkout is application code only.

**Required services**

- 🎨 **Redis** — pub/sub transport (the app connects to a local Redis instance)
- 🍃 **MongoDB** — location-history store (URI configured via Django settings)

**Required Django settings** (in the git-ignored `settings.py`)

- `SECRET_KEY`, `DATABASE_URL` — core Django configuration
- `MONGO_DB_URI`, `MONGO_DB_NAME` — MongoDB connection

Suggested dependencies: Django 5.x with `channels`, `redis`, and `pymongo`.

## 📚 Further Reading

The project wiki goes deeper on architecture and conventions:

- **Repository Overview** — purpose, key concepts, and the dual-persistence strategy
- **System Architecture** — component map and communication patterns
- **Driver Location Tracking** — detailed walkthrough of the live-location flow

**Built for scalable, real-time location tracking with efficient message broadcasting**.
