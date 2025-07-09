# utils/redis_helper.py

from django.core.cache import cache
import json
import logging

logger = logging.getLogger(__name__)

class RedisHelper:import json
from django_redis import get_redis_connection

class RedisHelper:
    def __init__(self):
        self.redis = get_redis_connection("default")

    # ----- STRING -----
    def set_string(self, key, value):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.redis.set(key, value)

    def get_string(self, key):
        val = self.redis.get(key)
        try:
            return json.loads(val)
        except:
            return val.decode() if val else None

    def delete_key(self, key):
        self.redis.delete(key)

    # ----- HASH -----
    def set_hash(self, key, data: dict):
        self.redis.hset(key, mapping=data)

    def get_hash(self, key):
        data = self.redis.hgetall(key)
        return {k.decode(): v.decode() for k, v in data.items()}

    def get_hash_field(self, key, field):
        value = self.redis.hget(key, field)
        return value.decode() if value else None

    def delete_hash_field(self, key, field):
        self.redis.hdel(key, field)

    # ----- LIST -----
    def push_list(self, key, values):
        if isinstance(values, list):
            self.redis.rpush(key, *values)
        else:
            self.redis.rpush(key, values)

    def get_list(self, key):
        return [item.decode() for item in self.redis.lrange(key, 0, -1)]

    def pop_list(self, key):
        value = self.redis.rpop(key)
        return value.decode() if value else None


    @staticmethod
    def set(key, value, timeout=None):
        """Set a value in Redis cache."""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            cache.set(key, value, timeout)
            return True
        except Exception as e:
            logger.error(f"Redis SET error: {e}")
            return False

    @staticmethod
    def get(key, as_json=False):
        """Get a value from Redis cache."""
        try:
            value = cache.get(key)
            if value and as_json:
                return json.loads(value)
            return value
        except Exception as e:
            logger.error(f"Redis GET error: {e}")
            return None

    @staticmethod
    def delete(key):
        """Delete a value from Redis cache."""
        try:
            cache.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis DELETE error: {e}")
            return False

    @staticmethod
    def has_key(key):
        """Check if a key exists in Redis cache."""
        return cache.get(key) is not None

    @staticmethod
    def incr(key, delta=1):
        """Increment a counter stored in Redis."""
        try:
            return cache.incr(key, delta)
        except Exception as e:
            logger.error(f"Redis INCR error: {e}")
            return None

    @staticmethod
    def decr(key, delta=1):
        """Decrement a counter stored in Redis."""
        try:
            return cache.decr(key, delta)
        except Exception as e:
            logger.error(f"Redis DECR error: {e}")
            return None
