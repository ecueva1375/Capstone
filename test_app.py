import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

# Tokens
casting_assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRobTNpaU95V05zaVRzbWV1R2Z1ZCJ9.eyJpc3MiOiJodHRwczovL2VjZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlOTFkOTY1MzA4MDkwMDY4MDAwNzY0IiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTYyNjg4NDIwMywiZXhwIjoxNjI2OTcwNjAzLCJhenAiOiJ4RHJFUkJIVWpBM25Pb3RZQ3FxQ1Q0cDhlQ3pNTnluMSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.jym0VN5aLbNNA2Zy2Hg7M-muUAgTLIdPlXPlFEAxB19Glfma9PQXk0l9Ogm4XDkiwWLIeBjajh0vTJ8JteVkhlZuWUZvHQm15vNeu0mCymaWexOqbAalZ4IffQrrmy28-L5UxgxuT5rErEJLVAKk1zTEQSvXeLYsg_YcDbhs_L2FayIsgWoXcfG9_eTnNZSHGvvH5dwzVPifX1429-4LAnq1r5zoiC9ebVB8dbHu-RK-fA6fTLGoAEQWlZSGf1kvTl3HdQcG7DI4wRCIyuFJSJoPEyX3B6gOtBwIgNpyzpeQ4K44V_6wO3_t92J82gyVUN-2-onqz5amFtymq9qokw'
casting_director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRobTNpaU95V05zaVRzbWV1R2Z1ZCJ9.eyJpc3MiOiJodHRwczovL2VjZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBkMDAwODU3NjQ0YzAwMDY4MjBkNTQzIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTYyNjg4NDI2NywiZXhwIjoxNjI2OTcwNjY3LCJhenAiOiJ4RHJFUkJIVWpBM25Pb3RZQ3FxQ1Q0cDhlQ3pNTnluMSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.krA2rv38ERY4UCInyo_TO-JXO2yaFYxoGQdKpB0eUqtBXDr05c9Wt6V6Egunjuze0Bwj-Kft-aJ2chw-okP-Ui2hKV69wrqypxjimAH5zfgpcgzFxKu_HoselLvF4cj9Sfts0EXsxicgo3y-ck41bfVBN2eV9t9l1SQlXH8PDUEJP6aDa-CrzyFfSThMzjAwI2Cnd50PGlOdGfGypqC20TH3s7-2Ru-kOGANNUAHHBagD5T7zRYj2m8rvYxQZgDC0QrhVBwPG0Me1FwT1TEO_hmEjMoAk6icaaBTGxs3PaxxN1Dm-nq2hwGxd6NJaHiz3G-Jap2qbEZvZ95WTnY-Gg'
executive_producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRobTNpaU95V05zaVRzbWV1R2Z1ZCJ9.eyJpc3MiOiJodHRwczovL2VjZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBjNTdjZTRlZDZmY2IwMDY5NDhkODliIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTYyNjg4NDMzOSwiZXhwIjoxNjI2OTcwNzM5LCJhenAiOiJ4RHJFUkJIVWpBM25Pb3RZQ3FxQ1Q0cDhlQ3pNTnluMSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.iaFjn0cBZM-eMgR0HdPyrHTGOgSVuLrFH9pJnZnSNeL-MOluDM-aJ022zc-9ZzLPtIhGIwZw4otp2Z2adlScr_VP0e6P2L1KOXKmc5sxSrrd-rWYTPzJtQ48l07ibKTffmHrkWkWpu6bA71OgZKqRtINyZjtGjzNRH9hsuApktLbhYjnN0MBqdVUM_1GdsY3Az6wpe6cRdTiCe-kQ4PM_LEM7yXwySa-liV_JC0Pb9UUjyGzIjU1ZdzC_X-FInbH3dlHCZ1_90ZacCAGa8OsRJnRzVpezx4ZAZRd2NakLZ6A1RxO6YJUhNne595lMaF58gFGPfngVf2ZHtbu0jqaxQ'


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres',
            'alexandra1375',
            'localhost:5432',
            self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_movie = {
            'title': 'Wonder',
            'release_date': '14/11/2017'
        }

        self.new_actor = {
            'name': 'Jacob Tremblay',
            'age': '14',
            'gender': 'Male'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test for each endpoint, one test for each test for
    # successful operation and for expected errors.
    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_404_movies_method_not_allowed(self):
        res = self.client().get('/movies/100', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_405_actors_method_not_allowed(self):
        res = self.client().get('/actors/200', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_if_movie_creation_not_allowed(self):
        res = self.client().post('/movies/200', json=self.new_movie, headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_if_actor_creation_not_allowed(self):
        res = self.client().post('/actors/200', json=self.new_actor, headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_update_movie(self):
        res = self.client().patch(
            '/movies/1',
            json={
                'title': 'Miracle in cell 7',
                'release_date': '16/10/2019'}, headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # number of items that correspond to a movie
        # without actors.
        movie = data['movies']
        self.assertEqual(len(movie), 3)

    def test_404_update_if_movie_does_not_exist(self):
        res = self.client().patch(
            '/movies/1000',
            json={
                'title': 'Hidden Figures',
                'release_date': '06/01/2017'}, headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_actor(self):
        res = self.client().patch(
            '/actors/1',
            json={
                'name': 'Nisa Sofiya Aksongur',
                'age': '10',
                'gender': 'Female'}, headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # number of items that correspond to a actor
        # without movies.
        self.assertEqual(len(data['actors']), 4)

    def test_404_update_if_actor_does_not_exist(self):
        res = self.client().patch(
            '/actors/1000',
            json={
                'name': 'Liam Neeson',
                'age': '69',
                'gender': 'Male'}, headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Delete a different movie in each attempt
    def test_delete_movie(self):
        res = self.client().delete('/movies/2', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie, None)

    def test_404_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1000', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Delete a different actor in each attempt
    def test_delete_actor(self):
        res = self.client().delete('/actors/2', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor, None)

    def test_404_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/1000', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # RBAC test demonstrating casting assistant can get all movies
    def test_get_movies_by_casting_assistant(self):
        res = self.client().get('/movies', headers={'Authorization': 'Bearer ' + casting_assistant})
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # RBAC test demonstrating casting assistant can get all actors
    def test_get_actors_by_casting_assistant(self):
        res = self.client().get(
            '/actors', headers={'Authorization': 'Bearer ' + casting_assistant})
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # RBAC test demonstrating casting director can create a actor
    def test_create_actor_by_casting_director(self):

        new_actor = {
                'name': 'Harrison Ford',
                'age': '78',
                'gender': 'Male'
                }

        res = self.client().post(
            '/actors',
            json=new_actor,
            headers={'Authorization': 'Bearer ' + casting_director}
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # RBAC test demonstrating casting director can delete a actor
    def test_delete_actor_by_casting_director(self):
        res = self.client().delete(
            '/actors/3',
            headers={'Authorization': 'Bearer ' + casting_director}
        )
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor, None)

    # RBAC test demonstrating executive producer can create a movie
    def test_create_movie_by_exec_producer(self):

        new_movie = {
            'title': 'Maléfica',
            'release_date': '28/05/2014'
            }

        res = self.client().post(
            '/movies',
            json=new_movie,
            headers={'Authorization': 'Bearer ' + executive_producer}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # RBAC test demonstrating executive producer can create an actor
    def test_create_actor_by_exec_producer(self):

        new_actor = {
                'name': 'Angelina Jolie',
                'age': '46',
                'gender': 'Female'
                }

        res = self.client().post(
            '/actors',
            json=new_actor,
            headers={'Authorization': 'Bearer ' + executive_producer}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
