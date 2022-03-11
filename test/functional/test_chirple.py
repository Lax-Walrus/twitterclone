from werkzeug.security import generate_password_hash
from flask import current_app
from website import create_app, db
import unittest
import os
from website.models import User, Chirps, Comment, Like
os.environ['DATABASE_URL'] = 'sqlite://'
# --------------------------------------------


class TestWebApp(unittest.TestCase):
    def populate_db(self):
        user = User(id=99, email='test@test.com', username='testerB',
                    password=generate_password_hash('password', method='sha256'), isAdmin=True)

        user2 = User(email='tester@tester.com', username='testerF',
                     password=generate_password_hash('password', method='sha256'))
        chirp = Chirps(id=90, text="this is a prebuilt test", author=99)
        chirp2 = Chirps(id=95, text="this is a prebuilt test", author=99)
        like = Like(id=55, author=99, chirp_id=95)
        comment = Comment(
            id=80, text='this is a prebuilt test comment', author=99, chirp_id=90)
        db.session.add(user)
        db.session.add(user2)
        db.session.add(chirp)
        db.session.add(chirp2)
        db.session.add(like)
        db.session.add(comment)
        db.session.commit()

    def setUp(self):
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.populate_db()
        self.client = self.app.test_client()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app
