import os
from fastapi import FastAPI
from redis.asyncio import Redis
from redis.exceptions import RedisError

app = FastAPI()

redis = Redis.from_url(
    os.environ["REDIS_URL"],
    decode_responses=True,
)

@app.get("/healthz")
async def healthz():
    try:
        await redis.ping()
        return {"status": "ok", "redis": "up"}
    except RedisError:
        return {"status": "error", "redis": "down"}

@app.post("/hit/{id}")
async def hit(id: str):
    count = await redis.incr(f"hit:{id}")
    return {"id": id, "count": count}