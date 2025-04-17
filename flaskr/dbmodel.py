from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(225), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'parent' or 'teacher'

    def __repr__(self):
        return f'<User {self.username}>'


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    # Define relationships (specify foreign_keys so it doesn't get confused)
    parent = db.relationship('User', foreign_keys=[parent_id], backref='parent_bookings')
    teacher = db.relationship('User', foreign_keys=[teacher_id], backref='teacher_bookings')
