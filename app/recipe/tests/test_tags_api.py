from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """
    Test the publicly available tags API.
    """
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """
        Test that login required for retrieving tags.
        """
        res = self.client.get(TAGS_URL)
        # This will make un authenticated request.

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """
    Test the authorized user tags API.
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # All we're going to do here is, we're going to set up by creating
    # a couple of sample tags and then we're going to make the request to
    # the API And then we're going to check that the tags returned equal
    # what we expect them to equal.
    def test_retrieve_tags(self):
        """
        Test retrieving tags.
        """
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)
        # This is going to make a HTTP GET request to the URL
        # which should return our tags. Our `Vegan` & `Dessert`
        # tags.

        tags = Tag.objects.all().order_by('-name')
        # This just ensures that the tags are returned in alphabetic
        # reverse order based on the name.

        # Now we're going to serialize our tags object.
        serializer = TagSerializer(tags, many=True)
        # Because there's going to be more than one item in our
        # serializer we're going to do `many=True`
        # if you pass it without `many=True`, it will
        # assume that you are trying to serialize a single object.
        # And we want to serialize the list of objects so we pass
        # in `many=True`.

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # Now we want to test that the tags that are retrieved are limited just to
    # the user that is logged in so we only want to see tags that are
    # assigned to the authenticated user.
    def test_tags_limited_to_user(self):
        """
        Test that tags returned, are for the authenticated user.
        """
        # what we're going to do first is we're going to create a new user
        # in addition to the user that is created at the setUp() just so we
        # can assign a tag to that user and then we can compare that, tag
        # was not included in the response because it was not the authenticated user.
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'testpass'
        )
        # Now we will create a Tag object for `user2`
        Tag.objects.create(user=user2, name='Fruity')

        # Now we will create a Tag object for the authenticated user,
        # means user which has been created in setUp().
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        # Now we will make our request.
        res = self.client.get(TAGS_URL)
        # So we would expect the one tag to be returned in the list
        # because that's the only tag assigned to the authenticated user.

        # Now we will do some assertion.
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Next we're going to check the length of the results returned
        # because if there's two returns then that's a problem. if there's
        # one returns then that's what we expect. Because we only created
        # one tag assigned to the authenticated user.
        self.assertEqual(len(res.data), 1)

        # Next we're going to test that the name of the tag returned
        # in the one response is the tag that we create and assign to
        # the authenticated user.
        self.assertEqual(res.data[0]['name'], tag.name)
        # So if we only return one result and that one result has the
        # name of the one that's assigned to the user that's authenticated.
        # We can be pretty confident that our API is limiting the results to
        # the authenticated user.
