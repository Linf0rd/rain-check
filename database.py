import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    connect_args={
        "sslmode": "require"
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SearchHistory(Base):
    """Store user search history"""
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class WeatherCache(Base):
    """Cache weather data to reduce API calls"""
    __tablename__ = "weather_cache"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    current_data = Column(JSON)
    hourly_data = Column(JSON)
    daily_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create all tables
Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session with error handling"""
    db = None
    try:
        db = SessionLocal()
        return db
    except Exception as e:
        if db:
            db.close()
        print(f"Database connection error: {str(e)}")
        return None
