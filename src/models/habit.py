"""Define an SQLAlchemy model for a habit."""

from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Habit(Base):
    """Define an SQLAlchemy model for a habit."""

    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]

    def __repr__(self):
        return f"Habit(id={self.id!r}, name={self.name!r}, description={self.description!r})"
