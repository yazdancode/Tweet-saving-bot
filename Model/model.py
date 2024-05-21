import os
from decouple import config
from typing import List, Optional
from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine
from data_base.dbcore import Base

database_directory = os.path.join("settings", "20.24")
os.makedirs(database_directory, exist_ok=True)
SQLITE_FILE_NAME = "database.db"
sqlite_path = os.path.join(database_directory, SQLITE_FILE_NAME)
sqlite_url = f"sqlite:///{sqlite_path}"
engine = create_engine(sqlite_url, echo=True)


class BaseModel(SQLModel, Base):
    __tablename__ = "model-basemodel"
    id: Optional[int] = Field(default=None, primary_key=True)

    def __repr__(self):
        return self.id, self.username, self.chat_id, self.last_name, self.first_name


class Student(BaseModel, Base, table=True):
    __tablename__ = "student"
    username: str = Field(max_length=50)
    chat_id: int = Field(max_length=100)
    last_name: str = Field(max_length=50)
    first_name: str = Field(max_length=50)
    login_time: Optional[datetime] = Field(nullable=True)
    logout_time: Optional[datetime] = Field(nullable=True)
    tweets: List["Tweet"] = Relationship(back_populates="student")

    def __repr__(self):
        return self.username, self.chat_id, self.last_name, self.first_name

    @classmethod
    def create_student(
        cls, username: str, chat_id: int, last_name: str, first_name: str
    ) -> "Student":
        with Session(engine) as session:
            existing_student = session.query(cls).filter_by(chat_id=chat_id).first()
            if existing_student:
                return existing_student
            student = cls(
                username=username,
                chat_id=chat_id,
                last_name=last_name,
                first_name=first_name,
            )
            session.add(student)
            session.commit()
            return student

    @classmethod
    def get(cls, chat_id: int) -> Optional["Student"]:
        with Session(engine) as session:
            student = session.query(cls).filter_by(chat_id=chat_id).first()
            return student

    def logout_user(self) -> None:
        with Session(engine) as session:
            self.logout_time = datetime.now(timezone.utc)
            session.add(self)
            session.commit()


class Tweet(BaseModel, Base, table=True):
    __tablename__ = "tweet"
    chat_id: int = Field(max_length=100)
    username: Optional[str] = Field(max_length=50, nullable=True)
    first_name: str = Field(max_length=200)
    last_name: str = Field(max_length=200)
    content: str = Field(max_length=200)
    postage_date: str = Field(max_length=100)
    student_id: Optional[int] = Field(default=None, foreign_key="student.id")
    student: Optional[Student] = Relationship(back_populates="tweets")
    admin_id: Optional[int] = Field(default=None, foreign_key="admin.id")
    admin: Optional["Admin"] = Relationship(back_populates="tweets")

    def __repr__(self):
        return (
            self.id,
            self.chat_id,
            self.username,
            self.first_name,
            self.last_name,
            self.content,
        )

    @classmethod
    def create_tweet(
        cls,
        chat_id: int,
        username: Optional[str],
        first_name: str,
        last_name: str,
        content: str,
        postage_date: str,
        student_id: Optional[int] = None,
        admin_id: Optional[int] = None,
    ) -> "Tweet":
        with Session(engine) as session:
            tweet = cls(
                chat_id=chat_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                content=content,
                postage_date=postage_date,
                student_id=student_id,
                admin_id=admin_id,
            )
            session.add(tweet)
            session.commit()
            return tweet


class Admin(BaseModel, Base, table=True):
    __tablename__ = "admin"
    telegram_chat_id: int = config("TELEGRAM_CHAT_ID_ADMIN", cast=int)
    username: str = "Y_Shabanei"
    email: str = config("EMAIL_ADMIN")
    role: str = "admin"
    expiration: int = datetime(year=2024, month=5, day=26)
    phone_number: int = config("PHONE_ADMIN", cast=int)
    tweets: List["Tweet"] = Relationship(back_populates="admin")
    approved_request: List["ApprovedRequest"] = Relationship(back_populates="admin")

    def __repr__(self):
        return (
            self.telegram_chat_id,
            self.username,
            self.email,
            self.role,
            self.expiration,
            self.phone_number,
        )

    @classmethod
    def create_admin(cls) -> None:
        with Session(engine) as session:
            admin = cls()
            session.add(admin)
            session.commit()

    @classmethod
    def create_admin_once(cls) -> Optional["Admin"]:
        with Session(engine) as session:
            admin = session.query(cls).get(1)
            if not admin:
                cls.create_admin()
                admin = session.query(cls).get(1)
            return admin

    @classmethod
    def update_admin_monthly(cls):
        today = datetime.now().date()
        if today.day == 30:
            cls.remove_admin()

    @classmethod
    def get(cls, username: str):
        with Session(engine) as session:
            admin = session.query(cls).filter_by(username=username).first()
            return admin

    @staticmethod
    def remove_admin() -> None:
        with Session(engine) as session:
            admin = session.query(Admin).order_by(Admin.id.desc()).first()
            if admin:
                session.delete(admin)
                session.commit()


class ApprovedRequest(BaseModel, Base, table=True):
    __tablename__ = "approvedrequest"
    chat_id: int = Field(max_length=10)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    content: str = Field(max_length=5000)
    admin_id: Optional[int] = Field(default=None, foreign_key="admin.id")
    admin: Optional[Admin] = Relationship(back_populates="approved_request")

    def __repr__(self):
        return self.chat_id, self.first_name, self.last_name, self.content

    @classmethod
    def create_approvedrequest(
        cls,
        chat_id: int,
        first_name: str,
        last_name: str,
        content: str,
    ) -> "ApprovedRequest":
        with Session(engine) as session:
            request = cls(
                chat_id=chat_id,
                first_name=first_name,
                last_name=last_name,
                content=content,
            )
            session.add(request)
            session.commit()
            return request


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
