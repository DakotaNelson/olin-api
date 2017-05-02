""" Exists at `/apps` and allows for registration of applications which
intend to use the Olin API """

from flask import Blueprint, request, make_response
from flask_restful import Resource, Api
from mongoengine.errors import NotUniqueError, ValidationError
from ..document_models import Application
from ..utils import send_email

# Blueprint setup
apps = Blueprint('apps', __name__)
api = Api(apps)


class RegisterApp(Resource):
    def post(self):
        """ Allows a user to register a client application with the Olin API.
        This will grant them an application token which can later be used to
        either access client-specific resources or request an authorization
        token that will grant the application access to the API on a user's
        behalf.

        Users must agree to the Olin API Honor Code at
        https://github.com/DakotaNelson/olin-api/blob/master/HONOR-CODE.md

        :param str contact: An email address to use as a designated contact \
                for the application.
        :param str name: The name of the application.
        :param bool honorcode: A boolean value indicating whether or not the \
                requester has read and agrees to the Olin API Honor Code.
        :param str description: A description of the application.
        :param str homepage: A URL pointing to the application's website.
        """

        params = request.get_json()

        # application point of contact email
        if not 'contact' in params:
            resp = {'message': 'Request must include \'contact\' parameter.'}
            return resp, 400

        # application name
        if not 'name' in params:
            resp = {'message': 'Request must include \'name\' parameter.'}
            return resp, 400

        # have they "signed" the honor code?
        # see `HONOR-CODE.md`
        if not 'honorcode' in params:
            resp = {'message': 'Request must include \'honorcode\' parameter '
                               'signifying that you will abide by the Olin API '
                               'Honor Code found at '
                               'https://github.com/DakotaNelson/olin-api'
                               '/blob/master/HONOR-CODE.md'}
            return resp, 400

        # TODO conversion to bool is gross and mistake-prone
        if  bool(params['honorcode']) != True:
            # TODO include link to honor code
            resp = {'message': 'You must agree to the Olin API Honor Code'
                               ' in order to use the Olin API.'}
            return resp, 400

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
            resp = {"message": "Application with that name and "
                               "contact email already exists."}
            return resp, 400
        except ValidationError:
            resp = {"message": "Application contact must be a properly "
                               "formatted email address, and application name "
                               "must be 140 characters or less."}
            return resp, 400

        # if the app successfully made it to the DB, add in its details
        # (double-save is inefficient but the code is simpler to grok)
        app.desc = desc
        app.homepage = homepage

        try:
            app.save()
        except ValidationError:
            resp = {"message": "Application homepage must be a properly "
                               "formatted URL. (Make sure to include "
                               "\'http://\')"}
            app.delete()
            return resp, 400

        # generate and return application auth token
        token = app.generate_token()

        # if creator's email isn't validated, send email with validation token
        if not app.validated:
            validation_token = app.generate_validation_token()

            validation_url = api.url_for(ValidateApp,
                                         token=validation_token,
                                         _external=True)

            # TODO actual email template that isn't terrible
            send_email(params['contact'],
                       "Here's your Olin-API validation token",
                       "<a href=\"{}\">Click here</a>".format(validation_url))

            resp = {'message': 'Success! Application will be valid once email '
                               'has been proven.',
                    'token': token,
                    'validated': False}
        else:
            # token is already valid
            resp = {'message': 'Success! Email has already been proven, so '
                               'you\'re good to go.',
                    'token': token,
                    'validated': True}

        return resp, 200

    # TODO some way to re-issue tokens
    # we can't allow just anyone to delete an app, but if we require the app
    # token to be included, what happens if they lose it? no way to re-issue
    # (we have their email, so we could re-verify it with another token)

    # def delete(self):
    #     """ Deletes an app record, rendering the associated token
    #     invalid and allowing for re-issuing a token. """
    #
    #     params = request.get_json()
    #
    #     # application point of contact email
    #     if not 'contact' in params:
    #         resp = {'message': 'Request must include \'contact\' parameter.'}
    #         return resp, 400
    #
    #     # application name
    #     if not 'name' in params:
    #         resp = {'message': 'Request must include \'name\' parameter.'}
    #         return resp, 400
    #
    #     Application.objects(contact=params['contact'],
    #                         name=params['name']).delete()
    #
    #     # security note: we don't want to say anything like "we couldn't find
    #     # that application" because it would allow people to fish for apps
    #     # being used in the API
    #     resp = {"message": "Success! If that application existed, it has been deleted."}
    #     return resp, 200


class ValidateApp(Resource):
    def get(self, token):
        """ Given a validation token (what is sent in an email to the token
        requester's email address), check that it is good, then mark the
        corresponding app as valid
        """
        if Application.verify_validation_token(token):
            resp = ('Success - thanks! Make sure you have read and understood '
                    'the <a href="https://github.com/DakotaNelson/olin-api/'
                    'blob/master/HONOR-CODE.md">Olin API Honor Code</a>.')
            # TODO better message/page for user? include name of authorized app?
            return make_response(resp, 200)
        else:
            resp = ('Unable to validate authentication token. Your validation '
                    'token is either invalid or expired.')
            return make_response(resp, 400)


class ListApps(Resource):
    def get(self):
        """ List all currently registered applications
        """
        apps = Application.objects()

        # TODO return more information
        apps_clean = []
        for app in apps:
            # don't include invalid apps
            if app["validated"] is True:
                apps_clean.append(
                    {"name": app["name"]}
                )

        return apps_clean, 200



# Resources
api.add_resource(ListApps, '/all')
api.add_resource(RegisterApp, '/register')
api.add_resource(ValidateApp, '/validate/<token>')
