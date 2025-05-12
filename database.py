from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./data.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, 
                      connect_args={'check_same_thread':False},
                      pool_size=10,        # Default is 5; Increase based on your needs
                      max_overflow=20,     # Default is 10; Controls how many extra connections can be created
                      pool_timeout=30,     # Default is 30 seconds
                      pool_recycle=1800    # Recycle connections every 30 minutes to avoid stale connection)
                      )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
