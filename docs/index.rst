Olin-API
========

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   components/auth
   components/app
   components/people

Welcome to the `Olin-API <https://github.com/DakotaNelson/olin-api>`_ docs!

Olin-api seeks to provide programmatic access to a wide variety of Olin College digital resources. It is meant to provide the foundation for a variety of student-built applications to benefit the community.

The API is organized as a series of modules, each of which provides a unique service to those using it.

:doc:`components/app`
---------------------

This module allows applications to register themselves with the API in order to access further API resources. It also allows clients to list applications which have been registered with the API.


:doc:`components/auth`
----------------------

This module provides authentication services to client applications. Specifically, it is able to verify whether or not any given user is in control of an email address they claim. This allows applications to verify that their users are, for example, in control of an ``@students.olin.edu`` email address and therefore allowed to access community-only resources.


:doc:`components/people`
------------------------

This module allows for CRUD operations on a database of Olin community members.
