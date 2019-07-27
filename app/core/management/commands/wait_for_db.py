import time
from django.db import connections
# we can use 'connection' to test the database connection,
# whether it is available or not.
from django.db.utils import OperationalError
# This error is thrown by Django, when database is not
# available.
from django.core.management.base import BaseCommand
# And finally we're importing base command which is the class
# that we need to build on in order to create our custom command class.


class Command(BaseCommand):
    """
    This is a Django command, to pause execution until database is
    available.
    """

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database........')
        db_conn = None
        while not db_conn:
            # Means while db_conn = None, execution will enter
            # this loop.
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting for 1 sec.')
                time.sleep(1)   # Our code will pause for 1 sec
        self.stdout.write(self.style.SUCCESS('Database is available!!!'))
