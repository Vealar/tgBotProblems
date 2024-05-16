from sqlalchemy.orm import sessionmaker
from db.models.models import Topic, Problem
from db.repositories.database import db

class ServiceAdmin:
    @staticmethod
    def add_topic(name):
        with db.session() as session:
            topic = Topic(name=name)
            session.add(topic)
            session.commit()
            session.refresh(topic)
            return topic
    @staticmethod
    def delete_topic(name):
        with db.session() as session:
            topic = session.query(Topic).filter_by(name=name).first()
            if topic:
                session.delete(topic)
                session.commit()
                return True
            return False
    @staticmethod
    def add_problem(level, text, solution):
        with db.session() as session:
            problem = Problem(level=level, text=text, solution=solution)
            session.add(problem)
            session.commit()
            session.refresh(problem)
            return problem
    @staticmethod
    def delete_problem(problem_id):
        with db.session() as session:
            problem = session.query(Problem).filter_by(id=problem_id).first()
            if problem:
                session.delete(problem)
                session.commit()
                return True
            return False
    @staticmethod
    def update_problem_description(problem_id, text):
        with db.session() as session:
            problem = session.query(Problem).filter_by(id=problem_id).first()
            if problem:
                problem.text = text
                session.commit()
                return True
            return False
    @staticmethod
    def update_problem_solution(problem_id, solution):
        with db.session() as session:
            problem = session.query(Problem).filter_by(id=problem_id).first()
            if problem:
                problem.solution = solution
                session.commit()
                return True
            return False
    @staticmethod
    def update_problem_level(problem_id, level):
        with db.session() as session:
            problem = session.query(Problem).filter_by(id=problem_id).first()
            if problem:
                problem.level = level
                session.commit()
                return True
            return False

    @staticmethod
    def add_topics_to_problem(problem_id, topics):
        with db.session() as session:
            problem = session.query(Problem).filter_by(id=problem_id).first()
            if not problem:
                return False
            for topic_name in topics:
                topic = session.query(Topic).filter_by(name=topic_name).first()
                if topic:
                    problem.topics.append(topic)
            session.commit()
            return True

    @staticmethod
    def remove_topics_from_problem(problem_id, topics):
        with db.session() as session:
            problem = session.query(Problem).filter_by(id=problem_id).first()
            if not problem:
                return False
            for topic_name in topics:
                topic = session.query(Topic).filter_by(name=topic_name).first()
                if topic and topic in problem.topics:
                    problem.topics.remove(topic)
            session.commit()
            return True
