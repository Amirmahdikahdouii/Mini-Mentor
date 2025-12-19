from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base


class Roadmap(Base):
    """SQLAlchemy model for storing learning roadmaps."""
    
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_query = Column(String(500), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    visual_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

