# Retsepile Koloko
# Classroom 2

import unittest
from app import app


class AppTest(unittest.TestCase):

    # testing whether or not endpoint status codes match (get/push/...) methods
    def test_sign_up(self):
        test = app.test_client(self)
        response = test.get('/sign-up')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_location(self):
        test = app.test_client(self)
        response = test.get('/location/')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_client(self):
        test = app.test_client(self)
        response = test.get('/client')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_get_users(self):
        test = app.test_client(self)
        response = test.get('/get-users/')
        status = response.status_code
        self.assertEqual(status, 201)


if __name__ == 'main':
    unittest.main()
