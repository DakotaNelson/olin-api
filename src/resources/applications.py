""" Exists at `/apps` and allows for registration of applications which
intend to use the Olin API """

from flask import Blueprint, request, jsonify, make_response
from flask_restful import Resource, Api
from mongoengine.errors import NotUniqueError, ValidationError
from ..document_models import Application

# Blueprint setup
apps = Blueprint('apps', __name__)
api = Api(apps)


class RegisterApp(Resource):
    def post(self):
        params = request.get_json()

        # application point of contact email
        if not 'contact' in params:
            resp = {'message': 'Request must include \'contact\' parameter.'}
            return make_response(jsonify(resp), 400)

        # application name
        if not 'name' in params:
            resp = {'message': 'Request must include \'name\' parameter.'}
            return make_response(jsonify(resp), 400)

        # have they "signed" the honor code?
        if not 'honorcode' in params:
            resp = {'message': 'Request must include \'honorcode\' parameter.'}
            return make_response(jsonify(resp), 400)

        # TODO conversion to bool is gross and mistake-prone
        if not bool(params['honorcode']) == True:
            # TODO include link to honor code
            resp = {'message': 'You must agree to the Olin API Honor Code in order to use the Olin API.'}
            return make_response(jsonify(resp), 400)

        try:
            desc = params['description']
        except KeyError:
            desc = None

        try:
            homepage = params['homepage']
        except KeyError:
            homepage = None

        # get the basics saved to the db
        app = Application(contact=params['contact'], name=params['name'])

        try:
            app.save()
        except NotUniqueError:
            resp = {"message": "Application with that name and contact email already exists."}
            return make_response(jsonify(resp), 400)
        except ValidationError:
            resp = {"message": "Application contact must be a properly formatted email address, and application name must be 140 characters or less."}
            return make_response(jsonify(resp), 400)

        # if the app successfully made it to the DB, add in its details
        # (double-save is inefficient but the code is simpler to grok)
        app.desc = desc
        app.homepage = homepage

        try:
            app.save()
        except ValidationError:
            resp = {"message": "Application homepage must be a properly formatted URL. (Make sure to include \'http://\')"}
            app.delete()
            return make_response(jsonify(resp), 400)

        # generate and return application auth token
        token = app.generate_token()

        resp = {'message': 'Success!', 'token': token}
        return make_response(jsonify(resp), 200)


# Resources
api.add_resource(RegisterApp, '/register')
