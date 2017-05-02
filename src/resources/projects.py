""" Exists at `/projects` and offers endpoints to conduct CRUD operations on a
database of Olin projects """


from flask import Blueprint
from flask_restful import Resource, Api


# Blueprint setup
projects = Blueprint('projects', __name__)
api = Api(projects)


class Project(Resource):
    """ Allows for querying, editing, and inserting projects in the database.
    Not yet implemented.
    """

    def get(self, query):
        raise NotImplementedError

    def put(self, query):
        raise NotImplementedError

    def post(self, query):
        raise NotImplementedError

# Resources
api.add_resource(Project, '/')
