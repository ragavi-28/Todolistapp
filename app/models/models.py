from sqlalchemy import Column, Integer, String, Boolean

from app.database.database import Base


class UserDB(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )


class Todo(Base):

    __tablename__ = "todos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        String(500)
    )

    completed = Column(
        Boolean,
        default=False
    )

    user_id = Column(
        Integer,
        nullable=False
    )