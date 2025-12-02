"""Define an SQLAlchemy model for a habit."""

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    start_time: Mapped[datetime]
    frequency: Mapped[int]
    last_done: Mapped[datetime] = mapped_column(nullable=True)

    def __repr__(self):
        return f"Habit(\
            id={self.id}, name={self.name}, description={self.description},\
            frequency{self.frequency}, start_time={self.start_time},\
            frequency={self.frequency}, last_done={self.last_done}\
        )"
