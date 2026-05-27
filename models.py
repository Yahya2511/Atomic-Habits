from __future__ import annotations

from datetime import timezone, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None
    )
    
    # --- Relationships ---
    # Habits this user hosts
    hosted_habits: Mapped[list["Habit"]] = relationship(
        "Habit", 
        back_populates="creator"
        )
    
    # Habits this user is participating in (The Party)
    user_habits: Mapped[list["UserHabits"]] = relationship(
        "UserHabits", 
        back_populates="user", 
        cascade="all, delete-orphan"
        )
    
    # Daily logs for this user
    logs: Mapped[list["HabitsLogs"]] = relationship(
        "HabitsLogs", 
        back_populates="user", 
        cascade="all, delete-orphan"
        )
    
    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"
    
class Habit(Base):
    __tablename__ = "habits"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(100), nullable=True)
    schedule_mask: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # --- Relationships ---
    creator: Mapped["User"] = relationship(
        "User", 
        back_populates="hosted_habits"
        )
    members: Mapped[list["UserHabits"]] = relationship(
        "UserHabits", 
        back_populates="habit", 
        cascade="all, delete-orphan"
        )
    logs: Mapped[list["HabitsLogs"]] = relationship(
        "HabitsLogs", 
        back_populates="habit", 
        cascade="all, delete-orphan"
        )
    
class UserHabits(Base):
    __tablename__ = "user_habits"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    habit_id: Mapped[int] = mapped_column(
        ForeignKey("habits.id"),
        nullable=False,
        index=True
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )
    
    # --- Relationships ---
    user: Mapped["User"] = relationship(
        "User", 
        back_populates="user_habits"
        )
    habit: Mapped["Habit"] = relationship(
        "Habit", 
        back_populates="members"
        )
        
class HabitsLogs(Base):
    __tablename__ = "habits_logs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    habit_id: Mapped[int] = mapped_column(
        ForeignKey("habits.id"),
        nullable=False,
        index=True
    )
    logged_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )
    is_completed: Mapped[bool] = mapped_column(
        default=False, 
        nullable=False
        )
    
    user: Mapped["User"] = relationship(
        "User", 
        back_populates="logs"
        )
    habit: Mapped["Habit"] = relationship(
        "Habit", 
        back_populates="logs"
        )