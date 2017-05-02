:mod:`Application Module`
==================================

.. contents:: Contents
   :local:

Introduction
------------

The application component allows applications to register themselves, at which point they are issued an application token. The application token allows access to application-scoped resources.

.. image:: http://www.plantuml.com/plantuml/png/VP2nJWCn38RtUmgh4mnz0LGXLOM12LIf6ulbMc1TS4BYjaAwXw-RonKTbPYSn9___B-HB6POR8Am6coY6f8j0CjqxX9c4vA4tc_SkwvJ2a9e4dM4w_kSVGsYi7vxgO3NhdsoVBpS7c3BtmSk1lYh1HPxrWbSBIUmfAY5uIJsUOl3dKQ37pOuOf3zVJSCGzVSNpMUlr22yq2ZDhL-hQAY7-Fqp4PZ9iDkYthmL3ruCgwA_yrN7_FCEqzn6y1j8H6N0fbBF6JYlojuuY17pjwlE-FzbJm3
    :align: center
    :alt: Application authentication flow diagram in PlantUML

.. @startuml
.. actor "Client Contact" as Contact
.. participant "Client\nApplication" as Client
.. participant "Olin API" as API
.. Client -> API: Request application token
.. Client <- API: Response with application token (not yet valid)
.. |||
.. Contact <- API: Email to client contact containing validation token
.. Contact -> API: Click link in email containing validation token
.. |||
.. Client -> API: Use application token to access resource
.. Client <- API: Deliver requested resource
.. @enduml


Glossary
--------

Application Token
^^^^^^^^^^^^^^^^^

Issued when a user registers an application. Requires verification of the application's contact email address before the token is marked valid. Allows for accessing application-level resources. Required in order to request an auth token.

Validation Token
^^^^^^^^^^^^^^^^^

Used for email validation. Sent in a link to the specified email when an auth token is requested, or to the application contact email when an application token is requested.


Endpoints
---------

.. autoflask:: src.app:create_app(FLASK_SETTINGS="example_settings.py")
 :endpoints:
 :order: path
 :blueprints: apps
 :undoc-static:
