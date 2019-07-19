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
        # Now we are going to do a http get on this above url.
        res = self.client.get(url)

        # Now we will assert that our response object has user
        # name & email.
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """
        Test that the user edit page work.
        """
        url = reverse('admin:core_user_change', args=[self.user.id])
        # This reverse() function will create url like this:
        # /admin/core/user/1

        # Now we are going to do a http get on this above url.
        res = self.client.get(url)

        # Now we will test that this page rendered ok.
        self.assertEqual(res.status_code, 200)
        # 200 means rendered ok.

    def test_create_user_page(self):
        """
        Test that will verify that create user page rendered
        correctly or not.
        """
        url = reverse('admin:core_user_add')
        # Now we are going to do a http get on this above url.
        res = self.client.get(url)

        # Now we will test that this page rendered ok.
        self.assertEqual(res.status_code, 200)
        # 200 means rendered ok.