from sqlalchemy import Column, Integer, String
from db import Base

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)

    def __repr__(self):
        return f"Habit(id={self.id}, name='{self.name}')"