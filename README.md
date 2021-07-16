# Full Stack Capstone Project
 
## Full Stack Movie Casting Agency API

This is the Capstone Project for the Udacity Full Stack Web Developer Nanodegree Program. It's an api allowing a casting agency creating movies and managing and assigning actors to those movies and in this way the process is simplified and streamlined.

In this Capstone project, the concepts and skills learned in the course have been used to create and host an end-to-end API.

The api has been developed using modeling data objects with SQLAlchemy, to limit access authentication with Auth0 has been used for which roles 
and permissions were created for the different endpoints and finally the deployment was carried out using Heroku.

The skills learned in the program are summarized below:

- Coding in Python 3
- Relational Database Architecture
- Modeling Data Objects with SQLAlchemy
- Internet Protocols and Communication
- Developing a Flask API
- Authentication and Access
- Authentication with Auth0
- Authentication in Flask
- Role-Based Access Control (RBAC)
- Testing Flask Applications
- Deploying Applications


## Backend - Full Stack Movie Casting Agency API

### Installing Dependencies for the Backend

To access the api locally, you need a database, a virtual environment, dependencies installed, and environment variables set up. 
You also need an account with Auth0 and an authentication service.

1. This api runs on a PostgreSQL database. You can download PostgreSQL at [postgresql.org](https://www.postgresql.org/).

2. Python 3.7 - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

3. Virtual Enviornment - We recommend wo rking within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized.
```bash
$ cd project_directory_path/
```

**Create a virtual environment**
```bash
$ py -3 -m venv venv

# activate a virtual environment
source venv/Scripts/activate
```

4. PIP Dependencies - Once you have your virtual environment setup and running, install dependencies by running:
```bash
	pip install -r requirements.txt
```

### Database Setup

With Postgres running, create a database using the setup_database.sql file provided. On a terminal screen run:

**Create database:**
```bash
psql postgres postgres # connect to postgres as superuser to an already existing base
\l
\i '/starter/setup_database.sql' # path where the file is located
```

The api uses migrations, so for the creation of the tables we must run the following from the starter folder:
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

To populate the database we must run the following in a terminal:
```bash
psql -U postgres casting_agency < C:\ ..\ .. capstone\starter\capstone_data.psql  # path where the file is located
```

**Environment variables**

Load environment variables configured in setup.sh
```bash
source setup.sh
```

**Running the server**

From within the starter directory first ensure you are working using your created virtual environment.

To run the server, execute:
```bash
set FLASK_APP=app.py
flask run --reload
```

## API Reference

Getting Started

Base URL: At present this api can be run locally and hosted as a base URL. The api backend is hosted at the default http://127.0.0.1:5000/ and url of the hosted api is https://casting-agency-ec.herokuapp.com/

### Authentication

**Configuration in auth0:**

**Dominio:** ecfsnd.us.auth0.com

**App name:** CastingAgencyService

**Api name:** CastingAgency

The following roles and permissions were set:

**Roles**

**Name:** Casting Assistant

**Description:** Someone can view actors and movies

**Permisos:**

	get:actors
    
	get:movies	

**Name:** Casting Director
**Description:** 
	All permissions a Casting Assistant has and…
	Add or delete an actor from the database
	Modify actors or movies
**Permisos:**
	get:actors
	get:movies
	post:actors
	delete:actors
	patch:actors
	patch:movies	

**Name:** Executive Producer
**Description:** 
	All permissions a Casting Director has and…
	Add or delete a movie from the database
**Permisos:**
	get:actors
	get:movies
	post:actors
	delete:actors
	patch:actors
	patch:movies
	post:movies
	delete:movies
```

Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
```

The API will return six error types when requests fail and an Auth error if authentication fails:

400: Bad request
403: Forbidden
404: Resource not found
405: Method not allowed
422: Not processable
500: Internal server error
AuthError: Auth0 error status code and description

```
```
Endpoints

GET '/api/v1.0/actors'
GET '/api/v1.0/movies'
POST '/api/v1.0/actors'
POST '/api/v1.0/movies'
PATCH '/api/v1.0/actors/${id}'
PATCH '/api/v1.0/movies/${id}'
DELETE '/api/v1.0/actors/${id}'
DELETE '/api/v1.0/movies/${id}'


GET '/api/v1.0/actors'
- Fetches actores rows.
- Request Arguments: None
- Returns: An a message indicating if the request was successful and an object with all actor records.
 
{
  'success': True,
  'actors': [
        {           
            "id": 1,
            "name": "Nisa Sofiya Aksongur",
	    "age": "9",
            "gender": "Female"
        },
]
}


GET '/api/v1.0/movies'
- Fetches movies rows.
- Request Arguments: None
- Returns: An a message indicating if the request was successful and an object with all movie records.
 
{
  'success': True,
  'movies': [
        {
            "id": 1,
	    "title": "Miracle in cell 7",
            "release_date": "Tue, 08 Oct 2019 00:00:00 GMT"            
        },
]
}


POST '/api/v1.0/actors'
- Sends a post request in order to add a new actor
- Request Body: 
{
    "name": "Jacob Tremblay",
    "age": "14",
    "gender": "Male"
}
- Returns: A message indicating if the creation was successful or not and single new actor object 
{
    'success': True,
    'actors': {
	    'id': 7,
	    'name': 'Jacob Tremblay',
            'age': '14',
            'gender': 'Male'              
           }    
}


POST '/api/v1.0/movies'
- Sends a post request in order to add a new movie
- Request Body: 
{
    'title': 'Wonder',
    'release_date': '14/11/2017'
}
- Returns: A message indicating if the creation was successful or not and single new movie object 
{
    'success': True,
    'movies': {
        'id': 10,
	'title': 'Wonder',
        'release_date': 'Tue, 14 Nov 2017 00:00:00 GMT'        
    }    
}


PATCH '/api/v1.0/actors/${id}'
- Sends a patch request in order to update a actor using the id of the actor
- Request Arguments: id - integer
- Request Body:
{
    'name': 'Jacob Tremblay',
    'age': '15',
    'gender': 'Male'
}
- Returns: A message indicating if the creation was successful or not and single updated actor object 
{
    'success': True,
    'actors': {
	    'id': 7,
	    'name': 'Jacob Tremblay',
            'age': '15',
            'gender': 'Male'              
           }    
}


PATCH '/api/v1.0/movies/${id}'
- Sends a patch request in order to update a movie using the id of the movie
- Request Arguments: id - integer
- Request Body:
{
    'title': 'Wonder',
    'release_date': '15/11/2017'
}
- Returns: A message indicating if the creation was successful or not and single updated movie object 
{
    'success': True,
    'actors': {
        'id': 10,
	'title': 'Wonder',
        'release_date': 'Wed, 15 Nov 2017 00:00:00 GMT'        
    }    
}


DELETE '/api/v1.0/actors/${id}'
- Deletes a specified actor using the id of the actor
- Request Arguments: id - integer
- Returns: a message indicating if the actor could be deleted successfully and id of deleted actor, if not the corresponding HTTP code message.
{
     'success': True,
     'delete': id
}


DELETE '/api/v1.0/movies/${id}'
- Deletes a specified movie using the id of the movie
- Request Arguments: id - integer
- Returns: a message indicating if the movie could be deleted successfully and id of deleted movie, if not the corresponding HTTP code message.
{
     'success': True,
     'delete': id
}

```

## Testing
To run the tests, run on a terminal screen
```
psql postgres postgres
dropdb casting_agency_test
createdb casting_agency_test
\q
```

### Create the tables and insert data.
```
psql -U postgres casting_agency_test < C:\ ..\ capstone\starter\capstone_data_test.psql 
# Run the test
python test_app.py

Tests include:
- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- Two tests of RBAC for each role.


```

## Deploying and Hosting Full Stack Movie Casting Agency API

**Getting Started on Heroku**
1. Create an account on Heroku 
	https://signup.heroku.com/

2. Download the Heroku CLI (Command Line Interface) in order to run commands from the terminal that enable us to create a Heroku application and manage it.
	https://devcenter.heroku.com/categories/command-line


**Deployment Configuration**
1. Update requirements file
    ```
	pip freeze > requirements.txt
    ```
2. All environment variables of the api must be configured in setup.sh, including authentication.

3. Install gunicorn
    ```
	pip install gunicorn
    ```

4. Create the file Procfile. This file contains the following line:
    ```
	web: gunicorn app:app
    ```


**Deploy and Test**

1. Create Heroku app
    ```
 	heroku create casting-agency-ec --buildpack heroku/python
    ```

2. Add git remote for Heroku to local repository
    ```
	git remote add casting https://git.heroku.com/casting-agency-ec.git
    ```

3. Add postgresql add on for our database
    ```
	heroku addons:create heroku-postgresql:hobby-dev --app casting-agency-ec
    ```

4. Check your configuration variables in Heroku
    ```
	heroku config --app casting-agency-ec
    ```

5. Fix the settings on Heroku
In the browser, the Heroku Panel accesses the application settings. We revealed the config variables and all the required environment variables for the project were added.

6. Push it
    ```
	git push casting main
    ```

7. Run migrations
Once the app is deployed, run migrations by running:
    ```
	heroku run python manage.py db upgrade --app casting-agency-ec
    ```

8. Access to the api hosted from [Postman](https://getpostman.com).
- Import the postman collection starter/Casting_agency_collection_postman.postman_collection.json.
- Run each of the collection requests.



	


