from fastapi import FastAPI
from config.settings import HN_URL
from app.engine.startup import lifespan
from app.routers.routes import router

app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/app")