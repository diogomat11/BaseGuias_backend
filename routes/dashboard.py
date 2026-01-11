from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Job, Carteirinha, BaseGuia
from sqlalchemy import func

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_carteirinhas = db.query(Carteirinha).count()
    total_guias = db.query(BaseGuia).count()
    total_jobs = db.query(Job).count()
    
    # Job Status Counts
    jobs_success = db.query(Job).filter(Job.status == 'success').count()
    jobs_error = db.query(Job).filter(Job.status == 'error').count()
    jobs_pending = db.query(Job).filter(Job.status.in_(['pending', 'processing'])).count()
    
    return {
        "overview": {
            "total_carteirinhas": total_carteirinhas,
            "total_guias": total_guias,
            "total_jobs": total_jobs
        },
        "jobs_status": {
            "success": jobs_success,
            "error": jobs_error,
            "pending": jobs_pending
        }
    }
