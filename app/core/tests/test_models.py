from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """
        Test that will test whether creating a new user with
        email and password is suceessful.
        """

        # Now create one fake email & password for testing the
        # user object
        email = "test_email@gmail.com"
        password = "TestPassword123"

        # Create fake user object using above emaill & pass
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        # Test the fake user object, whether properly created
        # or not.
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))