import os
import redis
import pickle
from functools import wraps

def get_redis():
    try:
        r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=os.getenv('REDIS_DB'))
        r.ping()  # Check if Redis is available
        print("Connected to Redis. Caching is enabled.")
        return r
    except:
        print("Cannot connect to Redis. Caching will be disabled.")
        return None

r = get_redis()

def cache_it_sync(timeout=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if r is not None:
                key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                result = r.get(key)
                if result is not None:
                    return pickle.loads(result)
            result = func(*args, **kwargs)
            if r is not None:
                r.set(key, pickle.dumps(result))
                if timeout is not None:
                    r.expire(key, timeout)
            return result
        return wrapper
    return decorator

def cache_it_async(timeout=3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if r is not None:
                key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                result = r.get(key)
                if result is not None:
                    return pickle.loads(result)
            result = await func(*args, **kwargs)
            if r is not None:
                r.set(key, pickle.dumps(result))
                if timeout is not None:
                    r.expire(key, timeout)
            return result
        return wrapper
    return decorator