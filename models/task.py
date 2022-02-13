from .db import db


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    note = db.Column(db.String())
    done = db.Column(db.Boolean(), default=False)
