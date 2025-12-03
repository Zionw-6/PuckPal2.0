from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String, default="user")

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    drill_id = Column(String)
    drill_title = Column(String)
    reps = Column(Integer)
    seconds = Column(Float)
    rate = Column(Float)
    date = Column(String)

    user = relationship("User")

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    day_number = Column(Integer)
    drill_id = Column(String)
    reps = Column(Integer)
    minutes = Column(Integer)

    user = relationship("User")
