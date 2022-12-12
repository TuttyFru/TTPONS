from pydantic import BaseModel

class RecivingBase(BaseModel):
    date: str
    signature: str
class RecivingCreate(RecivingBase):
    pass
class Reciving(RecivingBase):
    id: int
    worker_id: int
    overall_id: int
    class Config:
        orm_mode = True

class OverallBase(BaseModel):
    kind: str
    wear_time: int
    cost: int
    
class OverallCreate(OverallBase):
    pass
class Overall(OverallBase):
    id: int
    recivings: list[Reciving] = []
    class Config:
        orm_mode = True

class WorkerBase(BaseModel):
    full_name: str
    job_title: str
    discount:int
class WorkerCreate(WorkerBase):
    pass
class Worker(WorkerBase):
    id: int
    job_id: int
    recivings: list[Reciving] = []
    class Config:
        orm_mode = True
        
class WorkshopBase(BaseModel):
    name: str
    full_name: str
class WorkshopCreate(WorkshopBase):
    pass
class Workshop(WorkshopBase):
    id: int
    workers: list[Worker] = []
    class Config:
        orm_mode = True

