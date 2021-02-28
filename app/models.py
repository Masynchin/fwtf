import datetime as dt

from app import db


class User(db.Model):
    __tablename__ = "users"

    id              = db.Column(db.Integer, primary_key=True)
    surname         = db.Column(db.String)
    name            = db.Column(db.String)
    age             = db.Column(db.Integer)
    position        = db.Column(db.String)
    speciality      = db.Column(db.String)
    address         = db.Column(db.String)
    email           = db.Column(db.String, unique=True)
    hashed_password = db.Column(db.String)
    modified_date   = db.Column(db.DateTime, default=dt.datetime.utcnow)
    jobs            = db.relationship("Jobs", backref="worker", lazy="dynamic")

    def __repr__(self):
        return f"{self.name} {self.surname}"


class Jobs(db.Model):
    __tablename__ = "jobs"

    id            = db.Column(db.Integer, primary_key=True)
    team_leader   = db.Column(db.Integer, db.ForeignKey("users.id"))
    job           = db.Column(db.String)
    work_size     = db.Column(db.Integer)
    collaborators = db.Column(db.String)
    start_date    = db.Column(db.DateTime)
    end_date      = db.Column(db.DateTime)
    is_finished   = db.Column(db.Boolean)


class Department(db.Model):
    __tablename__ = "departments"

    id      = db.Column(db.Integer, primary_key=True)
    title   = db.Column(db.String)
    chief   = db.Column(db.Integer, db.ForeignKey("users.id"))
    members = db.Column(db.String)
    email   = db.Column(db.String)
