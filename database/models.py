from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Flag(Base):
    __tablename__ = "flags"
    id = Column(Integer, primary_key=True)
    team = Column(String(128), index=True)
    flag = Column(String(256))

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True)
    team = Column(String(128), unique=True)
    score = Column(Integer, default=0)
