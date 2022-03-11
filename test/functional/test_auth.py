import pytest
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash
from test_chirple import TestWebApp


class Test_Auth_Post(TestWebApp):
    def test_auth_create_account_post(self):
        """ GIVEN a flask application configured for testing
            WHEN the '/sign-up' page is request (POST)
            THEN check that the response is 200"""

        response = self.client.post('/signup', data={"email": "test@tester.com", 'username': 'testerA',
                                    'password1': 'password', 'password2': 'password'}, follow_redirects=True)

        assert response.status_code == 200
        assert response.request.path == '/home' or '/'

    def test_auth_signout_get(self):
        response = self.client.get('/logout', follow_redirects=True)
        assert response.request.path == '/login'

    def test_auth_login_post(self):
        """ GIVEN a flask application configured for testing
            WHEN the '/login' page is request (POST)
            THEN check that the response is 200"""

        response = self.client.post('/login', data={"email": "test@test.com", 'password':
                                                    'password'}, follow_redirects=True)

        assert response.status_code == 200
        html = response.get_data(as_text=True)

        assert response.request.path == '/home' or '/'

        assert 'CHIRPLE' in html
        assert 'Logout' in html
        assert 'Profile' in html
        assert 'Home' in html

    def login(self):
        self.client.post(
            '/login', data={'email': 'test@test.com', 'password': 'password'})

    def test_create_chirp_post(self):
        self.login()
        response = self.client.post(
            '/createchirp', data={'text': 'this is a test post'}, follow_redirects=True)
        assert response.status_code == 200

        html = response.get_data(as_text=True)
        assert 'this is a test post' in html

    def test_auth_updateuser_update(self):
        self.login()
        response = self.client.post(
            '/updateUser/testerB', data={'username': "testerC", 'password1': 'password', 'password2': 'password'}, follow_redirects=True)

        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'testerC' in html

    def test_create_comment(self):
        self.login()

        response = self.client.post(
            '/createcomment/1', data={'text': 'this is a test comment'}, follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        assert response.request.path == '/' or '/home'
        assert 'Comment added successfully' in html

    def test_like(self):
        self.login()
        response = self.client.post('/likechirp/90', follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        assert '{"liked":true,"likes":1}' in html

    def test_unlike(self):
        self.login()
        response = self.client.post('/likechirp/95', follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        assert '{"liked":false,"likes":0}' in html

    def test_delete_comment(self):
        self.login()
        response = self.client.get('/deletecomment/80', follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        assert 'Comment successfully removed!' in html

    def test_delete_chirp(self):
        self.login()
        response = self.client.get('/deletechirp/90', follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'Chrip Deleted' in html
