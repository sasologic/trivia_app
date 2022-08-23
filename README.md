# FULLSTACK TRIVIA API

The TRIVIA API aims at creating seamless bonding experiences between Udacity students and employees by giving them opportunities to expose their wealth of knowledge playing the TRIVIA quiz. At the end of the each game, the most knowledgeable of the bunch is recognized. 

## API DESCRIPTION

The application does the following: -

1.  Display questions - both all questions and by category. Questions show the question, category and difficulty   rating and toggles the answer.
2.  Deletes question by its Id.
3.  Adds questions including question and answer text.
4.  Searches for questions based on case-insensitive partial text query string.
5.  Plays the quiz randomnizing questions in a specified category.

## LOCAL BACKEND REQUIREMENTS
This app requires Python 3.7 or later

### Python 3.7
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

### Virtual Environment 
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


### PIP Dependencies
Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash or powershell
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash or powershell
CREATE DATABASE trivia;
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:


```bash or powershell
psql -h localhost -U postgres -d trivia -f trivia.psql
```

### Run the Server

From within the `./backend` directory first ensure you are working using your created virtual environment.

Set local environment variables by issuing the commands:
```powershell
$env:FLASK_APP='flaskr'
$env:FLASK_ENV='development'
```

```bash
export FLASK_APP='flaskr'
export FLASK_ENV='development'
```

To run the server, execute:

```bash or powershell
py -m flask run
```

Tbe FLASK_APP variable detects the __init__.py  in the 'flaskr' directory for the server to run successfully. The FLASK_ENV to 'development' variable will detect file changes and restart the server automatically.

## TRIVIA API FRONTEND REQUIREMENTS

## Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected. We recommend that you **stand up the backend first**, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash or powershell
npm install
```

> _tip_: `npm i`is shorthand for `npm install``

## Required Tasks

### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash or powershell
npm start
```

## API REFERENCE

### Endpoints


`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
Example: curl 127.0.0.1:5000/categories

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success":true
}
```

---

`GET '/categories/<int:category_id>/questions'`

- Fetches questions for a cateogry specified by category_id request argument
- Request Arguments: `category_id` - integer
- Returns: An object with questions for the specified category, total questions for that category, and current category string
Example: curl 127.0.0.1:5000/categories/questions/3
"current_category": 3,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 3
}


`GET '/questions?page=<int>'`

- Fetches a paginated set of questions, a total number of questions and all categories.
- Request Arguments: `page` - integer which is optional
- Returns: An object with 10 paginated questions, total questions, and object including all categories

Example:  curl 127.0.0.1:5000/questions


  {
    "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    ... too long to be displayed
  ],
  "success": true,
  "total_questions": 10
}


```
```

`DELETE '/questions/<int:question_id>'`

- Deletes a specified question using the id of the question
- Request Arguments: `question_id` - integer
- Returns 200 status code if successfully deleted
- Returns paginated `questions` and length of `total_questions`
- Returns 404 if questions was not found in the database
Example: curl -X DELETE 127.0.0.1:5000/questions/5

 "deleted": 5,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    --- remaining questions too long to be displayed
    ],
  "success": true,
  "total_questions": 10
}



---

`POST '/quizzes'`

- Sends a post request in order to get the next random question based on a question category
- Returns a new random question object
- Request Body:
Example: curl 127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"id":1,"type":"Science"}}'


 "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true
}


`POST '/questions'`

- Sends a POST request in order to add a new `question`
- Returns 200 status code if requst is successful
- Returns 404 status code if there is no request body
- Returns success value, id of newly created question, questions and length of total questions in quiz if successful

Example:  curl 127.0.0.1:5000/questions -X POST -H 'Content-Type:application/json' -d '{"question":"What is the capital of Federal Repblic of Nigeria?","answer":"Abuja", "category":"4", "difficulty":"3"}'


"created": 37,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    --- to long to be displayed
  ],
  "success": true,
  "total_questions": 32
}



`POST '/questions/search'`

- Sends a post request in order to search for a specific question by search term
- Request Body: JSON object from any supported client
- Returns 404 status code if there are no questions that meets the search criteria
- Returns `success` value, paginated `current_questions` that meets the search criteria and `total_questions` in quiz
Example: curl  curl 127.0.0.1:5000/questions/search -X POST -H 'Content-Type:application/json' -d '{"searchTerm":"Nigeria"}'

  "questions": [
    {
      "answer": "Muhammadu Buhari",
      "category": 2,
      "difficulty": 3,
      "id": 26,
      "question": "Who is the current president of the Federal Republic of Nigeria?"
    },
    {
      "answer": "1960",
      "category": 4,
      "difficulty": 3,
      "id": 27,
      "question": "In what year did Nigeria got her independence"
    },
    {
      "answer": "Abuja",
      "category": 4,
      "difficulty": 3,
      "id": 37,
      "question": "What is the capital of Federal Repblic of Nigeria?"
    }
  ],
  "success": true,
  "total_questions": 32
}


## ERROR HANDLERS

A JSON response is returned when an error occurs.  The app handles the following error types:
1.  404: Resource not found
2.  405: Method not allowed
3.  422: Unprocessable Entity

#### Error Example
##### 405 
{
  'success': False,
  'error': 405,
  'message': 'method not allowed'
}

## Testing

To deploy the tests, run

```bash or powershell
DROP DATABASE IF EXISTS trivia_test;
CREATE DATABASE trivia_test;
psql -h localhost -U postgres -d trivia_test -f trivia.psql
python test_flaskr.py
```