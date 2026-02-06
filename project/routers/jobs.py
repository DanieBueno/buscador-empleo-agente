from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import SessionLocal
from ..models.job import Job as JobModel
from ..schemas.job import Job, JobCreate

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[Job])
def get_jobs(db: Session = Depends(get_db)):
    return db.query(JobModel).all()

@router.post("/", response_model=Job)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = JobModel(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/{job_id}", response_model=Job)
def get_job(job_id: int, db: Session = Depends(get_db)):
    return db.query(JobModel).filter(JobModel.id == job_id).first()
from ..agents.scraper_agent import JobScraperAgent

@router.post("/scrape")
def scrape_jobs():
    agent = JobScraperAgent()
    count = agent.run()
    return {"message": f"Scraping complete. {count} jobs processed."}