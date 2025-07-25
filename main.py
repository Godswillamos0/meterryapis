from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from routers import smart_meter, esp32, users
from database import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # or ["*"] to allow all (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(smart_meter.router)
app.include_router(esp32.router)
app.include_router(users.router)


@app.get("/ping")
async def ping_server():
    return "server active"
