from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer

# We're going to create a new view and that view are going to inherit
# from create API view, that comes with the Django rest framework.
# So this is a view that's pre-made for us that allows us to easily
# make a API that creates an object in a database using the serialize
# that we're going to provide.


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system.
    """
    serializer_class = UserSerializer


class CreateAuthToken(ObtainAuthToken):
    """
    Create a new auth token for user.
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
