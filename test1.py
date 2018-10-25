from flaskr import app, db, Entries
from flask_testing import TestCase


class BaseTestCase(TestCase):
	
	def createApp(self):
		app.config.from_object('config.TestConfig')
		return app
	
	def setUp(self):
		db.create_all()

		db.session.add(Entries('user_name', 'title', 'text', False))
		db.session.commmit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()


class FlaskrTestCase(BaseTestCase):
	
	# url /login повертає код 200
	def test_login_code(self):
		
		response = self.client.get('/login', content_type = 'html/text')
		self.assertEqual(response.status_code, 200)

	# слово Login - частина html за url /login
	def test_login_page(self):
		
		response = self.client.get('/login', content_type = 'html/text')
		self.assertTrue(b'Login' in response.data)

	# коли залогінився правильно редіректнуло на добру сторінку
	def test_login_correct(self):
		
		response = self.client.post('/login', data = dict(username = 'admin', password = 'default'), follow_redirects = True)
		self.assertTrue(b'u were logged in' in response.data)

	# коли залогінився неправильно не редіректнуло на добру сторінку
	def test_login_incorrect(self):
		
		response = self.client.post('/login', data = dict(username = 'incorrect', password = 'default'), follow_redirects = True)
		self.assertTrue(b'Bad username' in response.data)


	# logout працює добре
	def test_logout(self):
		
		response = self.client.post('/login', data = dict(username = 'admin', password = 'default'), follow_redirects = True)
		response = self.client.get('/logout', follow_redirects = True)
		self.assertTrue(b'logout succeded' in response.data)

	# index page вимагає Login
	def test_logout(self):
		
		response = self.client.post('/login', data = dict(username = 'admin', password = 'default'), follow_redirects = True)
		response = self.client.get('/logout', follow_redirects = True)
		self.assertTrue(b'logout succeded' in response.data)

	# index page містить login here
	def test_index_login(self):
		
		response = self.client.get('/', content_type = 'html/text')
		self.assertTrue(b'loGin here' in response.data)

	# main page містить замітки
	def test_index_post(self):
		
		response = self.client.get('/', content_type = 'html/text')
		self.assertTrue(b'redact' in response.data)