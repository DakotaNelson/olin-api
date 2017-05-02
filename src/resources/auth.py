""" Exists at `/auth` and allows for authentication of users """

from flask import Blueprint, request, make_response
from flask_restful import Resource, Api
from mongoengine.errors import DoesNotExist
from ..document_models import Token, Application
from ..utils import send_email

# Blueprint setup
auth = Blueprint('auth', __name__)
api = Api(auth)


class RequestToken(Resource):
    def post(self):
        """ Returns an access token against an email address which will be
        valid once the specified email address is verified (by clicking a link
        in an email sent to it)

        If called multiple times, will simply return the same auth token.

        :param str email: Email address to validate and return an access \
                token for.
        :param str apptoken: An application token verifying that the calling \
                application has registered itself, provided a contact, agreed \
                to the Olin API Honor code, etc.
        """

        params = request.get_json()

        # TODO rate limit, else we can be used to spam people
        if not 'email' in params:
            resp = {'message': 'Request must include \'email\' parameter.'}
            return resp, 400

        if not 'apptoken' in params:
            resp = {'message': 'Request must include \'apptoken\' parameter.'}
            return resp, 400

        app = Application.verify_token(params['apptoken'])
        if app is None:
            resp = {'message': 'Application token is invalid.'}
            return resp, 401

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

            # TODO actual email template that isn't terrible
            send_email(params['email'],
                       "Here's your Olin-API validation token",
                       "<a href=\"{}\">Click here</a>".format(validation_url))

            resp = {'message': 'Success! Token will be valid once email has been proven.',
                    'token': token_value, "validated": False}
        else:
            # token is already valid
            resp = {'message': 'Success! Email has already been proven, so you\'re good to go.',
                    'token': token_value, "validated": True}
        return resp, 200

    def delete(self):
        """ Deletes an access token record, rendering the associated token
        invalid and allowing for re-issuing a token.

        :param str email: Email for the token to delete.
        :param str apptoken: An application token verifying that the calling \
                application has registered itself, provided a contact, agreed \
                to the Olin API Honor code, etc.
        """

        params = request.get_json()

        if not 'email' in params:
            resp = {'message': 'Request must include \'email\' parameter.'}
            return resp, 400

        if not 'apptoken' in params:
            resp = {'message': 'Request must include \'apptoken\' parameter.'}
            return resp, 400

        app = Application.verify_token(params['apptoken'])
        if app is None:
            resp = {'message': 'Application token is invalid.'}
            return resp, 401

        Token.objects(email=params['email']).delete()

        # security note: we don't want to say anything like "we couldn't find
        # that email" because it would allow people to fish for emails being
        # used in the API
        resp = {"message": "Success! If there was a token associated with that email address, it has been deleted."}
        return resp, 200


class ValidateToken(Resource):
    def get(self, token):
        """ Given a validation token (what is sent in an email to the token
        requester's email address), check that it is good, then mark the
        corresponding token as valid
        """
        if Token.verify_validation_token(token):
            resp = 'Success! Thanks!'
            # TODO better message/page for user? include name of authorized app?
            return make_response(resp, 200)
        else:
            resp = 'Unable to validate authentication token. Your validation token is either invalid or expired.'
            return make_response(resp, 400)


class Authenticate(Resource):
    def post(self):
        """ Given an authentication token, returns a person profile OR a
        message stating the token is invalid

        :param str token: The authentication token to check.

        """

        params = request.get_json()

        if not 'token' in params:
            resp = {'message': 'Request must include \'token\' parameter.'}
            return resp, 400

        email = Token.verify_token(params['token'])

        if email is None:
            resp = {'message': 'Invalid auth token.', 'valid': False}
            return resp, 401

        resp = {'message': 'Success! Auth token is valid.',
                'email': email,
                'valid': True}
        return resp, 200




# Resources
api.add_resource(Authenticate, '')
api.add_resource(RequestToken, '/token')
api.add_resource(ValidateToken, '/token/validate/<token>')
