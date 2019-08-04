from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Now we will import some rest_framework test helper tools
from rest_framework.test import APIClient
# This just is a test client that we can use to make requests
# to our API and then check what the response is.
from rest_framework import status
# This is a module that contains some status codes that
# we can see in basically human readable form. So instead
# of just typing 200, it's HTTP 200 ok. It just makes the
# tests a little bit easier to read and understand.

CREATE_USER_URL = reverse('user:create')

# Then we're going to add a helper function that we can
# use to create some example users for our tests.
# So anything that you do multiple times in different tests,
# I like to create a helper function so instead of creating
# the user for each test individually you can just call the
# helper function and it just makes it a little bit easier
# to create users that you're testing with.


def create_user(**params):
    return get_user_model().objects.create_user(**params)

# So a public API is one that is unauthenticated so that is
# just anyone from the internet can make a request. An example
# of this would be the create user, because when you typically
# create a user on a system, usually you're creating a user
# because you haven't got authentication set up already.


class PublicUserAPITest(TestCase):
    """
    Test publicly available user api.
    """

    def setUp(self):
        """
        This function is run before every test from this
        class is run. So some times there are some set up
        task, that need to be done before running every
        test from this class.
        """
        # First create a test client
        self.client = APIClient()
        # What this above line does is, it basically set
        # APIClient() to self, so that other function from
        # this class can access APIClient()

    # We're going to create a test that validates the user
    # is created successfully.
    def test_create_valid_user_success(self):
        """
        Test creating user with valid payload is successfull.
        """
        # First create a valid payload
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass123',
            'name': 'Test user name'
        }

        # Now we will make our request to CREATE_USER_URL using
        # this avobe valid payload.
        res = self.client.post(CREATE_USER_URL, payload)
        # Here, our res object has user & http response status.

        # Now we will check our http response.
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Next we're going to test that the user object is actually
        # created. So we will retrieve created user from django db.
        user = get_user_model().objects.get(**res.data)

        # Now we will check the retrieved user password, with our
        # payload password. If match then, user creation is successfull.
        self.assertTrue(user.check_password(payload['password']))

        # finally we want to check that the password is not returned
        # as part of this above object 'user'
        self.assertNotIn('password', res.data)

    # Next we're going to test what happens if they try and create
    # a user but the user already exists. So we're trying to create
    # duplicate user here.
    def test_user_exist(self):
        """
        Test creating a user that already exist fail.
        """
        # Generate a valid payload
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass123',
            'name': 'Test user name'
        }
        # Create new user using create_user() function.
        create_user(**payload)

        # Now we will, try to create the same user by http post method.
        res = self.client.post(CREATE_USER_URL, payload)
        # Here, our res object has user & http response status.

        # We expect to see here is a HTTP 400 bad request because
        # it's a bad request because the user already exists.
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Now we are going to create a test which will check whether
    # the password is too short.
    def test_password_too_short(self):
        """
        Test password must be more than 5 characters
        """
        # Generate a payload with very short password
        payload = {
            'email': 'test@gmail.com',
            'password': 'pw',
            'name': 'Test user name'
        }

        # Now we will make our request to CREATE_USER_URL using
        # this avobe payload.
        res = self.client.post(CREATE_USER_URL, payload)
        # Here, our res object has user & http response status.

        # So we want to first make sure that it returns a HTTP bad
        # request.
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Now lets check that the user was never created.
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        # What this above code will do is, if the user exists it will
        # return true otherwise it will return false.
        self.assertFalse(user_exist)
