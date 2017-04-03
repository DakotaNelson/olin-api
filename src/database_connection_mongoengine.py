""" Methods for connecting to and managing MongoDB """

import os

from mongoengine import connect

### Resources ###
# http://docs.mongoengine.org/


### Database Interaction ###

def make_connection(requestLocation=None):
    """
    Connects a user to a database on the mongoDB server.

    requestLocation    the name of the database the user wants to connect to
                       either None or a string.
    """
    if os.environ.get('MONGODB_URI'):
        uri = os.environ.get('MONGODB_URI')
    else:
        uri = 'mongodb://localhost:27017/'
    if not requestLocation:
        databaseName = 'test'
    else:
        databaseName = requestLocation
    connect(databaseName, host=uri)
