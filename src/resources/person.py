""" Exists at `/people` and offers endpoints to conduct CRUD operations on a
database of Olin people """

from flask import Blueprint, request
from flask_restful import Resource, Api
from src.document_models import Person
# from src.database_connection_mongoengine import handle_get_request

# Blueprint setup
people = Blueprint('people', __name__)
api = Api(people)


# http://flask.pocoo.org/docs/0.12/api/#flask.Request


class Person(Resource):
    """ Allows for querying, editing, and inserting people in the database """

    def get(self):
        raise NotImplementedError

    def put(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError


# Resources
api.add_resource(Person, '/') #url_prefix is registered as /people in src/app.py

