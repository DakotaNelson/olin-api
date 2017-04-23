""" Currently undeveloped test suite for the authentication component of the API """

import unittest

from src.app import create_app

class TestCase(unittest.TestCase):
    def setUp(self):
        app = create_app(testing=True)
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_add(self):
        self.assertEqual(1, 1)
