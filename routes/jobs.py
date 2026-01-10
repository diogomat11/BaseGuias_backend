from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Job, Carteirinha
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

class CreateJobRequest(BaseModel):
    type: str # 'single', 'multiple', 'all'
    carteirinha_ids: Optional[List[int]] = None

@router.post("/")
def create_jobs(request: CreateJobRequest, db: Session = Depends(get_db)):
    created_count = 0
    
    if request.type == 'all':
        # Create jobs for all carteirinhas that don't have a PENDING or PROCESSING job?
        # User requirement: "se for sim, apagar todas carteirinhas da tabela e salvar novas, se fo não não apenas armazenar novas" -> For Upload
        # For Jobs: "1 carteirinha específica, várias, todas"
        # Often we want to re-process even if exists, or maybe check duplicates. 
        # Strategy: Create new job regardless of history, but maybe ensure no *active* job exists?
        # Let's just create new jobs for now as per simple request.
        
        all_carteirinhas = db.query(Carteirinha).all()
        for cart in all_carteirinhas:
            job = Job(carteirinha_id=cart.id, status="pending")
            db.add(job)
            created_count += 1
            
    elif request.type in ['single', 'multiple']:
        if not request.carteirinha_ids:
             raise HTTPException(status_code=400, detail="carteirinha_ids required for single/multiple")
        
        for cart_id in request.carteirinha_ids:
            # Validate existence
            cart = db.query(Carteirinha).filter(Carteirinha.id == cart_id).first()
            if cart:
                job = Job(carteirinha_id=cart.id, status="pending")
                db.add(job)
                created_count += 1
                
    else:
        raise HTTPException(status_code=400, detail="Invalid job type")

    db.commit()
    return {"message": f"Created {created_count} jobs", "count": created_count}

@router.get("/")
def list_jobs(status: Optional[str] = None, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(Job)
    if status:
        query = query.filter(Job.status == status)
    
    # Order by priority desc, created_at asc
    jobs = query.order_by(Job.priority.desc(), Job.created_at.asc()).limit(limit).all()
    return jobs
