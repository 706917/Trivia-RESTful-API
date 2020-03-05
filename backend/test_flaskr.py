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
        self.database_name = "trivia"
        self.database_path = "postgres://postgres: @{}/{}".format('localhost:5432', self.database_name)
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
    """--------TEST Full Questions listing------"""

    def test_get_questions(self):
        """ get response and load its body into the json object"""
        response = self.client().get('/api/questions')
        body = json.loads(response.data)

        """ check status code and message """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)
        """ check that we got data from response"""
        self.assertTrue(body['questions'])
        self.assertTrue(len(body['categories']))
        self.assertTrue(body['questions'])


    def test_404_questions_listing(self):
        """---------Test 404 error on questions listing----------"""
        # get response from request of invalid page number
        response = self.client().get('/questions?page=100')
        body = json.loads(response.data)

        ''' check status code and message'''
        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['success'], False)
        self.assertTrue(body['message'])

    def test_categories(self):
        """----------Test request for all categories----------"""
        response = self.client().get('/categories')
        body = json.loads(response.data)

        """ check status """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['access'], True)
        """ check data """
        self.assertTrue(body['categories'])

    def test_get_questions_by_category_id(self):
        """----------Tests getting questions by category id---------"""
        # send request with specified id=5 and get response
        response = self.client().get('/categories/5/questions')
        body = json.loads(response.data)

        # check response status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)

        # check that category has questions
        self.assertNotEqual(len(body['questions']), 0)

        # check that current category returned is 'Entertainment'
        self.assertEqual(data['current_category'], 'Entertainment')



    def test_question_delete(self):
        """-------Tests question delete--------------"""

        # create a new question
        question = Question(question=self.new_question['question'], answer=self.new_question['answer'],
                            category=self.new_question['category'], difficulty=self.new_question['difficulty'])
        question.insert()

        # id of the new question
        question_id = question.id

        # number of questions before delete
        total_questions_before_delete = Question.query.all()

        # delete the question and get response
        response = self.client().delete('/questions/{}'.format(question_id))
        body = json.loads(response.data)

        # number of questions after delete
        total_questions_after_delete = Question.query.all()

        # check the questions has been deleted - None expected
        question = Question.query.filter(Question.id == 1).one_or_none()

        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)

        # check if id of new question matches id of question deleted
        self.assertEqual(body['deleted'], question_id)

        # check if one less question after delete
        self.assertTrue(len(total_questions_before_delete) - len(total_questions_after_delete) == 1)

        # check if question equals None after delete
        self.assertEqual(question, None)

    def test_create_question(self):
        """-------------Tests question creation -----------"""

        # number of questions before post
        total_questions_before_post = Question.query.all()

        # create question and load response data
        response = self.client().post('/questions', json=self.new_question)
        body = json.loads(response.data)

        # number of questions after post
        total_questions_after_creation = Question.query.all()

        # check new question existence in db
        question = Question.query.filter_by(id=body['created']).one_or_none()

        # check status code and  message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)

        # check if one more question after post
        self.assertTrue(len(total_questions_after_creation) - len(total_questions_before_post) == 1)

        # check that question is not None
        self.assertIsNotNone(question)

    def test_search(self):
        """------------Tests search questions ---------------"""

        # send request with search term and get response
        response = self.client().post('/questions',json={'searchTerm': 'egyptians'})
        body = json.loads(response.data)

        # check response status code message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)

        # check data
        self.assertTrue(len(body['questions']))

    def test_404_search(self):
        """-------Tests search 404 error-------------"""

        # send post request with bad search term and get responce
        response = self.client().post('/questions', json={'searchTerm': 'abcdefghijk'})
        body = json.loads(response.data)

        # check response status code message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['success'], False)
        self.assertTrue(body['message'])









# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
