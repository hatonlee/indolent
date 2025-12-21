"""Define models for habits and their completions."""

from datetime import datetime, timedelta

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Habit(Base):
    """SQLAlchemy ORM model for a habit."""

    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    start_time: Mapped[datetime]
    frequency: Mapped[timedelta]
    completions: Mapped[list["Completion"]] = relationship(
        back_populates="habit", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Habit(id={self.id}, name={self.name!r}, start_time={self.start_time!r}), frequency={self.frequency}, done={self.completed()}>"

    def completed(self, interval: int | datetime = datetime.now()) -> bool:
        """Return whether the habit has been completed within a specific `interval`.

        Args:
            interval: Index starting from 0 for the first interval since `start_time`,
                      or a `datetime` object to specify a particular time.

        Returns:
            Whether the habit has been completed within the specified interval.
        """
        if not self.completions:
            return False

        if isinstance(interval, datetime):
            interval = (interval - self.start_time) // self.frequency

        interval_start = self.start_time + interval * self.frequency
        interval_end = interval_start + self.frequency
        return any(interval_start <= c.time < interval_end for c in self.completions)


class Completion(Base):
    """SQLAlchemy ORM model for a habit completion entry."""

    __tablename__ = "completions"

    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[datetime]
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"))
    habit: Mapped["Habit"] = relationship(back_populates="completions")

    def __repr__(self):
        return (
            f"<Completion(id={self.id}, time={self.time!r}, habit_id={self.habit.id})>"
        )
