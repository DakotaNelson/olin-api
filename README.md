# olin-api

Olin-api seeks to provide programmatic access to a wide variety of Olin College digital resources. It is meant to provide the foundation for a variety of student-built applications to benefit the community.

This README primarily covers getting started developing on the API code itself. If you'd like to simply use the existing API resources, you can refer to the [usage docs](http://olin-api.readthedocs.io).

# Getting Started

**First: read and understand the [Olin API Honor Code](HONOR-CODE.md).**

The `./bin/` directory contains a number of scripts which will help you get started:

 - `lint.sh` - lint the codebase to ensure quality
 - `test.sh` - run unit tests
 - `readthedocs.sh` - generate and serve the project's documentation
 - `run.sh` - run the project itself
 - `setUpEnv.sh` - installs dependencies for the project

## Quickstart

First, make sure MongoDB is running and accepting connections. Then,

`bin/setUpEnv.sh && bin/run.sh`

### Configuration

Right now, configuration is stored both in `.env` and `instance/default_settings.py`. This is gross, and should be changed.

You will find examples of configuration variables stored in `.env.example` and `instance/example_settings.py`. These variables are not ready for production, but might let you run locally. Either way, you'll need to copy them to `.env` and `instance/default_settings.py`. `.env` is automatically sourced when you run `heroku local` (which is what `run.sh` relies on), which results in all of the key value pairs being present as environment variables in your shell available to the python process running olin-api. The `instance/default_settings.py` file is used by [Flask's configuration system](http://flask.pocoo.org/docs/0.12/config/). If you would like to use a different file, you can set the `FLASK_SETTINGS` variable in `.env` to whatever filename you'd like, and Flask will look for that filename in the `instance` folder.

In addition, you can add overrides in `run.py`, directly into the `app.run()` function call. These will take precedence over anything in `.env` or `*_settings.py`


# API Components

### Authentication

 The authentication component allows for API users to prove that they own an email. Devlopers utilizing this component can then proceed with trust that the user controls the email account that they claim to be.

 The auth flow is as such:

1. POST request is issued to `/auth` containing an email address. The API returns a JSON Web Signature (JWS) token (referred to here as the "auth token") and sends an email to the specified email address containing another token (referred to here as the "validation token").

2. The user visits their email and clicks a link containing the validation token in the form `/auth/token/validate/<validation_token>`.

3. The API ensures that the validation token is correct, and if so marks the auth token as valid, allowing it to be used for 1 year. Any resource which is accessed with this auth token can assume that the requester is in fact in control of the email address they have validated.

The largest oddity here is that the API does not store auth tokens: since they are tamper-proof and self-expiring cryptographic tokens, they do not need to be checked against a secure database. The API merely stores a structure which contains an email and a "validated" flag indicating whether or not that email currently has a valid token.

Full authentication documentation can be found [here](AUTH.md).


### People
