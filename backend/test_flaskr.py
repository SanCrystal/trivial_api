import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(os.environ.get('USERNAME'),os.environ.get('PASSWORD'),'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question1 = {
            "question": "Who is the best tutor at Udacity?",
            "answer": "Amy",
            "category": "4",
            "difficulty": 1
        }
        self.new_question2 = {
            "question": "Who is the longest serving president in Africa?",
            "answer": "Robert Mugabe",
            "category": "4",
            "difficulty": ""
        }
        self.searchTerm = "Which country won the first ever soccer World Cup in 1930?"
        
        self.quiz_data = {
            "previous_questions": [],
            "quiz_category": { "type": "Science", "id": "1" }
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Test for Categories endpoints 200 success case
    def test_get_category_200(self):
        """
            Test for Category success (200)
        """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["categories"])


    # Test for Questions endpoints 200 success case
    def test_get_questions_200(self):
        """
            Test for Question success (200)
        """
        res =self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertEqual(data["current_category"],None)

    # Test Pagination request beyond valid page number case
    def test_pagination_beyond_valid_page_number(self):
        """
            Test for Pagination beyond valid page number
        """
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertEqual(len(data["questions"]),0)
        self.assertEqual(data["current_category"],None)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])


    # Test fot Delete Question endpoint 200 success case
    def test_delete_questions_200(self):
        """
            Test for Delete Question success (200)
        """
        res = self.client().delete('/questions/15')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 15).one_or_none()
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertEqual(data["deleted"],15)
        self.assertEqual(question,None)
    

    # Test for Delete Question endpoint 422 unprocessable entity case
    def test_delete_questions_404(self):
        """
            Test for Delete Question 422 unprocessable entity
        """
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data["success"],False)
        self.assertEqual(data["error"],422)
        self.assertEqual(data["message"],"unprocessable entity")
    

    # Test for Add Question endpoint 200 success case
    def test_add_question_200(self):
        """
            Test for Add Question success (200)
        """
        res = self.client().post('/questions',json=self.new_question1)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        

    # Test for Add Question endpoint 422 unprocessable entity case
    def test_add_question_422(self):
        """
            Test for Add Question 422 unprocessable entity
        """
        res = self.client().post('/questions',json=self.new_question2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data["success"],False)
        self.assertEqual(data["error"],422)
        self.assertEqual(data["message"],"unprocessable entity") 

    # Test for Search Question endpoint 200 success case
    def test_search_question_200(self):
        """
            Test for Search Question success (200)
        """
        res = self.client().post('/questions',json={"searchTerm":self.searchTerm})
        data = json.loads(res.data)

        _questions = Question.query.filter(Question.question.ilike(f'%{self.searchTerm}%')).all()
        questions = [question.format() for question in _questions]
        _categories = [i['category'] for i in questions]
        current_category = max(_categories,key=_categories.count)  if len(_categories) >0 else None
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertEqual(len(data["questions"]),len(questions))
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"],current_category)

    # Test for get Question By Category endpoint 200 success case
    def test_get_question_by_category_200(self):
        """
            Test for get Question By Category success (200)
        """
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)

        questions = Question.query.filter(Question.category == 1).all()
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertEqual(len(data["questions"]),len(questions))
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"]["id"],5)

    # Test for get Question By Category endpoint 404 not found case
    def test_get_question_by_category_404(self):
        """
            Test for get Question By Category 404 not found
        """
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data["success"],False)
        self.assertEqual(data["error"],404)
        self.assertEqual(data["message"],"resource not found")

    # Test for Quiz endpoint 200 success case
    def test_quiz_200(self):
        """
            Test for Quiz success (200)
        """
        res = self.client().post('/quizzes',json=self.quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["question"])
        self.assertTrue(data["category"])
        

    # Test for Endpoint method not allowed case
    def test_quiz_405(self):
        """
            Test for Quiz 405 method not allowed
        """
        res = self.client().get('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertEqual(data["success"],False)
        self.assertEqual(data["error"],405)
        self.assertEqual(data["message"],"method not allowed")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()