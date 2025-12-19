from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import engine, get_db, Base
from .models import Roadmap
from .schemas import RoadmapCreate, RoadmapResponse, RoadmapList, RoadmapListItem
from .services.claude_service import get_claude_service

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini Mentor Agent API",
    description="AI-powered learning roadmap generator",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Mini Mentor Agent API"}


@app.post("/api/roadmaps", response_model=RoadmapResponse, status_code=201)
def create_roadmap(request: RoadmapCreate, db: Session = Depends(get_db)):
    """
    Create a new learning roadmap based on the user's query.
    
    This endpoint sends the query to Claude AI to generate a comprehensive
    learning roadmap with phases, milestones, and resources.
    """
    try:
        claude = get_claude_service()
        roadmap_data = claude.generate_roadmap(request.query)
        
        # Create database record
        db_roadmap = Roadmap(
            user_query=request.query,
            title=roadmap_data.get("title", f"Learning Roadmap: {request.query[:50]}"),
            content=roadmap_data.get("content", ""),
            visual_data=roadmap_data.get("visual_data")
        )
        
        db.add(db_roadmap)
        db.commit()
        db.refresh(db_roadmap)
        
        return db_roadmap
        
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to generate roadmap: {str(e)}")


@app.get("/api/roadmaps", response_model=RoadmapList)
def list_roadmaps(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    List all saved roadmaps.
    
    Returns a paginated list of roadmap summaries (without full content).
    """
    total = db.query(Roadmap).count()
    roadmaps = db.query(Roadmap).order_by(Roadmap.created_at.desc()).offset(skip).limit(limit).all()
    
    return RoadmapList(
        roadmaps=[RoadmapListItem.model_validate(r) for r in roadmaps],
        total=total
    )


@app.get("/api/roadmaps/{roadmap_id}", response_model=RoadmapResponse)
def get_roadmap(roadmap_id: int, db: Session = Depends(get_db)):
    """
    Get a specific roadmap by ID.
    
    Returns the full roadmap including content and visual data.
    """
    roadmap = db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()
    
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    return roadmap


@app.delete("/api/roadmaps/{roadmap_id}", status_code=204)
def delete_roadmap(roadmap_id: int, db: Session = Depends(get_db)):
    """
    Delete a roadmap by ID.
    """
    roadmap = db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()
    
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    db.delete(roadmap)
    db.commit()
    
    return None

