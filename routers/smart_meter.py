from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from models import SmartMeter, Users
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
    if now-ld.time_stamp > timedelta(seconds=10):
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT)
    print(ld.time_stamp -now)
    return ld

@router.get('/expired', status_code=status.HTTP_200_OK)
async def check_if_unit_expired(db: db_dependency):
    user_model=db.query(Users).filter(Users.id==1).first()
    if user_model.bill <= 0.0:
        return True
    else:
        return False
