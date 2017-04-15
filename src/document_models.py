""" Contains all of the mongoengine models for data held in mongo """
from flask import current_app

from mongoengine import (Document, StringField, IntField,
                         DictField, EmailField, BooleanField, DoesNotExist,
                         URLField)

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          URLSafeTimedSerializer,
                          BadSignature,
                          SignatureExpired)

class Person(Document):
    """
    Represents a real, actual, honest-to-goodness person.

    Fields:
    fName           First Name. Required.
                    Takes a string with maximum length 240.
                    Example: "John"

    lName           Last Name. Required.
                    Takes a string with maximum length 240.
                    Example: "Smith"

    comYear         Community Year (year the person joined the olin community)
                    Not required, takes an integer.
                    Example: 2015

    email           Email. Required, takes a string.
                    Example: "JohnSmith@students.olin.edu"

    pronouns        Personal pronouns. Not required, takes a string.
                    Example: "He/Him/His"

    services        Other services associated with this person.
                    Not required, takes a dictionary.
                    Example: {"venmo":"jSmith50", "messenger":"Smithee"}

    """
    fName = StringField(max_length=240, required=True)
    lName = StringField(max_length=240, required=True)
    comYear = IntField()
    email = EmailField(max_length=100, required=True, unique=True, sparse=True)
    pronouns = StringField(max_length=100)
    preferredName = StringField(max_length=240)
    services = DictField()

    # TODO: other fields
    # add role at Olin
    # BOW students?
    # allergies/diet
    # image/gravatar

class Token(Document):
    """ Represents an authorization token that allows a user to delegate a client
    application access to the Olin API on their behalf. """
    email = EmailField(max_length=100, required=True, unique=True)
    # 'validated' is marked as true once the user has confirmed they own the
    # email address the validation token is sent to
    validated = BooleanField(default=False)

    def generate_token(self, expiration=86400 * 365):
        """ Generate an authentication token, by default good for 1 year """
        serializer = Serializer(
            current_app.config['SECRET_KEY'], expires_in=expiration)
        return serializer.dumps({'email': self.email}).decode(encoding='UTF-8')

    @staticmethod
    def verify_token(token):
        """ ensures that the login token passed to it is valid, returns
        the correct person object based on the token passed to it """
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        token = Token.objects.get(email=data['email'])
        if token.validated is False:
            return None # token not validated

        # otherwise, success!
        #person = Person.objects.get(email=data['email'])
        # disabled - this creates an unfortunate linkage between the API types
        # (i.e. what do we do if someone has no person profile but we still
        # want to auth them?)
        return True

    def generate_validation_token(self):
        """ Creates and saves an token to be sent in an email to the email
        address provided during auth flow. This proves ownership of that
        email by the user undertaking the auth flow."""
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        # 'salt' is actually a namespace - see:
        # http://pythonhosted.org/itsdangerous/#the-salt
        salt = current_app.config['VALIDATION_TOKEN_SALT']
        return serializer.dumps(self.email, salt=salt)

    @staticmethod
    def verify_validation_token(token, expiration=12*3600):
        """ verifies a registration token, sets the 'validated' field of the
        corresponding token to True """
        salt = current_app.config['VALIDATION_TOKEN_SALT']
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=salt,
                max_age=expiration)
        except:
            return False
        try:
            tokenObj = Token.objects.get(email=email)
            tokenObj.validated = True
            tokenObj.save()
        except DoesNotExist:
            # for some reason, we're validating a token that doesn't exist...
            return False

        return True

class Application(Document):
    """ Represents a client application developed to use the Olin API. """
    # who can we contact about this application?
    contact = EmailField(max_length=100, required=True)
    # what is the application's name? (one contact can't have two identically
    # named applications)
    name = StringField(max_length=140, required=True, unique_with='contact')
    # what is the application?
    description = StringField()
    # where can people learn more?
    homepage = URLField()

    def generate_token(self, expiration=86400 * 365 * 4):
        """ Generate an authentication token, by default good for ~4 years """
        serializer = Serializer(
            current_app.config['SECRET_KEY'], expires_in=expiration)
        return serializer.dumps({'contact': self.contact, 'name': self.name}) \
                         .decode(encoding='UTF-8')

    @staticmethod
    def verify_token(token):
        """ ensures that the application token passed to it is valid, returns
        the correct app object based on the token passed to it """
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        # otherwise, success!
        app = Application.objects.get(contact=data['contact'], name=data['name'])
        return app
