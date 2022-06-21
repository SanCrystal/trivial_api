
import os
from sys import prefix
from flask import Flask, request, abort, jsonify,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    route_prefix = '/api/v1.0'
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r'/*': {'origins': '*'}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    DONE
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response


    # pagination
    def pagination(req,selection):
        page = req.args.get('page',1 ,type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions, len(questions)

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    DONE
    """
    # GET /categories
    @app.route(route_prefix+'/categories',methods=['GET'])
    def get_categories():
        _categories = Category.query.all()
       
        categories = {category.format()["id"]:category.format()["type"] for category in _categories}
        return jsonify({
            'success': True,
            'categories': categories
        })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    DONE
    """
    # GET /questions
    @app.route(route_prefix+'/questions',methods=["GET"])
    def get_questions():
        _questions = Question.query.all()
        questions, total_questions = pagination(request,_questions)
        categories_list = Category.query.all()
        categories = {category.format()["id"]:category.format()["type"] for category in categories_list}
        
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': total_questions,
            'categories': categories,
            'current_category': None
        })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    DONE
    """
    # DELETE /questions/<id>
    @app.route(route_prefix+'/questions/<int:question_id>',methods=["DELETE"])
    def delete_questions(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            question.delete()
            return jsonify({
                'success': True,
                'deleted_id': question_id
            })
        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    DONE
    """
    # POST /questions || add questions
    @app.route(route_prefix+'/questions',methods=["POST"])
    def add_question_search_question():
        
        try:
            if "searchTerm" in request.get_json():
                searchTerm = request.get_json()["searchTerm"]
                _questions = Question.query.filter(Question.question.ilike('%'+searchTerm+'%')).all()
                questions, total_questions = pagination(request,_questions)

                # number of occurence of categories in questions would be set to current category
                _categories = [i['category'] for i in questions]
                current_category = max(_categories,key=_categories.count)  if len(_categories) >0 else None
                
                return jsonify({
                    'success': True,
                    'questions': questions,
                    'total_questions': total_questions,
                    'current_category': current_category,
                })
            
            question = request.get_json()["question"]
            answer = request.get_json()["answer"]
            category = request.get_json()["category"]
            difficulty = request.get_json()["difficulty"]
            # check that data values are not empty
            if question == "" or answer == "" or category == "" or difficulty == "":
                abort(422)

            # add questions to db
            new_question = Question(question,answer,category,difficulty)
            new_question.insert()
            return jsonify({
                'success': True,
            })
        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    DONE
    """
    # POST /questions (search)
    # @app.route('/questions',methods=["POST"])
    # def search_questions():
      
        
        

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    DONE
    """
    # GET /categories/<category_id>/questions
    
    @app.route(route_prefix+'/categories/<int:category_id>/questions',methods=["GET"])
    def get_questions_by_category(category_id):
        try:
            _questions =Question.query.filter(Question.category == category_id).all()
            current_category = Category.query.filter(Category.id == category_id).one_or_none()
            if current_category is None:
                abort(404)
            
            questions,total_questions = pagination(request,_questions)
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': total_questions,
                'current_category': current_category.format()
            })
        except:
            abort(404)


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    DONE
    """
    # POST /quizzes
    @app.route(route_prefix+'/quizzes',methods=["POST"])
    def get_quiz_question():
        try:
            category = request.get_json()["quiz_category"]
            previous_questions = request.get_json()["previous_questions"]
            questions,total_questions= pagination(request,Question.query.filter(Question.category == category["id"]).all() if category["id"] != 0 else Question.query.all())
            

            # check previous questions
            filtered_question = [question for question in questions if question['id'] not in previous_questions]
            # get random question from filtered question
            quiz =random.choice(filtered_question) if len(filtered_question)>0 else None
            
            return jsonify({
                'success': True,
                'question': quiz,
                'category': category
            })

        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    DONE
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable entity"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
             "success": False,
            "error": 500,
            "message": "internal server error"
        }),500
    return app

