import uuid

from decouple import config
from typing import List, Optional
from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine

SQLITE_FILE_NAME = "database.db"
sqlite_url = f"sqlite:///{SQLITE_FILE_NAME}"
engine = create_engine(sqlite_url, echo=True)


class BaseModel(SQLModel):
    created_at: datetime = Field(default=datetime.today(), nullable=False)
    last_edited: datetime = Field(
        default_factory=lambda: datetime.today(), nullable=False
    )


class Student(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50)
    chat_id: int = Field(max_length=100)
    last_name: str = Field(max_length=50)
    first_name: str = Field(max_length=50)
    login_time: Optional[datetime] = Field(nullable=True)
    logout_time: Optional[datetime] = Field(nullable=True)
    tweets: List["Tweet"] = Relationship(back_populates="student")

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


class Tweet(BaseModel, table=True):
    id_random: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    chat_id: int = Field(max_length=100)
    first_name: str = Field(max_length=200)
    last_name: str = Field(max_length=200)
    content: str = Field(max_length=200)
    student_id: Optional[int] = Field(default=None, foreign_key="student.id")
    student: Optional[Student] = Relationship(back_populates="tweets")
    admin_id: Optional[int] = Field(default=None, foreign_key="admin.id")
    admin: Optional["Admin"] = Relationship(back_populates="tweets")

    @classmethod
    def create_tweet(
        cls,
        chat_id: int,
        first_name: str,
        last_name: str,
        content: str,
        student_id: Optional[int] = None,
        admin_id: Optional[int] = None,
    ) -> "Tweet":
        with Session(engine) as session:
            tweet = cls(
                chat_id=chat_id,
                first_name=first_name,
                last_name=last_name,
                content=content,
                student_id=student_id,
                admin_id=admin_id,
            )
            session.add(tweet)
            session.commit()
            return tweet

    @classmethod
    def get(cls, id_random: str) -> Optional["Tweet"]:
        with Session(engine) as session:
            tweet = session.query(cls).filter_by(id_random=id_random).first()
            return tweet


class Admin(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_chat_id: int = config("TELEGRAM_CHAT_ID_ADMIN", cast=int)
    username: str = "Y_Shabanei"
    email: str = config("EMAIL_ADMIN")
    role: str = "admin"
    expiration: int = datetime(year=2024, month=5, day=26)
    phone_number: int = config("PHONE_ADMIN", cast=int)
    tweets: List["Tweet"] = Relationship(back_populates="admin")
    approved_request: List["ApprovedRequest"] = Relationship(back_populates="admin")

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


class ApprovedRequest(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: int = Field(max_length=10)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    content: str = Field(max_length=5000)
    admin_id: Optional[int] = Field(default=None, foreign_key="admin.id")
    admin: Optional[Admin] = Relationship(back_populates="approved_request")

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
