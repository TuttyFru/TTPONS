from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class BaseModel(Base):
    """
    Абстартный базовый класс, где описаны все поля и методы по умолчанию
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)

    def __repr__(self):
        return f"<{type(self).__name__}(id={self.id})>"


class Overall(BaseModel):
    __tablename__ = "overalls"

    kind = Column(String, index=True)
    wear_time = Column(Integer)
    cost = Column(Integer)

    recivings = relationship("Reciving", back_populates="overall")


class Workshop(BaseModel):
    __tablename__ = "workshops"

    name = Column(String, index=True)
    full_name = Column(String, index=True)

    workers = relationship("Worker", back_populates="job")


class Worker(BaseModel):
    __tablename__ = "workers"

    full_name = Column(String, index=True)
    job_title = Column(String)
    discount = Column(Integer) # Скидка на спецодежду

    job_id = Column(Integer, ForeignKey("workshops.id"))

    job = relationship("Workshop", back_populates="workers")
    recivings = relationship("Reciving", back_populates="worker")


class Reciving(BaseModel):
    __tablename__ = "recivings"

    date = Column(String)
    signature = Column(String, index=True)

    worker_id = Column(Integer, ForeignKey("workers.id"))
    overall_id = Column(Integer, ForeignKey("overalls.id"))

    worker = relationship("Worker", back_populates="recivings")
    overall = relationship("Overall", back_populates="recivings")



