from unittest.mock import patch
# This above import is going to allow us to 
# mock the behaviour of the Django get_database() function.
# What this will do is, we can basically simulate the database 
# being available and not being available for when we test our
# command.

from django.core.management import call_command

from django.db.utils import OperationalError
# OperationalError is an error that Django throws when the database is 
# unavailable and we're going to use this error to simulator database as 
# being available or not.

from django.test import TestCase


class CommandTests(TestCase):
    """
    This class is resposible for doing all the test associated with
    command.
    """

    # The first function we're going to create is simply going to test,
    # what happens when we call our command and the database is already
    # available.
    def test_wait_for_db_ready(self):
        """
        Test waiting for db, when db is available.
        """
        # So to set up our test here we need to simulate the behaviour of
        # Django, When the database is available. Our management command is 
        # going to basically try and retrieve the database connection from
        # Django. And it's going to check if when we try and retrieve it,
        # it retrieved an operational error or not. So if it retrieves an
        # operational error then a database is not available. If an operational
        # error is not thrown then the database is available and the comman
        # will continue.