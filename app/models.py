import datetime as dt

from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model, SerializerMixin):
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
    jobs            = db.relationship("Jobs", backref="team_lead")
    department      = db.relationship("Department", backref="chief_lead")

    def __repr__(self):
        return f"{self.name} {self.surname}"

    @staticmethod
    def get_by_email(email):
        return User.query.filter(User.email == email).first()

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Jobs(db.Model, SerializerMixin):
    __tablename__ = "jobs"

    id            = db.Column(db.Integer, primary_key=True)
    team_leader   = db.Column(db.Integer, db.ForeignKey("users.id"))
    job           = db.Column(db.String)
    work_size     = db.Column(db.Integer)
    collaborators = db.Column(db.String)
    start_date    = db.Column(db.DateTime)
    end_date      = db.Column(db.DateTime)
    is_finished   = db.Column(db.Boolean)
    category_id   = db.Column(db.Integer, db.ForeignKey("job_category.id"))
    


class JobCategory(db.Model, SerializerMixin):
    __tablename__ = "job_category"

    id   = db.Column(db.Integer, primary_key=True)
    jobs = db.relationship("Jobs", backref="category")


class Department(db.Model, SerializerMixin):
    __tablename__ = "departments"

    id      = db.Column(db.Integer, primary_key=True)
    title   = db.Column(db.String)
    chief   = db.Column(db.Integer, db.ForeignKey("users.id"))
    members = db.Column(db.String)
    email   = db.Column(db.String)
