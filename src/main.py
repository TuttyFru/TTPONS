from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    """
    Задаем зависимость к БД. При каждом запросе будет создаваться новое
    подключение.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/workshop/", response_model=schemas.Workshop)
def create_workshop(workshop: schemas.WorkshopCreate, db: Session = Depends(get_db)):
    return crud.create_workshop(db=db, workshop=workshop)
@app.post("/workshop/{workshop_id}/workers/", response_model=schemas.Worker)
def create_woreker_for_workshop(workshop_id: int, worker:schemas.WorkerCreate, db: Session=Depends(get_db)):
    return crud.create_workshop_worker(db=db, worker=worker, workshop_id=workshop_id)
@app.get("/workshop/", response_model=list[schemas.Workshop])
def read_workshops(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    workshops = crud.get_workshops(db, skip=skip, limit=limit)
    return workshops
@app.get("/workshop/{workshop_id}", response_model=schemas.Workshop)
def read_workshop(workshop_id: int, db: Session=Depends(get_db)):
    db_workshop = crud.get_workshop(db, workshop_id=workshop_id)
    if db_workshop is None:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return db_workshop


@app.post("/overall/", response_model=schemas.Overall)
def create_overall(overall: schemas.OverallCreate, db: Session = Depends(get_db)):
    return crud.create_overall(db=db, overall=overall)
@app.get("/overall/", response_model=list[schemas.Overall])
def read_overalls(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    overalls = crud.get_overalls(db, skip=skip, limit=limit)
    return overalls
@app.get("/overall/{overall_id}", response_model=schemas.Overall)
def read_overall(overall_id: int, db: Session=Depends(get_db)):
    db_overall = crud.get_overall(db, overall_id=overall_id)
    if overall_id is None:
        raise HTTPException(status_code=404, detail="Overall not found")
    return db_overall

@app.get("/worker/", response_model=list[schemas.Worker])
def read_workers(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    workers = crud.get_workers(db, skip=skip, limit=limit)
    return workers
@app.get("/worker/{worker_id}", response_model=schemas.Worker)
def read_worker(worker_id: int, db: Session=Depends(get_db)):
    db_worker = crud.get_worker(db, worker_id=worker_id)
    if worker_id is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker

@app.get("/reciving/", response_model=list[schemas.Reciving])
def read_recivings(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    recivings = crud.get_recivings(db, skip=skip, limit=limit)
    return recivings
@app.get("/reciving/{reciving_id}", response_model=schemas.Reciving)
def read_reciving(reciving_id: int, db: Session=Depends(get_db)):
    db_reciving = crud.get_reciving(db, reciving_id=reciving_id)
    if reciving_id is None:
        raise HTTPException(status_code=404, detail="Reciving not found")
    return db_reciving
    