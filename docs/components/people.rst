:mod:`People Module`
=============================

.. contents:: Contents
   :local:


Introduction
------------

This module allows for CRUD operations on a database of Olin community members.


Endpoints
---------

.. autoflask:: src.app:create_app(FLASK_SETTINGS="example_settings.py")
 :endpoints:
 :order: path
 :blueprints: people
 :undoc-static:
