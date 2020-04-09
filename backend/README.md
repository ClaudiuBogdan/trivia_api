# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup

Copy .env.example to .env and add values to the vars:
*SQL_USER=caryn
*SQL_PASSWORD=password
*SQL_DATABASE=udacity_trivia


With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Testing
To run the tests:
Add database config values to .env vars: 
*TEST_SQL_USER=caryn
*TEST_SQL_PASSWORD=password
*TEST_SQL_DATABASE=udacity_trivia_test

Run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 


### Endpoints 
#### GET /categories
- General:
    - Returns a payload with a list of categories objects, success value, and response message
- Sample: `curl http://127.0.0.1:5000/categories`

``` 
{
  "error": null, 
  "message": "Get categories successfully.", 
  "payload": {
    "categories": [
      {
        "id": 1, 
        "type": "Science"
      }, 
      {
        "id": 2, 
        "type": "Art"
      }, 
      {
        "id": 3, 
        "type": "Geography"
      }, 
      {
        "id": 4, 
        "type": "History"
      }, 
      {
        "id": 5, 
        "type": "Entertainment"
      }, 
      {
        "id": 6, 
        "type": "Sports"
      }
    ]
  }, 
  "success": true
}
```

#### GET /questions
- General:
    - Returns a payload with a list of questions and categories objects, success value, and response message
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions?page=1`

``` 
{
  "error": null, 
  "message": "Get questions successfully.", 
  "payload": {
    "categories": [
      {
        "id": 4, 
        "type": "History"
      }, 
      {
        "id": 5, 
        "type": "Entertainment"
      }, 
      {
        "id": 6, 
        "type": "Sports"
      }, 
      {
        "id": 3, 
        "type": "Geography"
      }, 
      {
        "id": 2, 
        "type": "Art"
      }
    ], 
    "current_category": {
      "id": 4, 
      "type": "History"
    }, 
    "limit": 10, 
    "page": 1, 
    "questions": [
      {
        "answer": "Muhammad Ali", 
        "category": 4, 
        "difficulty": 1, 
        "id": 9, 
        "question": "What boxer's original name is Cassius Clay?"
      }, 
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
      {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }, 
      {
        "answer": "Brazil", 
        "category": 6, 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      }, 
      {
        "answer": "George Washington Carver", 
        "category": 4, 
        "difficulty": 2, 
        "id": 12, 
        "question": "Who invented Peanut Butter?"
      }, 
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
        "answer": "Escher", 
        "category": 2, 
        "difficulty": 1, 
        "id": 16, 
        "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
      }, 
      {
        "answer": "Mona Lisa", 
        "category": 2, 
        "difficulty": 3, 
        "id": 17, 
        "question": "La Giaconda is better known as what?"
      }
    ], 
    "total": 17
  }, 
  "success": true
}
```

#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the deleted question, success value and response message.
- `curl -X DELETE http://127.0.0.1:5000/questions/16`
```
{
   "error":"None",
   "message":"Delete question successfully.",
   "payload":{
      "question":{
         "answer":"The Liver",
         "category":1,
         "difficulty":4,
         "id":20,
         "question":"What is the heaviest organ in the human body?"
      }
   },
   "success":True
}
```

#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, category and difficulty. Returns the id of the created question, success value and response message. 
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is E = m * c * c", "question":"Enstein energy-mass formula", "category":1, difficulty: 5}'`
```
{
   "error":"None",
   "message":"Create question successfully.",
   "payload":{
      "question":{
         "answer":"Enstein energy-mass formula",
         "category":1,
         "difficulty":5,
         "id":134,
         "question":"What is E = m * c * c"
      }
   },
   "success":True
}
```

#### POST /questions/search
- General:
    - Search question by question text. Returns a list of all matching questions (case insensitive) 
- `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"search_term":"title"}'`
```
{
   "error":"None",
   "message":"Search question successfully.",
   "payload":{
      "categories":[
         {
            "id":5,
            "type":"Entertainment"
         }
      ],
      "current_category":{
         "id":5,
         "type":"Entertainment"
      },
      "questions":[
         {
            "answer":"Edward Scissorhands",
            "category":5,
            "difficulty":3,
            "id":6,
            "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
         }
      ],
      "total_questions":1
   },
   "success":True
}
```

#### GET /categories/category_id/questions
- General:
    - Returns a payload with a list of questions by category id, success value, and response message
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

``` 
{
   "error":"None",
   "message":"Get questions by category successfully.",
   "payload":{
      "current_category":1,
      "questions":[
         {
            "answer":"Apollo 13",
            "category":5,
            "difficulty":4,
            "id":2,
            "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
         },
         {
            "answer":"Tom Cruise",
            "category":5,
            "difficulty":4,
            "id":4,
            "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
         },
         {
            "answer":"Edward Scissorhands",
            "category":5,
            "difficulty":3,
            "id":6,
            "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
         }
      ],
      "total_questions":3
   },
   "success":True
}
```

#### POST /quizzes
- General:
    -  POST endpoint to get questions to play the quiz. 
    This endpoint takes category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":2, "previous_questions": [16, 17, 18]}'`
```
{
   "error":"None",
   "message":"Start trivia successfully.",
   "payload":{
      "question":{
         "answer":"Jackson Pollock",
         "category":2,
         "difficulty":2,
         "id":19,
         "question":"Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
      }
   },
   "success":True
}
```