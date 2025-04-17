from flask import Flask, session, g, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from .db import db # init_app, close_connection, get_db
from werkzeug.security import check_password_hash, generate_password_hash
import click
from flask.cli import with_appcontext, AppGroup
import sqlite3

#ignore
'''
import sentry_sdk

sentry_sdk.init(
    dsn="https://65447ba865a89a3593c17bc15a5d220c@o4509166047526912.ingest.us.sentry.io/4509166050607104",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profile_session_sample_rate to 1.0 to profile 100%
    # of profile sessions.
    profile_session_sample_rate=1.0,
    # Set profile_lifecycle to "trace" to automatically
    # run the profiler on when there is an active transaction
    profile_lifecycle="trace",
)
'''

app = Flask(__name__)

def create_app(test_config=None):
    print("initalized")

    #factory
    app = Flask(__name__, instance_relative_config=True)
    user_cli = AppGroup('users', help='User management commands.')
    db_path = os.path.join(app.instance_path, 'app.db')
    app.secret_key = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #initalizes the db based on dbmodel.py
    @click.command('init-db')
    @with_appcontext
    def init_db_command():
        """Clear the existing data and create new tables."""
        db.drop_all()
        db.create_all()
        print(db_path)
        click.echo('Initialized the database.')
    #IGNORE THIS, CONNECTING TO DB
    def get_db():
        if 'db' not in g:
            g.db = connect_db()
        return g.db

    def connect_db():
        db_path = os.path.join(current_app.instance_path, 'app.db')
        print(f"path: {db_path}")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    app.cli.add_command(init_db_command)

    #ALL THINGS USER

    #help
    @user_cli.command('help')
    def help_user():
        """Display help information for user commands."""
        click.echo('User management commands:')
        click.echo('  create <username> <email> <generate_password (y/n)> <role (teacher/parent)>')
        click.echo('  delete <username>')
        click.echo('  help')
    app.cli.add_command(user_cli)

    #create user
    @user_cli.command('create')
    @click.argument('username')
    @click.argument('email')
    @click.argument('generate_password')
    @click.argument('role')
    @with_appcontext
    def create_user(username,email,generate_password,role):
        """Create a new user."""
        db = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        if not email:
            error = 'Email is required.'
        if not role:
            error = 'Role is required, please specify teacher or parent.'
        elif role not in ['teacher', 'parent']:
            error = 'Role must be either teacher or parent.'
        if not generate_password:
            error = 'Please specify if you want to autogenerate a password.'
        elif generate_password.lower() == 'y':
            generate_password = username + '1234'
        elif generate_password.lower() == 'n':
            generate_password = input('Enter password: ')
        else:
            error = 'Please specify if you want to autogenerate a password, y or n'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                    (username, email, generate_password_hash(generate_password), role)
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} or {email} is already registered."
            else:
                click.echo(f'Created user {username} with role {role}.')
                click.echo(f'Your password is {generate_password}.')
        else:
            click.echo(error)
    app.cli.add_command(user_cli)
    
    #remove user
    @user_cli.command('delete')
    @click.argument('username')
    @with_appcontext
    def delete_user(username):
        if not username:
            click.echo('Username is required.')
            return
        else:
            db = get_db()
            query = db.execute(
                "DELETE FROM user WHERE username = ?",
                (username,)
            )
            if query is None:
                click.echo(f'User {username} does not exist.')
                return

            else:
                db.commit()
                click.echo(f'Deleted user {username}.')
    app.cli.add_command(user_cli)



    '''
    @app.before_request
    def load_db():
        get_db()
    
    @app.teardown_appcontext
    def teardown_db(exception):
        close_connection(exception)
    '''
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