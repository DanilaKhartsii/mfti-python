import json
import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def cache_get(key: str):
    data = redis_client.get(key)
    if data is None:
        return None
    return json.loads(data)


def cache_set(key: str, value, expire: int = 60):
    redis_client.set(key, json.dumps(value), ex=expire)


def cache_delete_pattern(pattern: str):
    for key in redis_client.scan_iter(pattern):
        redis_client.delete(key)
