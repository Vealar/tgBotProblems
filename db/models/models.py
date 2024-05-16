
from sqlalchemy import Table,Column,Integer,String,MetaData,ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

metadata = MetaData()
Base = declarative_base()
class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer)
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    def __init__(self, user_id, name):
        self.username = name
        self.id = user_id

    # M2M
    problems_solved = relationship(
        "Problem",
        secondary="problem2user",
        back_populates="users_solving"
    )

class Topic(Base):
    __tablename__ = "topics"
    name = Column(String,primary_key=True)
    def __init__(self, name):
        self.name = name

    # M2M
    problems_relevant = relationship(
        "Problem",
        secondary="problem2topic",
        back_populates="topics"
    )

class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    level = Column(String)
    text = Column(String)
    solution = Column(String)
    #M2M
    topics = relationship(
        "Topic",
        secondary="problem2topic",
        back_populates="problems_relevant"
    )
    # M2M
    users_solving = relationship(
        "User",
        secondary="problem2user",
        back_populates="problems_solved"
    )

class Problem2Topic(Base):
    #M2M
    __tablename__ = 'problem2topic'
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), primary_key=True)
    topic_id = Column(String, ForeignKey("topics.name", ondelete="CASCADE"), primary_key=True)
class Problem2User(Base):
    #M2M
    __tablename__ = 'problem2user'
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)