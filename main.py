from fastapi import FastAPI
import models
from routers import smart_meter, esp32, users
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(smart_meter.router)
app.include_router(esp32.router)
app.include_router(users.router)