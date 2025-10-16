# 🚗 Uber Live Location Tracking Backend 


## 📋 Project Overview
Real-time driver location tracking system built with Django Channels and Redis Pub/Sub for Uber-like live tracking functionality.

## 🏗️ Technology Stack
-🐍 Django - Backend Framework

-🔌 Django Channels - WebSocket Handling

-🎨 Redis - Pub/Sub Messaging

-🌐 ASGI - Async Support

-🎯 Core Features

1)Real-time driver location updates

2)Live ride tracking for customers

3)WebSocket-based communication

4)Redis Pub/Sub for message broadcasting


# 🔄 How It Works
Customer books ride → WebSocket connection established

Driver sends location → Published to Redis channel

All subscribed users → Receive real-time updates

Live tracking → Continuous location streaming

⚡ Key Components

1)Redis Pub/Sub - Broadcasts location to multiple clients

2)Django Channels - Handles WebSocket connections

3)Channel Layers - Manages real-time communication


 **Built for scalable, real-time location tracking with efficient message broadcasting**.
