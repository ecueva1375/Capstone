import os
from datetime import datetime
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from models import setup_db, Movie, Actor # se quita el punto 
from flask_cors import CORS 

from auth.auth import AuthError, requires_auth # se quita el punto

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,PATCH,DELETE,OPTIONS')
        return response

    @app.route('/actors')
    @requires_auth('get:actors')
    def retrieve_actors(payload):

        try:
            actors_q = Actor.query.all()

            actors = [actor.format_no_movies() for actor in actors_q]
            
            return jsonify({
                'success': True,
                'actors': actors
            }), 200

        except():
            abort(400)

    @app.route('/movies')
    @requires_auth('get:movies')
    def retrieve_movies(payload):

        try:
            movies_q = Movie.query.all()

            movies = [movie.format_no_actors() for movie in movies_q]            

            return jsonify({
                'success': True,
                'movies': movies
            }), 200

        except():
            abort(400)

    
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        
        try:
            body = request.get_json(force=True)            

            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)

            # ppp json.dumps() function converts a Python object
            # into a json string.
            actor_new = Actor(name=name, age=age, gender=gender)
            actor_new.insert()
            actor = [actor_new.format_no_movies()]

            return jsonify({
                'success': True,
                'actors': actor
            }), 200

        except():
            abort(400)

    
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):

        try:
            body = request.get_json(force=True)            

            title = body.get('title', None)
            release_date = body.get('release_date', None) 
            
            try:
                if release_date != datetime.strptime(release_date, "%d/%m/%Y").strftime('%d/%m/%Y'):
                    raise ValueError
            except ValueError:
                abort(422)

            
            release_date = datetime.strptime(release_date, '%d/%m/%Y').date()                 

            # ppp json.dumps() function converts a Python object
            # into a json string.
            movie_new = Movie(title=title, release_date=release_date)
            movie_new.insert()
            movie = [movie_new.format_no_actors()]

            return jsonify({
                'success': True,
                'movies': movie
            }), 200

        except():
            abort(400)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors') 
    def update_actor(payload, id):
        try:

            body = request.get_json(force=True)            

            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)          

            actor_upd = Actor.query.filter(Actor.id == id).one_or_none()

            if actor_upd is None:
                abort(404)

            actor_upd.name = name
            actor_upd.age = age
            actor_upd.gender = gender
            actor_upd.update()
            actor = actor_upd.format_no_movies()

            return jsonify({
                'success': True,
                'actors': actor
            }), 200

        except():
            abort(400)
  
  
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, id):
        try:

            body = request.get_json(force=True)            

            title = body.get('title', None)
            release_date = body.get('release_date', None)

            movie_upd = Movie.query.filter(Movie.id == id).one_or_none()

            if movie_upd is None:
                abort(404)

            try:
                if release_date != datetime.strptime(release_date, "%d/%m/%Y").strftime('%d/%m/%Y'):
                    raise ValueError
            except ValueError:
                abort(422)

            
            release_date = datetime.strptime(release_date, '%d/%m/%Y').date()

            movie_upd.title = title
            movie_upd.release_date = release_date          
            movie_upd.update()
            movie = movie_upd.format_no_actors()
            
            return jsonify({
                'success': True,
                'movies': movie
            }), 200

        except():
            abort(400)

  
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        try:

            actor_delete = Actor.query.filter(Actor.id == id).one_or_none()

            if actor_delete is None:
                abort(404)

            actor_delete.delete()

            return jsonify({
                'success': True,
                'delete': id
            }), 200

        except():
            abort(400)

  
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        try:

            movie_delete = Movie.query.filter(Movie.id == id).one_or_none()

            if movie_delete is None:
                abort(404)

            movie_delete.delete()

            return jsonify({
                'success': True,
                'delete': id
            }), 200

        except():
            abort(400)

  
    # Error Handling
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400


    @app.errorhandler(403)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden"
        }), 403


    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500


    # Receive the raised authorization error and propagates it as response
    @app.errorhandler(AuthError)
    def auth_error(ex):
        print(ex.error['code'], "is the code")
        return jsonify({
            "success": False,
            "error": ex.status_code,
            "message": ex.error['code']
        }),  ex.status_code


    return app

app = create_app()  

if __name__ == '__main__':   
    app.run(host='0.0.0.0', port=8080, debug=True)