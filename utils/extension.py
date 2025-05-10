#contains common parts for blueprints like redis conncetion 
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis

redis_client = redis.Redis(host='redis', port=6379, db=0)

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://redis:6379"
)
