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

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Endpoints 
### GET '/categories'
`http://127.0.0.1:5000/categories`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.

- Request Arguments: None

- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
```
{
'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"
}  
```

<hr>
  

### GET '/questions'

`http://127.0.0.1:5000/questions`


- Fetches a dictionary of questions in which the keys are the ids and the value is the corresponding string of the question.

- Request Arguments: accept  a page argument , defualt is 1 `http://127.0.0.1:5000/questions?page=2`

- Returns: Return a json object containg a categories dictionary, questions array, a current category array which  is ordred to match the questions array and a success value.
note that the questions are paginated by 10.

 ```
{
"categories": {
"1": "Science",
"2": "Art",
"3": "Geography",
"4": "History",
"5": "Entertainment",
"6": "Sports"
},
"current_category": [
5,
5,
],
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
}
],
"success": true,
"total_questions": 2
}
```

<hr>


### DELETE /questions/{question_id}

`http://127.0.0.1:5000/questions/1`

- Deletes a question based on the id sent in the URI
- Request Arguments: None
- Returns: Return a json object containg the id of the deleted question and a success value.
```
{
"deleted": 2,
"success": true
}
```
<hr>

### POST /questions

`http://127.0.0.1:5000/questions`

- Add a new question or fetches a list of questions based on a search term. 
  - To get the add behavior the request body should be similar to this
	```
	{
	question: "question",
	answer: "answer",
	difficulty: 1,
	category: 1
	}
	```
   - To get the search behaviour the request body should be similar to this
		```
		 {
		 searchTerm: "title"
		 }
		```
- Request Arguments: None
- Returns: a json object will be returned based on the body attributes if it matches the add or the search criteria.
   - For the Add it will return a success value and the id for the newly created question
		```
		{
		"success":True,
		"created":question.id,
		}
		```
	- For the search behaviour it will return a json object containing a success value, questions array including the questions which include  the term "case insensitive", a total of the questions which got retuned , categories dictionary and a current category array which  is ordred to match the questions array.
		```
			{
		"categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
		},
		"current_category": [
		4,
		5
		],
		"questions": [
		{
		"answer": "Maya Angelou",
		"category": 4,
		"difficulty": 2,
		"id": 5,
		"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
		},
		{
		"answer": "Edward Scissorhands",
		"category": 5,
		"difficulty": 3,
		"id": 6,
		"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
		}
		],
		"success": true,
		"total_questions": 2
		}
		```
<hr>

### GET /categories/{category_id}/questions
`http://127.0.0.1:5000/2/questions`

- Fetches an array of  questions based on a category
- Request Arguments: accept a category id "can be found using the /categories endpoint".
- Returns:  It will return a json object containing  a success value, questions array filtered by the selected category a total of the questions which got retuned , categories dictionary and a current category array which  is ordred to match the questions array.
```
{
"categories": {
"1": "Science",
"2": "Art",
"3": "Geography",
"4": "History",
"5": "Entertainment",
"6": "Sports"
},
"current_category": [
5,
5
],
"questions": [
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
}
],
"success": true,
"total_questions": 2
}
```

### POST  '/quizzes'
`http://127.0.0.1:5000/quizzes`

- Fetchs a question randomly which hasn’t been sent to the client before from all categories (id = 0) or from specific category based on the category id which was sent.
- Request Body: needs to sent an array of the previous questions ids and the selected category.
```
{
"previous_questions": [4,2,7],
"quiz_category":{"id":1},
}
```
- Returns:  It will return a json object containing the question object .
```
{
"question":
	{
	'id': self.id,
	'question': self.question,
	'answer': self.answer,
	'category': self.category,
	'difficulty': self.difficulty
	}
}
```

## Errors 
The expected errors that you might encounter using this API are (400,404,422,500)
A  sample of a retuned json when you get an error.

```
{
"success": False,
"error": 400,
"message": "Bad Request"
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```