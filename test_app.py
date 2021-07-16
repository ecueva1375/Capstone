import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

# Tokens
casting_assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRobTNpaU95V05zaVRzbWV1R2Z1ZCJ9.eyJpc3MiOiJodHRwczovL2VjZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlOTFkOTY1MzA4MDkwMDY4MDAwNzY0IiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTYyNjQ2OTIxNCwiZXhwIjoxNjI2NTU1NjE0LCJhenAiOiJ4RHJFUkJIVWpBM25Pb3RZQ3FxQ1Q0cDhlQ3pNTnluMSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.Sf527oARtSBcdN2NpTScVs7xr-DRctozbrmWLOnXx4DVpyIJfzYsZx0f1v0nWAH2fD7E6JNf3COFS3acRO4tYvWNNCkuBAtazXQcHTzgYrBmAVKvb4blTaztJiCX1ZogOPcuS60CyQ1TVVsLTMY9LgyMgOJg8I94-PTwtoah8FV3XtG0SXeof9nE7QHfMt5u--Uw94bSfCxXsarVMxQYPJzZU7o6TxMHlx6II30TjqhKEdQkzJ8TjwQdk48Zy5b4BY7Gaz-7cFBbGTS_rxKnAHYjAZ2_nd7ERPTHDx_p8NF0ug2or0PEzs_lrbbGkozEg9VPtuQPCmpUjNq4sEvYVg'
casting_director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRobTNpaU95V05zaVRzbWV1R2Z1ZCJ9.eyJpc3MiOiJodHRwczovL2VjZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBkMDAwODU3NjQ0YzAwMDY4MjBkNTQzIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTYyNjQ2OTM1NSwiZXhwIjoxNjI2NTU1NzU1LCJhenAiOiJ4RHJFUkJIVWpBM25Pb3RZQ3FxQ1Q0cDhlQ3pNTnluMSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.dmqG0ml1oKkAKAkiuviW-FhemW4CQF-La65YJwEnu0g1-vnmD9uyBz__hsY8Xmbgn7hLkoD4JEPM8nfYejXkITm5_48Tl-FI0m7KHGE4xWkPlkzo-zcFQp5FTPtyTL6Fa_3uqIab9M0pb4qnS5qWZ4rBe1b529S2tx_ioomRu2wxCxvlxzhkpzk0i-6mcmt94k2mAphv33gkbHqpq1rNV5yg_ShyU5e1ccYQEAg7cs_KjNfZjmFc26KZh3JiFULYfdvAX5hHevlLqTFxV7GfXNOQiydSv9bfxTuldNQ_3avTwtGL46Ju9ZZKlVnhLW75b04VP67vSYyRrbfAGQCDsg'
executive_producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRobTNpaU95V05zaVRzbWV1R2Z1ZCJ9.eyJpc3MiOiJodHRwczovL2VjZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBjNTdjZTRlZDZmY2IwMDY5NDhkODliIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTYyNjQ2OTQ0NywiZXhwIjoxNjI2NTU1ODQ3LCJhenAiOiJ4RHJFUkJIVWpBM25Pb3RZQ3FxQ1Q0cDhlQ3pNTnluMSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.ffxHsq8O5vt7dGBkTfxc9ocYo4ExeLMdyaZyu8WDLE6fNC1Mj7eEobfKnkkDrFcn0ir67RvWrf1jAC6DFzXSxQIz19WauRp8ZiETUKbh6MsnaKnjwBsIi8wKkxWds5nYk59u4lAcq9HBZg9BiWKJBTqO1mW_bY2BEvtzTIFBMrFNUJSbhGQc6vd1-BQF6wCNQm0itsEZ1itro1THpmI-gLemvTC9i4jKBChJWMEqPJ-1e1myX4If7k7aosMXh1ybPxu8Cblj3pv_mvUbi2lRXYSFsCdvLdo5zA-ySKHeVXoMMePZmheVb-KatfU9G5696obol_cC9_LWV_puuwlJlQ'


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
