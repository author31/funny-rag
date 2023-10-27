from fastapi import FastAPI
from config.settings import HN_URL
from app.engine.startup import lifespan

app = FastAPI(lifespan=lifespan)

@app.get("/")
def get_base():
    return {"succcess": True}