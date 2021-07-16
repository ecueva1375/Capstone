import datetime
from sqlalchemy import (
    Column,
    String,
    create_engine,
    Integer,
    ForeignKey,
    Date)
from flask_sqlalchemy import SQLAlchemy
import json
import os
from sqlalchemy.sql import func

# This line is uncommented when the app is being tested locally
database_path = os.environ['DATABASE_URL']
# This line is used when the app is deployed in heroku.
#database_path = os.environ['DATABASE_URL'].replace("://", "ql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


class Movie_actor(db.Model):
    __tablename__ = 'movies_actors'

    id = Column(Integer, primary_key=True)
    movie_id = Column(
        Integer, ForeignKey('movies.id'), nullable=False)
    actor_id = Column(
        Integer, ForeignKey('actors.id'), nullable=False)

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def format(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id}


'''
Movie:
  attributes: title and release date
'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date, default=datetime.date)

    movies_actors = db.relationship('Movie_actor', backref='movie',
                                    lazy=True, cascade="all, delete-orphan")

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [actor.format() for actor in self.movies_actors]
            }

    def format_no_actors(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
            }


'''
Actor:
  attributes: name, age and gender
'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(String)
    gender = Column(String)

    movies_actors = db.relationship('Movie_actor', backref='actor',
                                    lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.format() for movie in self.movies_actors]
            }

    def format_no_movies(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
            }
