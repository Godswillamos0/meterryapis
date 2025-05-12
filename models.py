from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime

class SmartMeter(Base):
    __tablename__ = 'smart_meter'
    
    id=Column(Integer, primary_key=True, index=True)
    time_stamp=Column(DateTime, nullable=True)
    voltage=Column(Float)
    current=Column(Float)
    power=Column(Float)
    energy=Column(Float)

    
    
class Users(Base):
    __tablename__ ='users'

    id=Column(Integer, primary_key=True, index=True)
    name= Column(String)
    bill=Column(Float)
    energy_consumption= Column(Float)
    
class Billings(Base):
    __tablename__ ='bills'
    
    id=Column(Integer, primary_key=True, index=True)
    amount=Column(Float)
    time_stamp=Column(DateTime)
    unit_gotten=Column(Float)