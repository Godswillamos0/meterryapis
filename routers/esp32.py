from typing import Annotated, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from models import SmartMeter, Users, Billings
from datetime import datetime


router = APIRouter(
    tags=['esp32'],
    prefix='/esp'
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DataRequest(BaseModel):
    voltage: float = Field(default=None)
    current:float = Field(default=None)
    power:float = Field(default=None)
    energy: float = Field(default=None)
    time_stamp: datetime

    class Config:
        from_attributes = True


 
latest_data: Optional[SmartMeter]=None
db_dependency = Annotated[Session, Depends(get_db)]



async def get_latest_data():
    global latest_data
    if latest_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return DataRequest.from_orm(latest_data)

@router.post('/send_data', status_code=status.HTTP_201_CREATED)
async def send_data(db: db_dependency, data: DataRequest):
    global latest_data
    user = db.query(Users).filter(Users.id==1).first()
    now = datetime.now()
    fixed_price = 206.80
    data.time_stamp = str(now)
    latest_data = data.dict()
    user.energy_consumption += data.energy
    consumption = user.energy_consumption/1000
    bill_taken = consumption/fixed_price
    user.bill -= bill_taken
    db.add(SmartMeter(**data.dict()))
    db.commit()
    #db.refresh(SmartMeter(**data.dict()))
    return data


@router.get('/')
async def dummy():
    return "Dummy"


