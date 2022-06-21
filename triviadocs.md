# Trivia API Project Documentation
### Setup and installations
- Python Installation version [Python 3.7](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python-for-your-platform) and above.
- Clone the project from [GitHub](https://github.com/SanCrystal/trivial_api.git) and navigate to the `backend` directory
- Virtual Environment Installation 
- Pip Dependencies Installation navigate to the backend directory and run    `pip install -r requirements.txt`
- **Database Setup**
  - Create a `trivia` database using the `createbd -U <username> trivia` command and populate the database using the `trivia.psql` file provided. 
    - Run the `psql -U <username> trivia < trivia.psql` command to populate the database.
- **Server Setup**
    - From the `backend` directory first ensure you are working using your created virtual environment. If not create one by running `python -m venv venv`or `python3 -m venv venv`.  run `venv/Script/activate` on windows `cmd` or `source venv/bin/activate` on mac to activate the virtual environment.

    - Run `export FLASK_APP=flaskr` on `bash or mac` || `set FLASK_APP=flaskr` on windows  `cmd` to set the flask application to run.

    - Run `export USERNAME=<username>` on `bash or mac` || `set USERNAME=<username>` on windows  `cmd` to set the environment variable for the username of database.
    - Run `export PASSWORD=<password>` on `bash or mac` || `set PASSWORD=<password>` on windows  `cmd` to set the environment variable for the password of database.
    - Run `flask run` to run the server. 

    - **_server should be up on default port of 5000_** _`http://localhost:5000/`_


## Trivia API Documentation
Trivia API is a api that provides a trivia game to the users. Here users can get a random question and answer from the database, Check the answer and get the next question. Also user can create questions and answers and post to the database.

### API Documentation

## Getting started
- General:
    - `Base URL` - The base URL of the API is currently running on `(http://localhost:5000/)[http://localhost:5000/]` 

    - `Authentication` - Currently, the API does not require authentication or an API key to function.

## Error Handling
- General:
    All data returned by the API is returned in a json format including the errors and status codes. The error returned are of the format:
    - `success` - A boolean value indicating whether the request was successful or not.
    - `error` - The error code.
    - `message` - The error message.

    - Example of an error response returned for a `404` request:
    ```
        {
            "success": False, 
            "error": 400,
            "message": "bad request"
        }
    ```
    - List of errors returned by the API:
        -- `400` - Bad Request
        -- `404` - Resource Not Found
        -- `422` - Not Processable
        -- `405` - Method Not Allowed
        -- `500` - Internal Server Error

## Endpoint Library
- General:
    The endpoints currently supported by the API are:

    ##### GET /api/v1.0/categories
    - `GET /api/v1.0/categories` - Returns an object of quiz categories, where the keys are the `category id `and the values are the `category name`.
   
    Example of a  `GET` request to `/api/v1.0/categories`:
    ```
        curl http://localhost:5000/api/v1.0/categories
    ```
    Expected response:

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
        "success": true
     }
    ```

    ##### GET /api/v1.0/questions

    - `GET /api/v1.0/questions` - Gets all questions paginated in groups of 10 per page, with all categories included. It also returns the total number of questions in the database.

    Example of a `GET` request to `/api/v1.0/questions`:
    ```
        curl http://localhost:5000/api/v1.0/questions

    ```
    Expected response:

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
        "current_category": null,
        "questions": [
            {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
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
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
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
            }
        ],
        "success": true,
        "total_questions": 21
        }
    ```   

    ##### GET /api/v1.0/categories/<int:category_id>/questions (get questions by category)

    - `GET /api/v1.0/categories/<int:category_id>/questions` - Gets all questions by category paginated in groups of 10 per page, with all categories included. It also returns the total number of questions in the database.

    Example of a `GET` request to `/api/v1.0/categories/1/questions`:

    ```
        curl http://localhost:5000/api/v1.0/categories/1/questions
    ```
    Expected response:

    ```
        {
            "current_category": {
                "id": 1,
                "type": "Science"
            },
            "questions": [
                {
                "answer": "The Liver",
                "category": 1,
                "difficulty": 4,
                "id": 20,
                "question": "What is the heaviest organ in the human body?"
                },
                {
                "answer": "Alexander Fleming",
                "category": 1,
                "difficulty": 3,
                "id": 21,
                "question": "Who discovered penicillin?"
                },
                {
                "answer": "Blood",
                "category": 1,
                "difficulty": 4,
                "id": 22,
                "question": "Hematology is a branch of medicine involving the study of what?"
                },
                {
                "answer": "e = mc^2",
                "category": 1,
                "difficulty": 1,
                "id": 25,
                "question": "What is the famous equation by Eienstein"
                }
            ],
            "success": true,
            "total_questions": 4
        }
    ```

    ##### POST /api/v1.0/questions

    - `POST /api/v1.0/questions` - Adds a question to the database. A proper format of the body of the request should be a JSON object with the following keys: 
        - `question` - The question itself.
        - `answer` - The correct answer to the question.
        - `difficulty` - The difficulty level of the question.
        - `category` - The category of the question.
    
    Example of a `POST` request to `/api/v1.0/questions`:

    ```
        curl -X POST -H "Content-Type: application/json" -d '{"question":"Why is Trivia API so cool?","answer":"Because the documentations are awesome", "category":"1","difficulty":"1"}' http://localhost:5000/api/v1.0/questions
    ```
    Expected response:

    ```
        {
            "success": true,
        }
    ```

    ##### POST /api/v1.0/question -(Search questions)

    - `POST /api/v1.0/question` - Search questions relatable strings in the question body.

    Example of a `POST` request to `/api/v1.0/question`:

    ```
         curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"peanut"}' http://localhost:5000/api/v1.0/questions

    ```
    Expected response:

    ```
    {
        "current_category": 4,
        "questions": [
            {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
            }
        ],
        "success": true,
        "total_questions": 1
    }

    ```
