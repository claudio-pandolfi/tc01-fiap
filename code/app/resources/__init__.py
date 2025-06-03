
from redis import Redis
from rq import Queue
from app.config import Config

redis_conn = Redis.from_url(url=Config().__dict__['REDIS_URL'])
queue = Queue('scraping', connection=redis_conn)
