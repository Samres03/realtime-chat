from fastapi import APIRouter, Depends
from app.db.deps import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok, api is running"}


@router.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    state = db.execute(text("Select 1"))
    return {"database": state.scalar()}
