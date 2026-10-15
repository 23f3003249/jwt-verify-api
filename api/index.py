
import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from upstash_redis import Redis

app = FastAPI()

rest_url = os.getenv("UPSTASH_REDIS_REST_URL")
rest_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")

redis_client = (
    Redis(url=rest_url, token=rest_token)
    if rest_url and rest_token
    else None
)


@app.get("/healthz")
def healthz():
    if redis_client is None:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "redis": "down"},
        )

    try:
        redis_client.ping()
        return {"status": "ok", "redis": "up"}
    except Exception as exc:
        print(f"Redis health check failed: {type(exc).__name__}: {exc}")
        return JSONResponse(
            status_code=503,
            content={"status": "error", "redis": "down"},
        )


@app.post("/hit/{hit_id}")
def hit(hit_id: str):
    if redis_client is None:
        return JSONResponse(
            status_code=503,
            content={"detail": "Redis is not configured"},
        )

    try:
        count = redis_client.incr(f"hit:{hit_id}")
        return {"id": hit_id, "count": count}
    except Exception as exc:
        print(f"Redis increment failed: {type(exc).__name__}: {exc}")
        return JSONResponse(
            status_code=503,
            content={"detail": "Redis unavailable"},
        )
