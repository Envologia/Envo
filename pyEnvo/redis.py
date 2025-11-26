# Envo Userbot - Redis Utility
# Created by @envologia

import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URI = os.getenv("REDIS_URI")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

def get_redis_connection():
    if not REDIS_URI or not REDIS_PASSWORD:
        raise ValueError("Redis URI and password are not set.")

    return redis.Redis.from_url(REDIS_URI, password=REDIS_PASSWORD, decode_responses=True)

try:
    r = get_redis_connection()
    r.ping()
except (ValueError, redis.exceptions.ConnectionError) as e:
    r = None
    print(f"Could not connect to Redis: {e}")

def redis_client():
    return r
