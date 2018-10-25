from flaskr import app, db
import flaskr
import unittest

from flask_testing import TestCase


class FlaskrTestCase(unittest.TestCase):
	
	# url /login повертає код 200
	def test_login_code(self):
		tester = app.test_client(self)
		response = tester.get('/login', content_type = 'html/text')
		self.assertEqual(response.status_code, 200)

	# слово Login - частина html за url /login
	def test_login_page(self):
		tester = app.test_client(self)
		response = tester.get('/login', content_type = 'html/text')
		self.assertTrue(b'Login' in response.data)

	# коли залогінився правильно редіректнуло на добру сторінку
	def test_login_correct(self):
		tester = app.test_client(self)
		response = tester.post('/login', data = dict(username = 'admin', password = 'default'), follow_redirects = True)
		self.assertTrue(b'u were logged in' in response.data)

	# коли залогінився неправильно не редіректнуло на добру сторінку
	def test_login_incorrect(self):
		tester = app.test_client(self)
		response = tester.post('/login', data = dict(username = 'incorrect', password = 'default'), follow_redirects = True)
		self.assertTrue(b'Bad username' in response.data)


	# logout працює добре
	def test_logout(self):
		tester = app.test_client(self)
		response = tester.post('/login', data = dict(username = 'admin', password = 'default'), follow_redirects = True)
		response = tester.get('/logout', follow_redirects = True)
		self.assertTrue(b'logout succeded' in response.data)

	# index page вимагає Login
	def test_logout(self):
		tester = app.test_client(self)
		response = tester.post('/login', data = dict(username = 'admin', password = 'default'), follow_redirects = True)
		response = tester.get('/logout', follow_redirects = True)
		self.assertTrue(b'logout succeded' in response.data)

	# index page містить login here
	def test_index_login(self):
		tester = app.test_client(self)
		response = tester.get('/', content_type = 'html/text')
		self.assertTrue(b'loGin here' in response.data)

	# main page містить замітки
	def test_index_post(self):
		tester = app.test_client(self)
		response = tester.get('/', content_type = 'html/text')
		self.assertTrue(b'redact' in response.data)


if __name__ == '__main__':
	unittest.main()