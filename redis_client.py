import redis
from config.settings import REDIS_URL

redis_client = redis.Redis(host=REDIS_URL)