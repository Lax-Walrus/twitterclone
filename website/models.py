from sqlalchemy import PrimaryKeyConstraint
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# user model usermixen creates an is authenticated boolean and login method to handle login and logout easier


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    isAdmin = db.Column(db.Boolean, default=False)
    chirps = db.relationship("Chirps", backref="user", passive_deletes=True)
    comment = db.relationship("Comment", backref="user", passive_deletes=True)
    like = db.relationship("Like", backref="user", passive_deletes=True)

# Chirp/Post model


class Chirps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)

    comment = db.relationship(
        "Comment", backref="chirps", cascade="all,delete-orphan")
    like = db.relationship(
        "Like", backref="chirps", cascade="all,delete-orphan")


# comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)

    chirp_id = db.Column(db.Integer, db.ForeignKey(
        'chirps.id',  ondelete="CASCADE"), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    chirp_id = db.Column(db.Integer, db.ForeignKey(
        'chirps.id',  ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
