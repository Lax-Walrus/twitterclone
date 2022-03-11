import pytest
from website.models import User, Chirps, Comment, Like
from werkzeug.security import generate_password_hash, check_password_hash


def test_new_user():
    """ GIVEN a User Model
        WHEN a new User is created
        THEN check the email, username and password """
    user = User(email='test@test.com',
                username='testusername', password=generate_password_hash(
                    'password', method='sha256'))

    assert user.email == 'test@test.com'
    assert user.username == 'testusername'
    assert user.password != "password"


def test_chirp():
    """ GIVEN a Chirp Model
       WHEN a new Chirp is created
       THEN check the text of the chirp """

    post = Chirps(text="this is a test chirp")
    assert post.text == "this is a test chirp"


def test_comment():
    """ GIVEN a Comment Model
       WHEN a new Comment is created
       THEN check the text of the Comment """
    comment = Comment(text="this is a test comment")
    assert comment.text == "this is a test comment"


def test_like():
    """ GIVEN a Like Model
        When a like is created
        THEN check if author exsits"""
    like = Like(author="Tester")
    assert like.author == "Tester"
