import db
from db.models.models import Problem, User, Topic
from db.repositories.database import db
from db.dto.dto import ProblemDTO
class ServiceUser:
    @staticmethod
    def add_user(user):
        with db.session() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    @staticmethod
    def add_solved_problem(user_id, problem_id):
        with db.session() as session:
            problem = session.query(Problem).filter_by(id=problem_id).first()
            user = session.query(User).filter_by(id=user_id).first()
            if user and problem:
                user.problems_solved.append(problem)
                session.commit()
                return True
            return False

    @staticmethod
    def delete_solved_problem(user_id, problem_id):
        with db.session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            solved_problem = session.query(Problem).filter_by(id = problem_id).first()
            if user and solved_problem:
                user.problems_solved.remove(solved_problem)
                session.commit()
                return True
            return False

    @staticmethod
    def get_solved_problems(user_id):
        with db.session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                return [ProblemDTO(problem.id, problem.level, problem.text, problem.solution).to_dict() for problem in
                        user.problems_solved]
            return []

    @staticmethod
    def reset_user_history(user_id):
        with db.session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                user.problems_solved = []
                session.commit()
                return True
            return False

    @staticmethod
    def get_problem_by_topics(topics):
        with db.session() as session:
            problems = session.query(Problem).filter(Problem.topics.any(Topic.name.in_(topics))).all()
            return [ProblemDTO(problem.id, problem.level, problem.text, problem.solution).to_dict() for problem in
                    problems]

    @staticmethod
    def get_problem_by_level(level):
        with db.session() as session:
            problems = session.query(Problem).filter_by(level=level).all()
            return [ProblemDTO(problem.id, problem.level, problem.text, problem.solution).to_dict() for problem in
                    problems]

    @staticmethod
    def get_problem_by_level_and_topics(level, topics):
        with db.session() as session:
            problems = session.query(Problem).filter_by(level=level).filter(
                Problem.topics.any(Topic.name.in_(topics))).all()
            return [ProblemDTO(problem.id, problem.level, problem.text, problem.solution).to_dict() for problem in
                    problems]

    @staticmethod
    def get_problem_by_id(problem_id):
        with db.session() as session:
            problem = session.query(Problem).filter_by(id=problem_id).first()
            if problem:
                problem_string = f"ID: {problem.id}, Level: {problem.level}, Text: {problem.text}"
                return problem_string
            return "Problem not found."

    @staticmethod
    def get_solve_by_id(problem_id):
        with db.session() as session:
            problem = session.query(Problem).filter_by(id=problem_id).first()
            if problem:
                problem_string = f"ID: {problem.id}, Level: {problem.level}, Text: {problem.text}, Solution: {problem.solution}"
                return problem_string
            return "Problem not found."

    @staticmethod
    def get_all_problems():
        with db.session() as session:
            problems = session.query(Problem).all()
            problem_strings = []
            for problem in problems:
                problem_string = f"ID: {problem.id}, Level: {problem.level}, Text: {problem.text}"
                problem_strings.append(problem_string)
            return problem_strings


