from . import db



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(225), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # parent or teacher

    def __repr__(self):
        return f'<User {self.username}>'



class ConferenceSlot(db.Model):  # for the teacher
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    isbooked = db.Column(db.Boolean, nullable=False)

class Booking(db.Model):  # for the parent
    id = db.Column(db.Integer, primary_key=True)  # Add a primary key
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('conference_slot.id'), nullable=False)

