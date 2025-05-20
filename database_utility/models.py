from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import Column, Integer, String,DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

timezone = datetime.now(ZoneInfo("Asia/Kolkata"))

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String,nullable=False)
    company_name = Column(String, nullable=False)
    lead_relevance = Column(String, nullable=False)
    conversation = Column(String) 
    created_at = Column(DateTime, default=timezone)
