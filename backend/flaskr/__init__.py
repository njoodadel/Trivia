import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    Questions_PER_PAGE = 10

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * Questions_PER_PAGE
        end = start + Questions_PER_PAGE
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

    def categories():
        selection = Category.query.all()
        return {category.id: category.type for category in selection}

    @app.route('/categories', methods=["GET"])
    def get_categories():
        categoriesList = categories()

        if len(categoriesList) == 0:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "categories": categoriesList
            })

    @app.route('/questions', methods=["GET"])
    def get_questions():
        # get categories
        categoriesList = categories()

        questions = []
        currentCategort = []
        selection = Question.query.order_by(Question.id).all()

        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)
        else:
            for question in current_questions:
                questions.append(question)
                currentCategort.append(question["category"])
            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "categories": categoriesList,
                "current_category": currentCategort,
            })

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "deleted": question.id,
            })

        except BaseException:
            abort(422)

    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()
        searchTerm = body.get('searchTerm', None)
        if searchTerm is not None:
            categoriesList = categories()

            questions = []
            currentCategort = []

            selection = Question.query.filter(
                Question.question.ilike(
                    "%" + searchTerm + "%")).all()
            current_questions = paginate_questions(request, selection)

            for question in current_questions:
                questions.append(question)
                currentCategort.append(question["category"])
            if len(current_questions) == 0:
                abort(404)
            else:
                return jsonify({
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(selection),
                    "categories": categoriesList,
                    "current_category": currentCategort,
                })

        else:

            new_question = body.get('question', None)
            new_answer = body.get("answer", None)
            new_difficulty = int(body.get("difficulty", None))
            new_category = body.get("category", None)
            if new_question is None or new_answer is None or new_difficulty is None or new_category is None:
                abort(400)

            try:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    difficulty=new_difficulty,
                    category=new_category)
                question.insert()


                return jsonify({
                    "success": True,
                    "created": question.id,

                })

            except BaseException:
                abort(422)

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_category(category_id):
        categoriesList = categories()

        questions = []
        currentCategort = []
        selection = Question.query.filter(
            Question.category == category_id).all()

        current_questions = paginate_questions(request, selection)
        for question in current_questions:
            questions.append(question)
            currentCategort.append(question["category"])
        if len(current_questions) == 0:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "categories": categoriesList,
                "current_category": currentCategort,
            })

    @app.route("/quizzes", methods=["POST"])
    def play():

        body = request.get_json()
        previousQuestions = body.get('previous_questions', None)
        quizCategory = body.get('quiz_category', None)
        if quizCategory is None or previousQuestions is None:
            abort(400)

        allQuestion = Question.query.all()

        randomID = random.randint(1, len(allQuestion) - 1)
        isPrevious = True
        question = None
        if quizCategory['id'] == 0:
            while isPrevious:
                question = Question.query.filter(
                    Question.id == randomID).first()
                if len(previousQuestions) >= len(allQuestion):
                    question = None
                    abort(400)
                    break
                if question is None:
                    randomID = random.randint(1, len(allQuestion) - 1)
                    continue
                if question.id in previousQuestions:
                    continue
                else:
                    isPrevious = False

        else:
            questionByCategory = Question.query.filter(
                Question.category == quizCategory['id']).all()
            randomID = random.randint(0, len(questionByCategory) - 1)
            while isPrevious:
                question = Question.query.filter(
                    Question.category == quizCategory['id']).all()
                if len(previousQuestions) >= len(question):
                    question = None
                    abort(400)

                    break
                question = question[randomID]
                if question.id in previousQuestions:
                    continue
                else:
                    isPrevious = False
        return jsonify({
            "question": question.format()
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        })

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        })

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        })

    return app
