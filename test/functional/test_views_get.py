import pytest
from test_chirple import TestWebApp


class Test_Views_get(TestWebApp):

    def login(self):
        self.client.post(
            '/login', data={'email': 'test@test.com', 'password': 'password'})

    def test_views_login_get(self):
        """ GIVEN a flask application configured for testing
                WHEN the '/' page is request (GET)
                THEN check that the response and redirect are valid"""

        response = self.client.get('/', follow_redirects=True)

        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'name="email"' in html
        assert 'name="password"' in html
        assert 'type="submit"' in html
        assert response.request.path == '/login'

    def test_views_sign_up(self):
        response = self.client.get('/signup')

        assert response.status_code == 200
        html = response.get_data(as_text=True)

        assert 'name="username"' in html
        assert 'name="email"' in html
        assert 'name="password1"' in html
        assert 'name="password2"' in html
        assert 'type="submit"' in html

    def test_views_user_profile(self):
        self.login()
        response = self.client.get('/chirps/testerB')

        assert response.status_code == 200
        html = response.get_data(as_text=True)

        assert 'name="username"' in html
        assert 'name="password1"' in html
        assert 'name="password2"' in html
        assert 'type="submit"' in html

    def test_views_profile(self):
        self.login()
        response = self.client.get('/chirps/testerF')

        assert response.status_code == 200
        html = response.get_data(as_text=True)

        assert "testerF's posts:" in html

    def test_views_admin(self):
        self.login()
        response = self.client.get('/dashboard')

        assert response.status_code == 200

        html = response.get_data(as_text=True)

        assert 'Hello Admin Here is your Dashboard'in html