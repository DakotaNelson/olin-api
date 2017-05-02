:mod:`Authentication Module`
============================

.. contents:: Contents
   :local:

Introduction
------------

The authentication component allows applications to authenticate that a user does in fact own an email address that they claim. Once this flow is completed, an auth token is issued, which allows the application to access resources on that user's behalf.

.. image:: http://www.plantuml.com/plantuml/png/VL51JWCn3BplAwoUu50UK2541Hnw0bNYniNA6cerwuJ4suAqZyURBAXe2wT8pinuPenEGuBdJAc9c9GTHnI5nPrd4dsHTOoU7Ie7MG1cgFFVs4VF0kkdJG7OsunoiBoPm2lOqdjFMI6ceEIKMaYKGvySLUZrSWQb3ja3jgqXyqnG3N9B7zX5JrSkTCqm34tz767cOGKRE8xk43JiIU3LOive4yNs5ygMSWoI2OwiEy1UT_OxfPzaBYGeV9B20JstbsNnTuQYyL2CQvWj0nT4aONbhP9FP7y25WbpvVPWfUx1YgrD_4S-4zxqplitO-YSTVht2Ux9yy56gPxYv5fV
    :align: center
    :alt: User authentication flow diagram in PlantUML


.. @startuml
.. actor User
.. participant "Client\nApplication" as Client
.. participant "Olin API" as API
.. User -> Client: Request protected resource
.. User <- Client: Request email address
.. User -> Client: test@example.com
.. |||
.. Client -> API: I want a token for test@example.com
.. Client <- API: Response with authentication token (not yet valid)
.. |||
.. User <- API: Email to test@example.com containing validation token
.. User -> API: Click link in email containing validation token
.. |||
.. Client -> API: Use authentication token to access resource
.. User <- Client: Deliver requested resource
.. @enduml


Glossary
--------

Application Token
^^^^^^^^^^^^^^^^^

Issued when a user registers an application. Requires verification of the application's contact email address before the token is marked valid. Allows for accessing application-level resources. Required in order to request an auth token.

Auth Token
^^^^^^^^^^^^^^^^^

Issued when a client application requests one. Scoped to a single email address, which is verified before the token is marked valid. Allows for requesting resources on behalf of the provided email address.

Validation Token
^^^^^^^^^^^^^^^^^

Used for email validation. Sent in a link to the specified email when an auth token is requested, or to the application contact email when an application token is requested.


Endpoints
---------

.. autoflask:: src.app:create_app(FLASK_SETTINGS="example_settings.py")
 :endpoints:
 :order: path
 :blueprints: auth
 :undoc-static:
