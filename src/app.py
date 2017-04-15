""" creates and returns the actual application object """

from flask import Flask

from src.resources.projects import projects
from src.resources.auth import auth
from src.resources.person import people
from src.resources.applications import apps

# Keep create_app in a separate module so that it can be imported and used in
# tests without creating a new app just by importing run. That has side effects
# on the database connection.
def create_app(**config_overrides):
    """ Creates an application object, loads configuration, initializes
    addons (database, mail, auth provider, etc.) sets up any blueprints,
    and returns the application object """

    app = Flask(__name__,
                static_folder='static',
                static_url_path='',
                instance_relative_config=True)

    try:
        app.config.from_envvar('FLASK_SETTINGS')
    except RuntimeError:
        app.logger.error("Env var 'FLASK_SETTINGS' not set, could not \
override default configuration. The env var should be a path \
to a config file to use for this deployment.")

    # TODO set up database here

    app.config.update(config_overrides)

    app.register_blueprint(projects, url_prefix='/projects')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(people, url_prefix='/people')
    app.register_blueprint(apps, url_prefix='/app')

    return app
