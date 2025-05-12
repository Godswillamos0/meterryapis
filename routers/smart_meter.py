from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from models import SmartMeter
from .esp32 import get_latest_data, DataRequest
from datetime import datetime, timedelta


router = APIRouter(
    tags=['smart_meter'],
    prefix='/meter'
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
live_data_dependency =  Annotated[dict, Depends(get_latest_data)]

@router.get('/history', status_code=status.HTTP_200_OK)
async def get_data_history(db: db_dependency):
    return db.query(SmartMeter).all()

@router.get('/live', response_model=DataRequest, status_code=status.HTTP_200_OK)
async def get_live_data(ld:live_data_dependency):
    print(ld)
    print(type(ld))
    now = datetime.now()
    if now-datetime.strptime(ld.time_stamp) > timedelta(seconds=5):
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT)
    print(ld.time_stamp -now)
    return ld
