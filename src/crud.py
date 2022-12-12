from sqlalchemy.orm import Session

from src import models, schemas


def create_workshop(db: Session, workshop: schemas.WorkshopCreate):
    db_workshop = models.Workshop(
        name=workshop.name,
        full_name=workshop.full_name)
    db.add(db_workshop)
    db.commit()
    db.refresh(db_workshop)
    return db_workshop
def create_workshop_worker(db: Session, worker: schemas.WorkerCreate, workshop_id: int):
    db_worker = models.Worker(
        **worker.dict(), 
        job_id=workshop_id)
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

def create_overall(db: Session, overall: schemas.OverallCreate):
    db_overall = models.Overall(
        kind=overall.kind,
        wear_time=overall.wear_time,
        cost=overall.cost)
    db.add(db_overall)
    db.commit()
    db.refresh(db_overall)
    return db_overall
def create_overall_reciving(db:Session, reciving: schemas.RecivingCreate, overall_id: int):
    db_reciving = models.Reciving(
        **reciving.dict(),
        overall_id=overall_id)
    db.add(db_reciving)
    db.commit()
    db.refresh(db_reciving)
    return db_reciving

def get_workshops(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Workshop).offset(skip).limit(limit).all()
def get_workshop(db: Session, workshop_id: id):
    return db.query(models.Workshop).filter(models.Workshop.id == workshop_id).first()
def get_workshop_by_name(db:Session, name: str):
    return db.query(models.Workshop).filter(models.Workshop.name == name).first()
def get_workshop_by_full_name(db:Session, full_name: str):
    return db.query(models.Workshop).filter(models.Workshop.full_name == full_name).first()

def get_overalls(db:Session, skip: int=0, limit: int=100):
    return db.query(models.Overall).offset(skip).limit(limit).all()
def get_overall(db: Session, overall_id: id):
    return db.query(models.Overall).filter(models.Overall.id == overall_id).first()
def get_overalll_by_kind(db:Session, kind: str):
    return db.query(models.Overall).filter(models.Overall.kind == kind).first()

def get_workers(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Worker).offset(skip).limit(limit).all()
def get_worker(db: Session, worker_id: int):
    return db.query(models.Worker).filter(models.Worker.id == worker_id).first()
def get_worker_by_full_name(db:Session, full_name: str):
    return db.query(models.Worker).filter(models.Worker.full_name == full_name).first()

def get_recivings(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Reciving).offset(skip).limit(limit).all()
def get_reciving(db: Session, reciving_id: str):
    return db.query(models.Reciving).filter(models.Reciving.id == reciving_id).first()
def get_reciving_by_signature(db: Session, signature: str):
    return db.query(models.Reciving).filter(models.Reciving.signature == signature).first()

