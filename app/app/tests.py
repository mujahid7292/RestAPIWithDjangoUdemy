from django.test import TestCase
# This above import will help us to test our django app.

#Next we will import function which we want to test.
from app.calc import add

#Now we will create a classs which will test our calc
#class.
class CalcTest(TestCase):
    #We are going to inherit this class from TestCase

    # Now we will create test function to test the add
    #function.

    def test_add_numbers(self):
        """
        Test that two numbers are added together.
        """
        self.assertEqual(add(3,8),11)