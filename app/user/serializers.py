from django.contrib.auth import get_user_model, authenticate
# authenticate = it's a Django helper command for working with
# the Django authentication system. So you simply pass in the
# username and password and you can authenticate a request.
from django.utils.translation import ugettext_lazy as _
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


class AuthTokenSerializer(serializers.Serializer):
        """
        Serializer for the user authentication object.
        """
        email = serializers.CharField()
        password = serializers.CharField(
            style={'input_type': 'password'},
            trim_whitespace=False
        )

        # This validate function is called when we validate our serializer.
        # This validation function will check whether inputs are all correct,
        # like whether email is CharField etc And as part of the validation
        # function we are also going to validate that the authentication
        # credentials are correct.
        def validate(self, attrs):
            """
            Validate and authenticate the user.
            """
            # attrs = This is a dictionary, which contain our passed in
            # email and password. So this attrs parameter here is basically
            # just every field that makes up our serializer. So any field
            # that makes up a serializer, it will get passed into the
            # validate function here as this dictionary and then we can
            # retrieve the fields via this attributes and we can
            # then validate whether we want to pass this validation or we want
            # to fail the validation. Now we will rtrieve those email and
            # password.
            email = attrs.get('email')
            password = attrs.get('password')

            # Now we will authenticate our request.
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )

            # If our above authentication fail, then
            if not user:
                # Means our authentication failed.
                msg = _('Unable to authenticate with provided credentials')
                raise serializers.ValidationError(
                    msg,
                    code='authentication'
                )
            # Now we will return our 'attrs' dictionary by
            # inserting our authenticated user.
            attrs['user'] = user
            return attrs