#### DELETE /api/v1.0/questions/<int:question_id> (delete question)
 - `DELETE /api/v1.0/questions/<int:question_id>` - Deletes a question with the corresponding ID `question_id` from the database.

  Example of a `DELETE` request to `/api/v1.0/question/`:

    ```
         curl -X DELETE http://localhost:5000/api/v1.0/questions/2

    ```
    Expected response:
    ```
        {
            "success": true,
            "deleted_id": 2
        }
    ```

#### POST /api/v1.0/quizzes (create quiz)
 - `POST /api/v1.0/quizzes` - Returns a random quiz with the questions in the database. A proper format of the body of the request should be a JSON object with the following keys: 
    - `quiz_category` - The category of the questions in the quiz.

    - `previous_questions` - An array of previous questions that have already been asked. [] (empty array) if it is the first question.

Example of a `POST` request to `/api/v1.0/quizzes`:

    ```
        curl -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"id":1,"type":"Science"},"previous_questions":[]}' http://localhost:5000/api/v1.0/quizzes
    ```
Expected response:
    ```
        {
            "category": {
                "id": 1,
                "type": "Science"
            },
            "question": {
                "answer": "Alexander Fleming",
                "category": 1,
                "difficulty": 3,
                "id": 21,
                "question": "Who discovered penicillin?"
            },
            "success": true
        }
    ```
A subsequent request to the same endpoint will return a new question that is not one of the questions that have already been asked.

Example of a `POST` request to `/api/v1.0/quizzes` with previous questions:

    ```
        curl -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"id":1,"type":"Science"},"previous_questions": {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        }}' http://localhost:5000/api/v1.0/quizzes
    ```
Expected response:

    ```
        {
            "category": {
                "id": 1,
                "type": "Science"
            },
            "question": {
                "answer": "The Liver",
                "category": 1,
                "difficulty": 4,
                "id": 20,
                "question": "What is the heaviest organ in the human body?"
            },
            "success": true
        }
    ```
## Acknowledgements

 - I would like to thank [the Udacity team](https://www.udacity.com) for the support and guidance.
 - Special thanks to all the session leads, career coaches and students who have helped me learn how to structure codes that follows required formats.
 
## **Author**
- [Amanze Arthur](https://www.github.com/sancrystal)

