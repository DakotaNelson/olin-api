""" Contains all of the mongoengine models for data held in mongo """

from mongoengine import Document, StringField, IntField

class Person(Document):
    """
    Fields:
    fName           First Name. Required, takes a string with maximum length 240.
    lName           Last Name. Required, takes a string with maximum length 240.
    communityYear   Community Year (which year the person joined the olin community)
                    Not required, takes an integer.
    """
    fName = StringField(max_length=240, required=True)
    lName = StringField(max_length=240, required=True)
    communityYear = IntField()
