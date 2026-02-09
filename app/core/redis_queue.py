import redis
from rq import Queue
from app.core.config import settings


def get_redis_connection():
    """Redis 연결 생성."""
    return redis.from_url(settings.REDIS_URL)


# Redis 연결
redis_conn = get_redis_connection()

# RQ Queue 생성 (기본 큐)
default_queue = Queue(connection=redis_conn)

# 우선순위별 큐 (선택사항)
high_priority_queue = Queue("high", connection=redis_conn)
low_priority_queue = Queue("low", connection=redis_conn)

