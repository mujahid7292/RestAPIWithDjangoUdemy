from rest_framework import generics, authentication, permissions
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

class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manage the authenticated user.
    """
    serializer_class = UserSerializer
    # Below this we're going to add two more class variables for
    # authentication and permission. So authentication is the
    # mechanism by which the authentication happens so this could
    # be cookie authentication or we're going to use is token
    # authentication. And the permissions are the level of access
    # that the user has, so the only permission we're going to add is
    # that the user must be authenticated to use the API they don't
    # have to have any special permissions they just have to be
    # logged in.
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # Finally we need to add a get_object() function to our API view.
    # So typically what would happen with an API view is you would
    # link it to a model and it could retrieve the item and you
    # would retrieve data based models. In this case we're going to
    # just get the model for the logged in user. So we're going to
    # override the get object and we're just going to return the user
    # that is authenticated.
    def get_object(self):
        """
        Retrieve and return authenticated user.
        """
        return self.request.user
        # So when the get_object() is called the request will have the
        # user attached to it because of the 'authentication_classes'.
        # So because we have the 'authentication_classes' that takes
        # care of getting the authenticated user and assigning it to
        # request.