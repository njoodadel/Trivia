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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
    #get categories
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])

    
    #get q
    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])

    def test_404_get_questions(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)   
        self.assertEqual(data['error'],404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"Not found")

    # #### delete
    # def test_delete_question(self):
    #     res = self.client().delete("/questions/9")
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code,200)
    #     self.assertEqual(data['success'],True)
    #     self.assertEqual(data['deleted'],9)
    
    def test_404_delete_question(self):
        res = self.client().delete("/questions/2000")
        data = json.loads(res.data)   
        self.assertEqual(data['error'],422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"Unprocessable Entity")

    def test_create_question(self):
        res = self.client().post("/questions", json = {
    'question': "question",
	'answer': "answer",
	'difficulty': 1,
	'category': 1
    })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['created'])

    def test_500_create_question(self):
        res = self.client().post("/questions")
        data = json.loads(res.data)
        self.assertEqual(data['error'],500)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"Internal Server Error")

    def test_search_question(self):
        res = self.client().post("/questions", json = {"searchTerm":"Tom"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])

    def test_404_search_question(self):
        res = self.client().post("/questions", json = {"searchTerm":"njood"})
        data = json.loads(res.data)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"Not found")


    def test_play(self):
        res = self.client().post("/quizzes", json = {
            "quiz_category":{"id":1},
            "previous_questions":[4,5]
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['question'])



    
    def test_400_play(self):
        res = self.client().post("/quizzes",json ={})
        data = json.loads(res.data)
        self.assertEqual(data['error'],400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"Bad Request")

    



    









   










    #search

    #delete
    #add q



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()