import os
import datetime
from sqlalchemy import create_engine, Integer, String, DateTime, func, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped, relationship

POSTGRES_USER = os.getenv('POSTGRES_USER', "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")
POSTGRES_DB = os.getenv("POSTGRES_DB", "netology_flask")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5433")

engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
                       f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "app_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "registration_time": self.registration_time.isoformat()
        }


class Post(Base):
    __tablename__ = "app_post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    heading: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    registration_time_post: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id = mapped_column(Integer, ForeignKey("app_users.id", ondelete="CASCADE"))
    user = relationship("User", lazy="joined")

    def json(self):
        return {
            "id": self.id,
            "heading": self.heading,
            "description": self.description,
            "registration_time_post": self.registration_time_post.isoformat(),
            "user_id": self.user_id
        }


Base.metadata.create_all(bind=engine)
