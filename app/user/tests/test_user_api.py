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
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')
# ME_URL = This is update user end point.

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

    def test_create_token_for_user(self):
        """
        Test the a token is created for the user.
        """
        # First we will create a user.
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass123',
            'name': 'Test user name'
        }
        # Create new user using create_user() function.
        create_user(**payload)

        # Now as our user has been created in our system, we will
        # check whether our system give us token for that user or
        # not. Now we will make our request to TOKEN_URL using
        # this avobe payload.
        res = self.client.post(TOKEN_URL, payload)
        # Here, our res object has token & http response status.

        # First we will check whether our system has given this user
        # authentication token or not.
        self.assertIn('token', res.data)
        # So this assertion will check whether there is a key called
        # 'token' in the res.data that we get back.

        # Next we will assert that response is HTTP 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # Now we're going to test what happens if we provide invalid
    # credentials.
    def test_create_token_invalid_credential(self):
        """
        Test that token is not created, if invalid credential is
        given.
        """
        # First we will create an user in our system.
        create_user(email='mujahid7292@gmail.com', password='123456')

        # Now we will create an invalid sign in attempt, means
        # user will provide valid email, but wrong password.
        payload = {
            'email': 'mujahid7292@gmail.com',
            'password': 'wrongPassword'
        }

        # Now we will try this invalid sign in
        res = self.client.post(TOKEN_URL, payload)
        # This res object generally contain the authentication
        # token & response status.

        # Now we will assert that, this res object does not have
        # token in it.
        self.assertNotIn('token', res.data)

        # Next we will assert that response is HTTP_400_BAD_REQUEST
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # In the next unit test we will check, if you're trying to authenticate
    # a non-existent user, what happen.
    def test_create_token_no_user(self):
        """
        Test that token is not created, if user does not exist.
        """
        # Now create our valid payload
        payload = {
            'email': 'mujahid7292@gmail.com',
            'password': '123456'
        }

        # Now we will try to authenticate with above user name
        # and password in our system, without creating user
        # with this exact email & password.

        # Now we will try this invalid sign in
        res = self.client.post(TOKEN_URL, payload)
        # This res object generally contain the authentication
        # token & response status.

        # Now we will assert that, this res object does not have
        # token in it.
        self.assertNotIn('token', res.data)

        # Next we will assert that response is HTTP_400_BAD_REQUEST
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # this unit test will check, if you provide a request that doesn't
    # include a password, token is not returned.
    def test_create_token_missing_field(self):
        """
        Test that to authenticate with the server, email and
        password is required.
        """
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        # This res object generally contain the authentication
        # token & response status.

        # Now we will assert that, this res object does not have
        # token in it.
        self.assertNotIn('token', res.data)

        # Next we will assert that response is HTTP_400_BAD_REQUEST
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # The first thing we're going to do is we're going to create a test
    # to make sure that authentication is required on the manage user
    # endpoint.
    def test_retrieve_user_unauthorized(self):
        """
        Test that authentication is required for the user.
        """
        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# We are going to make a PrivateUserAPITest class for authenticated test.
# Means test those require authentication will be in this class.
class PrivateUserAPITest(TestCase):
    """
    Test API requests that require authentication.
    """
    # Part of the setup, we're going to do the authentication
    # for each test that we do. So we don't need to basically set
    # the authentication for every single test we're just do the
    # setup and then that happens automatically before each test.
    def setUp(self):
        """
        This function is run before every test from this
        class is run. So some times there are some set up
        task, that need to be done before running every
        test from this class.
        """
        self.user = create_user(
            email='test@londonappdev.com',
            password='testpass',
            name='fname',
        )
        # This above code create a valid user in our system, so
        # that other function from this class can access this
        # specific user.
        self.client = APIClient()
        # What this above line does is, it basically set
        # APIClient() to self, so that other function from
        # this class can access APIClient()
        self.client.force_authenticate(user=self.user)
        # force_authenticate() method is used to authenticate any
        # requests that the client makes with our above user.

    # Next thing we're going to do is add our retrieve profile
    # successful test. We're just going to test that we can
    # retrieve the profile of the logged in user.
    def test_retrieve_profile_success(self):
        """
        Test retrieving profile for logged in user.
        """
        # Then what we will do is we'll just make the request because
        # we've already authenticated in our setup so we don't need
        # to do that authentication in this function.
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Then we're going to test that the user object returned is
        # what we expect.
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    # Next we're going to test that you cannot do a HTTP POST request
    # on the profile.
    def test_post_on_me_url_not_allowed(self):
        """
        Test that post is not allowed on the me url.
        """
        res = self.client.post(ME_URL, {})

        self.assertEqual(
            res.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    # Next we are going to add our user profile update test.
    # So we're going to update the user via the API and we're
    # going to test that the updates worked.
    def test_update_user_profile(self):
        """
        Test updating the user profile for authenticated user
        works.
        """
        payload = {
            'name': 'New Name',
            'password': 'newPassword123'
        }

        # Now we will update our user
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        # This above code will refresh our existing user.

        # Now we will check that our user is updated or not.
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
