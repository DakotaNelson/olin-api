from mongoengine import Document, StringField, IntField

class Person(Document):
    """
    Fields:
    fName - First Name. Required, takes a string with maximum length 240.
    lName - Last Name. Required, takes a string with maximum length 240.
    communityYear - Community Year (which year the person joined the olin community). Not required, takes an integer.
    """
    fName = StringField(max_length = 240, required = True)
    lName = StringField(max_length = 240, required = True)
    communityYear = IntField()
    #Once we make a user, we can probably reference that user in another document by putting a Person object into a ReferenceField.

