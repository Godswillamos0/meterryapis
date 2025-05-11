from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from models import SmartMeter, Users, Billings
from datetime import datetime


class Bill(BaseModel):
    amount:float =Field(default=300)


class CreateUserRequest(BaseModel):
    name:str=Field(min_length=3, max_length=20)
    bill:float
    energy_consumption:float

    class Config:
        from_attributes = True


router = APIRouter(
    tags=['users'],
    prefix='/user'
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
db_dependency = Annotated[Session, Depends(get_db)]


@router.post('/create-user', status_code=status.HTTP_204_NO_CONTENT)
async def create_user(db: db_dependency, user: CreateUserRequest):
    create_user_model = Users(**user.dict())
    db.add(create_user_model)
    db.commit()

@router.post('/bill/buy', status_code=status.HTTP_204_NO_CONTENT)
async def buy_unit(db: db_dependency, bill: Bill):
    
    user_data=db.query(Users).filter(Users.id==1).first()
    #1 unit(KWh) is == #206.80
    fixed_price = 206.80
    unit_buy = bill.amount/fixed_price
    user_data.bill += unit_buy
    db.add(user_data)
    db.add(Billings(amount=bill.amount, 
                    time_stamp=datetime.now(), 
                    unit_gotten=unit_buy))
    db.commit()
    
@router.get('/bill/history', status_code=status.HTTP_200_OK)
async def get_bill_history(db: db_dependency):
    return db.query(Billings).all()

@router.get('bill/history/remaining-bill', status_code=200)
async def get_user_remaining_bill(db: db_dependency):
    user_model = db.query(Users).filter(Users.id ==1).first()
    return user_model.bill
    
