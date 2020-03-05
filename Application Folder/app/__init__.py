# app/__init__.py

# third-party imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
import logging

# local imports
from config import get_app_config

# db variable initialization
db = SQLAlchemy()

# Initialize login manager
login_manager = LoginManager()


def create_app():

    # Initialize App with Congfig
    app = Flask(__name__, instance_relative_config=True)
    # Load environment specific config
    app.config.from_object(get_app_config())
    # Load sensitive config
    app.config.from_pyfile('config.py')
    
    # DB Connection
    db.init_app(app)


    # Configure Login Manager
    login_manager.session_protection = "strong"
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    # DB migrate
    migrate = Migrate(app, db)

    # Bootstrap CSS Libraries
    Bootstrap(app)

    # Register Application Blueprints
    from app import models
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .portfolio import portfolio as portfolio_blueprint
    app.register_blueprint(portfolio_blueprint)


    # Define Customized Error Handlers 
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500


    
    # TODO: Fix this logging block / move settings to settings file
    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.INFO)  # DEBUG
    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)


    # Initialise Coin Data API Call Scheduler 
    # DO NOT move this import from here.
    from util_scripts.api_task_scheduler import schedule_api_tasks
    @app.before_first_request
    def initialize():
        schedule_api_tasks(app)


    return app
