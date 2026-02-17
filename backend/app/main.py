from fastapi import FastAPI, Depends
from app.db.deps import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok, api is running"}


@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    state = db.execute(text("Select 1"))
    return {"database": state.scalar()}
