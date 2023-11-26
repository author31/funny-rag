from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.engine.startup import lifespan
from app.routers.routes import router
from app.middleware import cache_middleware
from config.settings import HN_URL

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router, prefix="/app")