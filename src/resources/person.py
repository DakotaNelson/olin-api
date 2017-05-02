""" Exists at `/people` and offers endpoints to conduct CRUD operations on a
database of Olin people """

from flask import Blueprint, request
from flask_restful import Resource, Api
from src.document_models import Person
from mongoengine.errors import NotUniqueError

# Blueprint setup
people = Blueprint('people', __name__)
api = Api(people)


# http://flask.pocoo.org/docs/0.12/api/#flask.Request


class PersonEndpoint(Resource):
    """ Allows for querying, editing, and inserting people in the database """

    def get(self):
        """
        Returns one or more user objects.

        :param str email: User's email address
        :param str fName: First name of the user
        :param str lName: Last name of the user
        :param int comYearMIN: Minimum community year of the user (inclusive)
        :param int comYearMAX: Maximum community year of the user (inclusive)
        """
        try:
            params = request.args
            query = Person.objects()
            if params.get('fName'):
                query = query.filter(fName = params['fName'])
            if params.get('lName'):
                query = query.filter(lName = params['lName'])
            if params.get('email'):
                query = query.filter(email = params['email'])
            if params.get('comYearMIN'):
                query = query.filter(comYear__gte = int(params['comYearMIN']))
            if params.get('comYearMAX'):
                query = query.filter(comYear__lte = int(params['comYearMAX']))
            return {'response': {'ok': 1.0}, 'results':[person.to_json() for person in query]}

        except Exception as e:
            return {'response': {'ok': 0.0, 'error': str(e)}, 'results': None}

    def put(self):
        try:
            params = request.args
            putQuery = Person.objects()
            if params.get('fName'):
                putQuery = putQuery.filter(fName = params['fName'])
            if params.get('lName'):
                putQuery = putQuery.filter(lName = params['lName'])
            if params.get('email'):
                putQuery = putQuery.filter(email = params['email'])
            if params.get('comYearMIN'):
                putQuery = putQuery.filter(comYear__gte = int(params['comYearMIN']))
            if params.get('comYearMAX'):
                putQuery = putQuery.filter(comYear__lte = int(params['comYearMAX']))
            edited_ids = [person.id for person in putQuery]
            serverResponse = putQuery.update(full_result = True, **request.json)
            return {'response': serverResponse, 'results': [person.to_json() for person in Person.objects(id__in = edited_ids)]}

        except NotUniqueError: #email is the only unique index users can access, since object id cannot be searched or created manually.
            return {'response': {'ok': 0.0, 'error': "Email {} already exists".format(request.json['email'])}, 'results': None}

        except Exception as e:
            return {'response': {'ok': 0.0, 'error': str(e)}, 'results': None}


    def post(self):
        """
        If requests.json's fields do not match those defined in the Person model, this fails.
        See documentation for src.document_models.Person for more details.
        """

        # TODO add parameter documentation for sphinx
        try:
            object = Person(**request.json)
            object.save()
            return {'response': {'ok': 1.0}, 'results': object.to_json()}

        except NotUniqueError:
            return {'response': {'ok': 0.0, 'error': "Email {} already exists".format(request.json['email'])}, 'results': None}

        except Exception as e:
            return {'response': {'ok': 0.0, 'error': str(e)}, 'results': None}




# Resources
api.add_resource(PersonEndpoint, '/') #url_prefix is registered as /people in src/app.py
