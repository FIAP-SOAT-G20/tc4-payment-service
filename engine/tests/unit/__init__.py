from unittest import TestCase

from engine import app


class PaymentUnitTest(TestCase):

    def setUp(self):
        self.app = app

    def tearDown(self):
        pass

    @staticmethod
    def create_app():
        return app
