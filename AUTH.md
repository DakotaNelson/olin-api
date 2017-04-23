Auth Flow
========

There are two distinct authentication flows used in the Olin API. The first allows applications to register themselves, at which point they are issued an application token. The application token allows access to application-scoped resources. One of these resources is the second authentication flow, which allows applications to authenticate that a user does in fact own an email address that they claim. Once this flow is completed, an auth token is issued, which allows the application to access resources on that user's behalf.


## Application Authentication Flow

This flow uses `src/resources/applications.py`.

![Application authentication flow diagram in PlantUML](http://www.plantuml.com/plantuml/png/VP2nJWCn38RtUmgh4mnz0LGXLOM12LIf6ulbMc1TS4BYjaAwXw-RonKTbPYSn9___B-HB6POR8Am6coY6f8j0CjqxX9c4vA4tc_SkwvJ2a9e4dM4w_kSVGsYi7vxgO3NhdsoVBpS7c3BtmSk1lYh1HPxrWbSBIUmfAY5uIJsUOl3dKQ37pOuOf3zVJSCGzVSNpMUlr22yq2ZDhL-hQAY7-Fqp4PZ9iDkYthmL3ruCgwA_yrN7_FCEqzn6y1j8H6N0fbBF6JYlojuuY17pjwlE-FzbJm3)

```
@startuml
actor "Client Contact" as Contact
participant "Client\nApplication" as Client
participant "Olin API" as API
Client -> API: Request application token
Client <- API: Response with application token (not yet valid)
|||
Contact <- API: Email to client contact containing validation token
Contact -> API: Click link in email containing validation token
|||
Client -> API: Use application token to access resource
Client <- API: Deliver requested resource
@enduml
```


## User Authentication Flow

This flow uses `src/resources/auth.py`.

![User authentication flow diagram in PlantUML](http://www.plantuml.com/plantuml/png/VL51JWCn3BplAwoUu50UK2541Hnw0bNYniNA6cerwuJ4suAqZyURBAXe2wT8pinuPenEGuBdJAc9c9GTHnI5nPrd4dsHTOoU7Ie7MG1cgFFVs4VF0kkdJG7OsunoiBoPm2lOqdjFMI6ceEIKMaYKGvySLUZrSWQb3ja3jgqXyqnG3N9B7zX5JrSkTCqm34tz767cOGKRE8xk43JiIU3LOive4yNs5ygMSWoI2OwiEy1UT_OxfPzaBYGeV9B20JstbsNnTuQYyL2CQvWj0nT4aONbhP9FP7y25WbpvVPWfUx1YgrD_4S-4zxqplitO-YSTVht2Ux9yy56gPxYv5fV)

```
@startuml
actor User
participant "Client\nApplication" as Client
participant "Olin API" as API
User -> Client: Request protected resource
User <- Client: Request email address
User -> Client: test@example.com
|||
Client -> API: I want a token for test@example.com
Client <- API: Response with authentication token (not yet valid)
|||
User <- API: Email to test@example.com containing validation token
User -> API: Click link in email containing validation token
|||
Client -> API: Use authentication token to access resource
User <- Client: Deliver requested resource
@enduml
```

<!-- see http://plantuml.com/sequence-diagram -->


### Glossary

#### Application Token

Issued when a user registers an application. Requires verification of the application's contact email address before the token is marked valid. Allows for accessing application-level resources. Required in order to request an auth token.

#### Auth Token

Issued when a client application requests one. Scoped to a single email address, which is verified before the token is marked valid. Allows for requesting resources on behalf of the provided email address.

#### Validation Token

Used for email validation. Sent in a link to the specified email when an auth token is requestd, or to the application contact email when an application token is requested.
