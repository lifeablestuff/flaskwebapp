import functools
import html #for xss prevention
import sqlite3

from flask import Flask, make_response
import os
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

from werkzeug.security import check_password_hash, generate_password_hash

# from flaskr.db import get_db

#start of my spaghetti code



bp = Blueprint('auth', __name__, url_prefix='/auth')

DATABASE = './instance/db.sqlite3'



#stuff for database connection
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


def home():
    return render_template('home.html')



@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'GET':
        error = None
        return render_template('auth/register.html')
    if request.method == 'POST':
        print(session)
        try:

            if session['userid'] is not None:
                error = 'You are already logged in!'
                return redirect(url_for('home.home'))
        except KeyError:
            # Handle the case where 'userid' is not in session
            error = None
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        error = None

    if not username:
        error = 'Username is required.'
        flash(error)
    elif not password:
        error = 'Password is required.'
        flash(error)
    elif not email:
        error = 'Email is required.'
        flash(error)
    role = 'parent' #default user role
    db = get_db()
    if error is None:
        print('hopefully something happens after this')
        try:
            print('trying to execute sql command')
            db.execute(
                "INSERT INTO User (username, email, password_hash, role) VALUES (?,?,?,?)",
                (username, email, generate_password_hash(password),role)
            )
            db.commit()
            
            flash('You have successfully created an account!')
            print(f'added {username} to db')
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                error = 'Username has already been registered'
            elif 'email' in str(e):
                error = 'Email has already been registered'
            else:
                error = 'An unkown error has occured during registeration'
            flash(error)
            db.rollback() #rollback transaction    
        
        db.close()

    else:
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = html.escape(request.form.get('username', '').strip())
        password = html.escape(request.form.get('password', '').strip())
        db = get_db()
        error = None
        if username is None:
            error = 'Please enter a username'
            flash(error)
        user = db.execute(
            'SELECT * FROM User WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'No username found'
            flash(error)
            return render_template('auth/login.html')
        if not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password.'
            flash(error)
            return render_template('auth/login.html')

        if error is None:
            session.clear()
            session['userid'] = user['id']
            session['role'] = user['role']
            return redirect(url_for('home.home'))

    
    if request.method == "GET":
        error = None

    flash(error)
    return render_template('auth/login.html')

@bp.route('/logout', methods=['POST','GET'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))



def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
