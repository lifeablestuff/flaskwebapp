from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from .db import db, init_app, close_connection, get_db

import click
from flask.cli import with_appcontext

def create_app(test_config=None):
    print("initalized")
    app = Flask(__name__, instance_relative_config=True)
    db_path = os.path.join(app.instance_path, 'app.db')
    app.secret_key = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    @click.command('init-db')
    @with_appcontext
    def init_db_command():
        """Clear the existing data and create new tables."""
        db.drop_all()
        db.create_all()
        print(db_path)
        click.echo('Initialized the database.')
    
    app.cli.add_command(init_db_command)
    
    @app.before_request
    def load_db():
        get_db()
    
    @app.teardown_appcontext
    def teardown_db(exception):
        close_connection(exception)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)


    #ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import home
    app.register_blueprint(home.bp)
    
    
    #IMPORTANT ------ CHANGE booking.py AND home.py, MODIFY TO USE SCHEMA
    #from . import booking
    #app.register_blueprint(booking.bp)

    #from . import home
    #app.register_blueprint(home.bp)
    
    return app