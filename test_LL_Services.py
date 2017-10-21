import unittest
import LL_Services
import sys


class Test_LL_Services(unittest.TestCase):


    def test_int_validate(self):
        """Tests the function LL_Services.int_validate()"""

        # Case: Input is in range
        result = LL_Services.int_validate('5', 3, 7)
        self.assertTrue(result)

        # Case: Input is out of range
        result = LL_Services.int_validate('5', 1, 4)
        self.assertFalse(result)

        # Case: Input is of type str but has non-numeric characters
        result = LL_Services.int_validate('pizza', 3, 7)
        self.assertFalse(result)

        # Case: Input is of type string but resembles a floating point number
        result = LL_Services.int_validate('5.0', 3, 7)
        self.assertFalse(result)


    def test_float_validate(self):
        """Tests the function LL_Services.float_validate()"""

        # Case: Input is in range
        result = LL_Services.float_validate('23.40', 19.54, 345.67)
        self.assertTrue(result)

        # Case: Input is out of range
        result = LL_Services.float_validate('400.00', 19.54, 345.67)
        self.assertFalse(result)

        # Case: Input is of type string but has non-numeric characters
        result = LL_Services.float_validate('pizza', 19.54, 345.67)
        self.assertFalse(result)

        # Case: Input is of type string but resembles an integer
        result = LL_Services.float_validate('21', 19.54, 345.67)
        self.assertTrue(result)

        # Case: Input is the negative 0 float
        result = LL_Services.float_validate('-0.00', -19.54, 345.67)
        self.assertTrue(result)

        # Case: No bounds are given.
        result = LL_Services.float_validate('23.40')
        self.assertTrue(result)

        # Case: User enters 'inf' as input
        result = LL_Services.float_validate('inf')
        self.assertFalse(result)

        # Case: User enters '-inf' as input
        result = LL_Services.float_validate('-inf')
        self.assertFalse(result)


    def test_date_validate(self):
        """Tests the function LL_Services.date_validate()"""

        # Case: User enters a real date that doesn't precede 01/01/1900
        result = LL_Services.date_validate('07/09/1990')
        self.assertTrue(result)

        # Case: User enters a real date that does precede 01/01/1900
        result = LL_Services.date_validate('07/09/1890')
        if sys.version_info < (3,0):
            self.assertFalse(result)    # When interpreter is Python 2.x
        else:
            self.assertTrue(result)     # When interpreter is Python 3.x

        # Case: User enters a fake date
        result = LL_Services.date_validate('07/35/1990')
        self.assertFalse(result)

        # Case: User enters a string that isn't in MM/DD/YYYY format.
        result = LL_Services.date_validate('pi/zz/a!')
        self.assertFalse(result)


    def test_is_string_valid_filename(self):
        """Tests the function LL_Services.is_string_valid_filename()"""

        # Case: Input is a valid filename.
        result = LL_Services.is_string_valid_filename("Ben's Budget")
        self.assertTrue(result)

        # Case: Input contains '.' as its first character.
        result = LL_Services.is_string_valid_filename(".Ben's Budget")
        self.assertFalse(result)

        # Case: Input contains ':' in the middle of the string.
        result = LL_Services.is_string_valid_filename("Ben's:Budget")
        self.assertFalse(result)

        # Case: Input contains '/' in the middle of the string.
        result = LL_Services.is_string_valid_filename("Ben's/Budget")
        self.assertFalse(result)

        # Case: Input contains '.' in the beginning and
        # ':' in the middle of the string.
        result = LL_Services.is_string_valid_filename(".Ben's:Budget")
        self.assertFalse(result)

        # Case: Input contains '.' somewhere other than the first character.
        result = LL_Services.is_string_valid_filename("Ben's.Budget")
        self.assertTrue(result)



if __name__ == '__main__':
    unittest.main()