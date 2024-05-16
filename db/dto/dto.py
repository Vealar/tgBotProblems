import json
from db.models.models import Problem

class ProblemDTO:
    def __init__(self, id, level, text, solution):
        self.id = id
        self.level = level
        self.text = text
        self.solution = solution

    def to_dict(self):
        return {
            "id": self.id,
            "level": self.level,
            "text": self.text,
            "solution": self.solution
        }

class ServiceUserDTO:
    @staticmethod
    def serialize_problem(problem):
        return ProblemDTO(problem.id, problem.level.value, problem.text, problem.solution).to_dict()

    @staticmethod
    def serialize_solved_problems(problems):
        return [ServiceUserDTO.serialize_problem(problem) for problem in problems]

    @staticmethod
    def serialize_user(user):
        return {
            "id": user.id,
            "username": user.username,
            "problems_solved": ServiceUserDTO.serialize_solved_problems(user.problems_solved)
        }

    @staticmethod
    def serialize_users(users):
        return [ServiceUserDTO.serialize_user(user) for user in users]
class TopicDTO:
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "name": self.name
        }

class ServiceAdminDTO:
    @staticmethod
    def serialize_problem(problem):
        return ProblemDTO(problem.id, problem.level.value, problem.text, problem.solution).to_dict()

    @staticmethod
    def serialize_topic(topic):
        return TopicDTO(topic.name).to_dict()