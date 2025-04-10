import functools

import sqlite3

from flask import Flask, make_response

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

#start of my spaghetti code



bp = Blueprint('auth', __name__, url_prefix='/auth')

DATABASE = './instance/db.sqlite3'






def connect_db():
    return sqlite3.connect(current_app.config['DATABASE'])


def home():
    return render_template('home.html')



@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'GET':
        error = None
        return render_template('auth/register.html')
    if request.method == 'POST':
        print(session)
        if session is not None:
            return redirect(url_for('home.home'))
                
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
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM User WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Please enter a username'
            return render_template('auth/login.html')
        if not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password.'
            flash(error)
            return render_template('auth/login.html')

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('home.home'))

    
    if request.method == "GET":
        error = None

    flash(error)
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
