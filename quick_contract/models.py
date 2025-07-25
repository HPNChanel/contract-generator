from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    contract_type = Column(String, nullable=False)
    data = Column(Text, nullable=True)  # JSON data stored as text
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 