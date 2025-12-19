from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Phase(BaseModel):
    """Schema for a learning phase in the visual timeline."""
    id: int
    title: str
    description: str
    duration: str
    milestones: List[str]


class VisualData(BaseModel):
    """Schema for the visual timeline data."""
    phases: List[Phase]
    total_duration: str


class RoadmapCreate(BaseModel):
    """Schema for creating a new roadmap."""
    query: str = Field(..., min_length=3, max_length=500, description="The learning goal query")


class RoadmapResponse(BaseModel):
    """Schema for roadmap response."""
    id: int
    user_query: str
    title: str
    content: str
    visual_data: Optional[VisualData] = None
    created_at: datetime

    class Config:
        from_attributes = True


class RoadmapListItem(BaseModel):
    """Schema for roadmap list item (summary)."""
    id: int
    user_query: str
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class RoadmapList(BaseModel):
    """Schema for list of roadmaps."""
    roadmaps: List[RoadmapListItem]
    total: int

