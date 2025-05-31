
from redis import Redis
from rq import Queue
from app.config import Config

redis_conn = Redis(host=Config().__dict__['REDIS_URL'], port=6379, db=0)
queue = Queue('scraping', connection=redis_conn)
