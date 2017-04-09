import os

import sendgrid

from src.database_connection_mongoengine import make_connection

make_connection()

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
