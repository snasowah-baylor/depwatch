from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine
from app.logging import configure_logging
from app.models.base import Base

configure_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if str(engine.url).startswith("sqlite"):
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="depwatch", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}
