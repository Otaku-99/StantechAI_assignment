from fastapi import FastAPI
from .database import engine, Base
from .routers import items
from .logger import logger
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI application started")
    yield
    logger.info("FastAPI application stopped")

app = FastAPI(title="FastAPI CRUD Assignment", lifespan=lifespan)

# Create tables (for demo / assignment)
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(items.router)

# Root route
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/health")
def health():
    return {"status": "ok"}
