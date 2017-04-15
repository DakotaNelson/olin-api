""" Exists at `/auth` and allows for authentication of users """

from flask import Blueprint, request, jsonify, make_response
from flask_restful import Resource, Api
from ..document_models import Token
from ..utils import send_email

# Blueprint setup
auth = Blueprint('auth', __name__)
api = Api(auth)


class RequestToken(Resource):
    def post(self):
        """ Returns an access token against an email address which will be valid once the specified
        email address is verified (by clicking a link in an email sent to it) """

        params = request.get_json()

        if not 'email' in params:
            resp = {'message': 'Request must include \'email\' parameter.'}
            return make_response(jsonify(resp), 400)

        # create a token object, and the actual string value of the token itself
        # TODO find and update OR create
        token = Token(email=params['email']).save()
        token_value = token.generate_token()

        # send email with the validation token
        validation_token = token.generate_validation_token()

        validation_url = api.url_for(ValidateToken,token=validation_token, _external=True)
        send_email(params['email'],
                   "Here's your Olin-API validation token",
                   "<a href=\"{}\">Click here</a>".format(validation_url))

        resp = {'message': 'Success! Token will be valid once email has been proven.', 'token': token_value}
        return make_response(jsonify(resp), 200)


class ValidateToken(Resource):
    def get(self, token):
        """ Given a validation token (what is sent in an email to the token requester's email address),
        check that it is good, then mark the corresponding token as valid """
        if Token.verify_validation_token(token):
            resp = 'Success! The token returned from your previous API request is now valid for 24 hours.'
            return resp, 200
        else:
            resp = 'Unable to validate authentication token. Your validation token is either invalid or expired.'
            return resp, 400

class Authenticate(Resource):
    def post(self):
        """ Given an authentication token, returns a person profile OR a message stating the token is invalid """
        raise NotImplementedError


# Resources
api.add_resource(RequestToken, '') #url_prefix registered as /auth in src/app.py
api.add_resource(ValidateToken, '/token/validate/<token>') #url_prefix registered as /auth in src/app.py
