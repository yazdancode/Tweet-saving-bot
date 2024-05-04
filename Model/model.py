from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel, create_engine

SQLITE_FILE_NAME = "database.db"

sqlite_url = f"sqlite:///{SQLITE_FILE_NAME}"
engine = create_engine(sqlite_url, echo=True)


class BaseModel(SQLModel):
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    last_edited: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


class Student(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    chat_id: int
    last_name: str
    first_name: str
    tweets: List["Tweet"] = Relationship(back_populates="student")


class Tweet(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: int
    content: str
    student_id: Optional[int] = Field(default=None, foreign_key="student.id")
    student: Optional[Student] = Relationship(back_populates="tweets")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
