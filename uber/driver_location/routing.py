# ride_app/routing.py
from django.urls import re_path
from . import consumers_redis

websocket_urlpatterns = [
    re_path(r'ws/ride/(?P<ride_id>\w+)/$', consumers_redis.OptimizedDriverLocationConsumer.as_asgi()),
  
]
