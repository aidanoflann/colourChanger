import os

REDIS_URL = os.getenv("APP_REDIS_URL", "localhost")
REDIS_PORT = os.getenv("APP_REDIS_PORT", 6379)
