""" Exists at `/auth` and allows for authentication of users """

from flask import Blueprint, request, jsonify, make_response
from flask_restful import Resource, Api
from mongoengine.errors import DoesNotExist
from ..document_models import Token
from ..utils import send_email

# Blueprint setup
auth = Blueprint('auth', __name__)
api = Api(auth)


class RequestToken(Resource):
    def post(self):
        """ Returns an access token against an email address which will be
        valid once the specified email address is verified (by clicking a link
        in an email sent to it)

        If called multiple times, will simply return the same auth token. """

        params = request.get_json()

        if not 'email' in params:
            resp = {'message': 'Request must include \'email\' parameter.'}
            return make_response(jsonify(resp), 400)

        # try to find a matching token that already exists, or create a new one
        # could do an upsert here, but it'd be less readable
        try:
            token = Token.objects(email=params['email']).get()
        except DoesNotExist:
            token = Token(email=params['email']).save()

        token_value = token.generate_token()

        # if auth token isn't validated, send email with validation token
        if not token.validated:
            validation_token = token.generate_validation_token()

            validation_url = api.url_for(ValidateToken,
                token=validation_token,
                _external=True)

            send_email(params['email'],
                       "Here's your Olin-API validation token",
                       "<a href=\"{}\">Click here</a>".format(validation_url))

            resp = {'message': 'Success! Token will be valid once email has been proven.', 'token': token_value, "validated": False}
        else:
            # token is already valid
            resp = {'message': 'Success! Email has already been proven, so you\'re good to go.', 'token': token_value, "validated": True}
        return make_response(jsonify(resp), 200)

    def delete(self):
        """ Deletes an access token record, rendering the associated token
        invalid and allowing for re-issuing a token. """

        params = request.get_json()

        if not 'email' in params:
            resp = {'message': 'Request must include \'email\' parameter.'}
            return make_response(jsonify(resp), 400)

        token = Token.objects(email=params['email']).delete()

        # security note: we don't want to say anything like "we couldn't find
        # that email" because it would allow people to fish for emails being
        # used in the API
        resp = {"message": "Success! If there was a token associated with that email address, it has been deleted."}
        return make_response(jsonify(resp), 200)


class ValidateToken(Resource):
    def get(self, token):
        """ Given a validation token (what is sent in an email to the token
        requester's email address), check that it is good, then mark the
        corresponding token as valid """
        if Token.verify_validation_token(token):
            resp = 'Success! Thanks!' # TODO better message/page for user?
            return resp, 200
        else:
            resp = 'Unable to validate authentication token. Your validation token is either invalid or expired.'
            return resp, 400


class Authenticate(Resource):
    def post(self):
        """ Given an authentication token, returns a person profile OR a
        message stating the token is invalid """
        raise NotImplementedError


# Resources
api.add_resource(Authenticate, '')
api.add_resource(RequestToken, '/token')
api.add_resource(ValidateToken, '/token/<token>/validate')
