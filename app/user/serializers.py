from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user object.
    """
    class Meta:
        model = get_user_model()
        # This above line will give us the model, which we will
        # serialize in this class.

        # Next you can specify the fields that you want to include
        # in serializer so these are the fields that are going to
        # be converted to and from json when we make our HTTP POST
        # request. So those basically are the fields that we want
        # to make accessible in the API either to read or write.
        fields = ('email', 'password', 'name')
        # These are the three fields that we're going to accept
        # when we create users.

        # So finally we're going to add something called extra
        # keyword args and what this does is it allows us to configure
        # a few extra settings in our model serializer and what we're
        # going to use this for is to ensure that the password is write
        # only and that the minimum required length is 5 characters.
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
                }
            }

    def create(self, validated_data):
        """
        Create a new user with an encrypted password and
        return it.
        """
        return get_user_model().objects.create_user(**validated_data)
