from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@gmail.com', password='testPassword'):
    """
    Create a sample user
    """
    return get_user_model().objects.create_user(email, password)


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
            email=email,
            password=password
        )

        # Test the fake user object, whether properly created
        # or not.
        self.assertEqual(user.email, email)
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
            email=email,
            password=password
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
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_super_user(self):
        """
        This test will check whether a new user is
        created and have the super user & staf tag
        assigned to it.
        """
        user = get_user_model().objects.create_superuser(
            'test_123@gmail.com',
            'Test123'
        )

        # check whether new user is super user
        self.assertTrue(user.is_superuser)
        # check whether new user is staff
        self.assertTrue(user.is_staff)

    # we're just going to create a simple test that creates a
    # tag and verifies that it converts to the correct string
    # representation.
    def test_tag_str(self):
        """
        Test the tag string representation
        """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)
