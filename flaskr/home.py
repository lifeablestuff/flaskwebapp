import functools

from flaskr.dbmodel import db, User, ConferenceSlot, Booking
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/', methods=('GET', 'POST'))
def home():
    
    print(request.headers)
    print(request.data)  # Print raw body for debugging


    return render_template('home/home.html')