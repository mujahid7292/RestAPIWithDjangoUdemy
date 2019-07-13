from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin

# Create a model manager class. As our model name is 'user',
# So, model manager class name will be 'UserModel'
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        This function creates and saves a new user.

        email = User email address.
        password = User provided password. Default is none.
        **extra_fields = This will allow to add new field when
                    we create user. Such as user phone number
                    etc.

        return
        This function return a newly created user.
        """
        if not email:
            raise ValueError('User must provide email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)

        # 'using=self._db' = This will help us to support
        # multiple database.

        return user

# Now we will create our model class

class User(AbstractBaseUser, PermissionsMixin):
    """
    This is custom user model, that supports email base
    user authentication rather than name base user 
    authentication.
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # In django by default USERNAME_FIELD = 'username', but
    # in this app we are stting it to be email.