"""Sets up the redis connection and the redis queue."""
import os

import redis
from rq import Queue

from sys_config import REDIS_HOST, REDIS_PORT

redis_conn = redis.Redis(
    host=os.getenv("REDIS_HOST", REDIS_HOST),
    port=os.getenv("REDIS_PORT", REDIS_PORT),
    password=os.getenv("REDIS_PASSWORD", "gimindpass"),
)

redis_queue_offiaccount = Queue(name='offiaccount',connection=redis_conn)
redis_queue_wechat = Queue(name='wechat',connection=redis_conn)
redis_queue_web = Queue(name='web',connection=redis_conn)

redis_queue_offiaccount_result = Queue(name='offiaccount_result',connection=redis_conn)
redis_queue_wechat_result = Queue(name='wechat_result',connection=redis_conn)
redis_queue_web_result = Queue(name='web_result',connection=redis_conn)
