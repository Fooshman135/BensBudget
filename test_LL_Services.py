import unittest
import LL_Services
import sys
import Models
from datetime import date as dt


class Test_LL_Services(unittest.TestCase):


    def test_int_validate(self):
        """Tests the function LL_Services.int_validate()"""

        # Case: Input is in range
        result = LL_Services.int_validate('5', 3, 7)
        self.assertTrue(result)

        # Case: Input is out of range
        result = LL_Services.int_validate('5', 1, 4)
        self.assertFalse(result)

        # Case: Input has non-numeric characters
        result = LL_Services.int_validate('pizza', 3, 7)
        self.assertFalse(result)

        # Case: Input resembles a floating point number
        result = LL_Services.int_validate('5.0', 3, 7)
        self.assertFalse(result)

    # ________________________________________________________________________#
    def test_float_validate(self):
        """Tests the function LL_Services.float_validate()"""

        # Case: Input is in range
        result = LL_Services.float_validate('23.40', 19.54, 345.67)
        self.assertTrue(result)

        # Case: Input is out of range
        result = LL_Services.float_validate('400.00', 19.54, 345.67)
        self.assertFalse(result)

        # Case: Input has non-numeric characters
        result = LL_Services.float_validate('pizza', 19.54, 345.67)
        self.assertFalse(result)

        # Case: Input resembles an integer
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


    # ________________________________________________________________________#
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
        result = LL_Services.date_validate('Be/nj/amin')
        self.assertFalse(result)


    # ________________________________________________________________________#
    def test_is_string_valid_filename(self):
        """Tests the function LL_Services.is_string_valid_filename()"""

        # Case: Input is a valid filename with no '.', ':', or '/' anywhere.
        result = LL_Services.is_string_valid_filename("Ben's Budget")
        self.assertTrue(result)

        # Case: Input contains '.' as its first character.
        result = LL_Services.is_string_valid_filename(".Ben's Budget")
        self.assertFalse(result)

        # Case: Input contains '.' somewhere other than the first character.
        result = LL_Services.is_string_valid_filename("Ben's.Budget")
        self.assertTrue(result)

        # Case: Input contains ':' in the middle of the string.
        result = LL_Services.is_string_valid_filename("Ben's:Budget")
        self.assertFalse(result)

        # Case: Input contains ':' in the beginning of the string.
        result = LL_Services.is_string_valid_filename(":Ben's Budget")
        self.assertFalse(result)

        # Case: Input contains ':' at the end of the string.
        result = LL_Services.is_string_valid_filename("Ben's Budget:")
        self.assertFalse(result)

        # Case: Input contains '/' in the middle of the string.
        result = LL_Services.is_string_valid_filename("Ben's/Budget")
        self.assertFalse(result)

        # Case: Input contains '/' in the beginning of the string.
        result = LL_Services.is_string_valid_filename("/Ben's Budget")
        self.assertFalse(result)

        # Case: Input contains '/' at the end of the string.
        result = LL_Services.is_string_valid_filename("Ben's Budget/")
        self.assertFalse(result)

        # Case: Input contains '.' in the beginning and
        # ':' in the middle of the string.
        result = LL_Services.is_string_valid_filename(".Ben's:Budget")
        self.assertFalse(result)

        # Case: Input contains '.' and nothing else.
        result = LL_Services.is_string_valid_filename(".")
        self.assertFalse(result)

        # Case: Input contains ':' and nothing else.
        result = LL_Services.is_string_valid_filename(":")
        self.assertFalse(result)

        # Case: Input contains '/' and nothing else.
        result = LL_Services.is_string_valid_filename("/")
        self.assertFalse(result)

        # Case: Input is the empty string.
        result = LL_Services.is_string_valid_filename("")
        self.assertFalse(result)

    # ________________________________________________________________________#
    def test_find_max_of_each_obj_attr(self):
        """Tests the function LL_Services.find_max_of_each_column()"""

        # Case: Input is a list of Category objects
        table = [
            Models.Category("Eating Out", -300.00),
            Models.Category("Groceries", -150.00),
            Models.Category("Transportation", -100.23),
            Models.Category("Rent", -1500.00),
            Models.Category("This is a long category name!", 10.00),
            Models.Category("w", -123456.78),

        ]
        expected_output = {"name": 29, "value": 12}
        result = LL_Services.find_max_of_each_obj_attr(table)
        self.assertEqual(result, expected_output)

        # Case: Input is a list of Transaction objects
        table = [
            Models.Transaction(
                1,
                "Long account name",
                "Eating Out",
                15.89,
                "Chipotle",
                dt(2016, 3, 14),
                "Delicious burrito!"
            ),
            Models.Transaction(
                2,
                "Savings",
                "Rent",
                1550.00,
                "Landlord",
                dt(2017, 8, 1),
                "August rent"
            ),
            Models.Transaction(
                3,
                "Cash",
                "This is a very long category name!",
                5.00,
                "friend",
                dt(2016, 3, 15),
                None
            ),
            Models.Transaction(
                4,
                "Checking",
                "Eating Out",
                15.89,
                "This is a very long payee name!",
                dt(2016, 3, 14),
                "This is a very long memo! It just keeps on going and going!"
            ),
        ]
        expected_output = {
            "uid": 1,
            "account": 17,
            "category": 34,
            "amount": 9,
            "payee": 31,
            "date": 10,
            "memo": 59
        }
        result = LL_Services.find_max_of_each_obj_attr(table)
        self.assertEqual(result, expected_output)

        # Case: Input is a list of Account objects
        table = [
            Models.Account("Checking", 3000.00),
            Models.Account("Savings", 5000.35),
            Models.Account("Long account name", 100.00),
            Models.Account("Hi", 1234567.89),
        ]
        expected_output = {"name": 17, "balance": 13}
        result = LL_Services.find_max_of_each_obj_attr(table)
        self.assertEqual(result, expected_output)

        # Case: Input is empty list.
        table = []
        expected_output = {}
        result = LL_Services.find_max_of_each_obj_attr(table)
        self.assertEqual(result, expected_output)

        # Case: Input contains multiple object types.
        table = [
            Models.Category("Eating Out", 30.00),
            Models.Transaction(
                34,
                "Checking",
                "Rent",
                7.78,
                "Starbucks",
                dt(2015, 4, 25),
                None
            ),
            Models.Account("Checking", 4000.00)
        ]
        with self.assertRaises(KeyError):
            LL_Services.find_max_of_each_obj_attr(table)


# ____________________________________________________________________________#
if __name__ == '__main__':
    unittest.main()