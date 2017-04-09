# olin-api

Olin-api seeks to provide programmatic access to a wide variety of Olin College digital resources. It is meant to provide the foundation for a variety of student-built applications to benefit the community.

# Getting Started

The `./bin/` directory contains a number of scripts which will help you get started:

 - `lint.sh` - lint the codebase to ensure quality
 - `readthedocs.sh` - generate and serve the project's documentation
 - `run.sh` - run the project itself
 - `setUpEnv.sh` - installs dependencies for the project

## Quickstart

 `bin/setUpEnv.sh && bin/run.sh`


# API Components

### Authentication

 The authentication component allows for API users to prove that they own an email. Devlopers utilizing this component can then proceed with trust that the user controls the email account that they claim to be.

 The auth flow is as such:

1. POST request is issued to `/auth` containing an email address. The API returns a JSON Web Signature (JWS) token (referred to here as the "auth token") and sends an email to the specified email address containing another token (referred to here as the "validation token").

2. The user visits their email and clicks a link containing the validation token in the form `/auth/token/validate/<validation_token>`.

3. The API ensures that the validation token is correct, and if so marks the auth token as valid, allowing it to be used for 24 hours. Any resource which is accessed with this auth token can assume that the requester is in fact in control of the email address they have validated.

The largest oddity here is that the API does not store auth tokens: since they are tamper-proof and self-expiring cryptographic tokens, they do not need to be checked against a secure database. The API merely stores a structure which contains an email and a "validated" flag indicating whether or not that email currently has a valid token.


### People
