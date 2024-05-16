from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from db.models.models import Base, Topic, Admin, Problem
from config.config_db import settings
from config.config_bot import ACCESS_ADMIN


class DataBase:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)

        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

        self.session = sessionmaker(bind=self.engine)


db = DataBase(settings.DATABASE_URL_psycopg)
def fullBase():
    with db.session() as session:

        problem1 = Problem(level = "EASY",text = "text1",solution = "solution1")
        problem2 = Problem(level = "EASY",text = "text2",solution = "solution2")
        problem3 = Problem(level = "MEDIUM",text = "text3",solution = "solution3")
        problem4 = Problem(level = "COFFIN",text = "text4",solution = "solution4")
        problem5 = Problem(level = "EASY",text = "text5",solution = "solution5")
        problem6 = Problem(level = "MEDIUM",text = "text6",solution = "solution6")
        problem7 = Problem(level = "HARD",text = "text7",solution = "solution7")
        problem8 = Problem(level = "EASY",text = "text8",solution = "solution8")

        topic1 = Topic(name='Algebra')
        topic2 = Topic(name='Geometry')
        topic3 = Topic(name='Kombinatorika')
        topic4 = Topic(name='Stereometry')
        topic5 = Topic(name='Functional')

        session.add(problem1)
        session.add(problem2)
        session.add(problem3)
        session.add(problem4)
        session.add(problem5)
        session.add(problem6)
        session.add(problem7)
        session.add(problem8)

        session.add(topic1)
        session.add(topic2)
        session.add(topic3)
        session.add(topic4)
        session.add(topic5)

        problem1.topics.append(topic2)
        problem3.topics.append(topic5)
        problem5.topics.append(topic5)
        problem3.topics.append(topic2)
        problem1.topics.append(topic3)
        problem6.topics.append(topic3)
        problem7.topics.append(topic2)
        problem1.topics.append(topic1)
        problem2.topics.append(topic2)
        problem4.topics.append(topic3)
        problem4.topics.append(topic4)

        admin = Admin(id = ACCESS_ADMIN)

        session.add(admin)
        session.commit()
fullBase()
