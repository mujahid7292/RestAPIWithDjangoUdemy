from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        """
        This function is run before every test from this
        class is run. So some times there are some set up
        task, that need to be done before running every
        test from this class.
        """
        # First create a test client
        self.client = Client()
        # What this above line does is, it basically set
        # Client() to self, so that other function from
        # this class can access Client()

        # Create an admin, which will be used to logged
        # into the above client
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='admin123'
        )
        # Now make the admin login to the client
        self.client.force_login(self.admin_user)
        # This above line will help us to run our test smothly,
        # because now we don't have to manualy log the user in,
        # we can use this above force_login() helper function.

        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='Test123',
            name='Full name of the test user'
        )

    def test_user_listed(self):
        """
        Test that user's are listed on user page.
        """
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
