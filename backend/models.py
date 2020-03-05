import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from backend.keys import database


database_path = "postgres://keys.user:keys.user_pass@{}/{}".format('localhost:5432', database.name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Question

'''


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(Integer)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }


'''
Category

'''


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            self.id: self.type
            # 'id': self.id,
            # 'type': self.type
        }


class Support:

    # Functions to return the list of question to show on specified page of listing
    # Accepts :
    # - 'request' body to get the value of the 'page' parameter
    # - 'selection' as object of result of database query
    # Returns: list of objects to show in specified page
    def paginate_questions(request, selection):
        # Constant with the number fof questions to show in one page of listing
        QUESTIONS_PER_PAGE = 10

        from flask import request

        # retrieve the page value from the request
        page = request.args.get('page', 1, type=int)
        # Define start and end indexes of the list of objects to return
        start = (page-1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        # Format every question-representation we got in the selection object
        # NOTE : format() function defined in 'Question' class
        questions = [item.format() for item in selection]
        current_questions = questions[start:end]

        return current_questions

    # Get the list of categories
    def get_category(id=None):
        from flask import abort
        if id:
            data = Category.query.filter_by(id=id).order_by(Category.type).all()
        else:
            data = Category.query.order_by(Category.type).all()

        if data is None:
            abort(400)

        categories = {}

        for item in data:
            categories[item.id] = item.type

        return categories
