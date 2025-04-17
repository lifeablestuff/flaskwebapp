from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, g, current_app
import sqlite3
import os

# Initialize SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()
app = Flask(__name__)





def init_app(app):
    """Initialize the database with the Flask app."""
    
    #db.init_app(app)
    migrate.init_app(app,db)
    print('asdf')
    Migrate(app, db)
    '''
    schema = 'schema.sql'
    print('fasd')
    # Create tables (only if they don't exist)
    with app.app_context():
        if os.path.exists(schema):
            conn = db.engine.raw_connection()
            try:
                cursor = conn.cursor()
                with open(schema, 'r') as f:
                    sql_script = f.read()
                cursor.executescript(sql_script)
                conn.commit()
            finally:
                cursor.close()
                conn.close()
        else:
            # if no schema
            db.create_all()
    '''
    

