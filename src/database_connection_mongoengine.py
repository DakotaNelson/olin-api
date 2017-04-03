from mongoengine import *
import os

from src.document_models import *

### Resources ###
# http://docs.mongoengine.org/


### Database Interaction ###

def make_connection(requestLocation=None):
    """
    Connects a user to a database on the mongoDB server.
    requestLocation is the name of the database the user wants to connect to, and is either None or a string.
    By default, a database has enough space for ~24000 collection namespaces.
    """
    if os.environ.get('MONGODB_URI'):
        uri = os.environ.get('MONGODB_URI')
    else:
        uri = 'mongodb://localhost:27017/'
    if not requestLocation:
        databaseName = 'test'
    else:
        databaseName = requestLocation
    connect(databaseName, host = uri) #is this global? It shouldn't be too much of a problem since we're running this once for each request.
