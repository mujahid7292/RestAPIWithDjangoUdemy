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


    def test_new_user_email_normalized(self):
        """
        This test will check whether we have implemented
        email text normalized / convert all upper case letter
        in email to lowercase or not.
        """

        # Now we will create a dummy email with all upper case
        # after @ sign 
        email = "test_email@GMAIL.COM"
        password = "Test1234"

        # Create fake user object using above emaill & pass
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        # Now we will check whether our upper case email
        # has been converted into lower case.
        self.assertEqual(user.email, email.lower())


    def test_invalid_user_email_raise_value_error(self):
        """
        This test will ensure that if we try to create a new
        user without providing an emaill address, our function
        will raise a value error.
        """
        with self.assertRaises(ValueError):
            # anything that we run in here should 
            # raise the value error And if it doesn't 
            # raise the value error, then this test will fail.
            get_user_model().objects.create_user(None,'test123')