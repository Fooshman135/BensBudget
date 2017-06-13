#!/usr/bin/env python3

"""
Ben Katz coding sample.

This program was written and designed entirely by Ben Katz. It was created as
a personal project, to showcase knowledge of the Python and SQL languages.

It is designed to be executed by a Python 3.6 interpreter (although earlier
versions of Python 3.x might work too) on Mac OS X. It has not been tested on
other operating systems.

This program will create directories and save files at the following location
(and nowhere else):
    ~/Library/Application Support/Bens Budget Program
Please note that the program will exit if it comes across any operating system
errors or file system errors.

This program is a command line based, personal finance budgeting app. It is a
work-in-progress, but its current development stage is sufficient for
demonstration purposes.

Ben Katz can be contacted at BenCKatz@gmail.com.
Thank you for your consideration.
"""

import os
import sqlite3
import glob

# Bash uses ~ to mean the home directory, but Python doesn't know that.
# That's why we use os.path.expanduser() in the following command.
CONFIG_DIRECTORY = os.path.expanduser(
    '~/Library/Application Support/Bens Budget Program')

WHICH_BUDGET_MENU_OPTIONS = ["make a new budget,",
                             "load an existing budget,",
                             "quit the program."
                             ]

MAIN_MENU_OPTIONS = ["go to the category menu,",
                     "go to the transactions menu,",
                     "go to the accounts menu,",
                     "choose a different budget or quit the program."
                     ]

CATEGORY_MENU_OPTIONS = ["see your list of budget categories,",
                         "add a new category,",
                         "delete an existing category,",
                         "return to the main menu."
                         ]

ACCOUNT_MENU_OPTIONS = ["see your list of accounts,",
                        "add a new account,",
                        "delete an existing account,",
                        "return to the main menu."
                        ]

# ____________________________________________________________________________#


class Category:

    total_category_value = 0

    def __init__(self, name, value):
        self.name = name
        self.value = value

    # Are there any class attributes? These would basically be properties
    # of Categories that might change over time.
    # If no class attributes, then use static methods instead of class methods.


    @staticmethod
    def new_category():
        """Prompt the user for a name and then create a category with that
        name."""

        while True:

            name = input_blacklist(
                "\nWhat do you want to call your new category? "
                "Enter a blank line to cancel: ",
                str,
                empty_string_allowed=True
            )

            if name == '':
                # User wants to cancel this decision.
                return
            cur = conn.cursor()
            cur.execute("SELECT name FROM Categories WHERE name=?", (name,))
            check = cur.fetchall()
            if not check:
                # The name which the user entered is not already
                # in the Categories table.
                break
            else:
                print("\nA category already exists with that name. "
                      "Please choose a different name.\n")
                continue

        # Category name has been approved, so now ask for value.
        # Then check to make sure value is less than total account balance.
        # If so, add data to category table in the database.
        # Else, inform user and ask for another value.






        cur.execute('INSERT INTO Categories VALUES(?,0)', (name,))
        cur.close()
        conn.commit()

        print(
            "\nOkay! You added a new category called %s to your list!" % name)


    @staticmethod
    def delete_category():
        """Present user with list of existing categories, then delete
        the one corresponding to the user's selection."""

        # TODO: Transfer category value to "unbudgeted total" category.
        # TODO: Determine how to handle transactions which refer to the deleted category.

        num_categories = 0
        category_dict = {}

        cur = conn.cursor()
        cur.execute("SELECT name FROM Categories")

        while True:
            try:
                category_dict[num_categories + 1] = cur.fetchone()[0]
            except TypeError:
                # cur.fetchone() returns None at the end of the query,
                # which is non-subscriptable.
                if num_categories == 0:
                    print(
                        "\nYou have no categories! You should make some!")
                break
            else:
                if num_categories == 0:
                    print("\nWhich category do you want to delete?")
                num_categories += 1
                print("\t%s)" % num_categories,
                      category_dict[num_categories])

        if num_categories > 0:
            choice_number = user_input_with_error_check_whitelist(
                "Enter the number in front of the category you wish to "
                "delete,"
                " or enter 0 to cancel: ",
                range(num_categories + 1),
                False,
                True
            )
            if choice_number > 0:
                cur.execute("DELETE FROM Categories WHERE name=?",
                            (category_dict[choice_number],))
                conn.commit()
                print("\nYou have successfully deleted %s from your"
                      " list of categories." % category_dict[
                          choice_number])

        cur.close()


    @staticmethod
    def display_categories():
        """Query the names of the user's categories and present them
        in a vertical list."""

        cur = conn.cursor()
        cur.execute("SELECT name FROM Categories")
        num_categories = 0
        while True:
            try:
                next_category = cur.fetchone()[0]
            except TypeError:
                # cur.fetchone() returns None at the end of the query,
                # which is non-subscriptable.
                if num_categories == 0:
                    # The Accounts table contains no data
                    print("\nYou have no categories! You should make some!")
                break
            else:
                if num_categories == 0:
                    print("\nHere are your categories:")
                print("\t", next_category)
                num_categories += 1

        cur.close()


    def update_category_value(self):
        """Given a Category instance, allow user to update the instance's
         value."""

        # First, show the user what the category's value currently is.
        # Then prompt for new value (specify addition or replacement).
        # Then update the category's value, and update total_category_value.

        # Also, how/when is this method called? The user needs to select a
        # category before this function is called. Maybe have another
        # function that handles the selection of which category?

        cur = conn.cursor()
        cur.execute("SELECT value FROM Categories WHERE name=?", (self.name,))
        self.value = cur.fetchone()[0]

        output = "Your {} category currently has a value of {}.".format(
            self.name,
            self.value)
        print(output)
        output = "Your unassigned total account balance is {}".format(
            Account.total_account_balance)
        print(output)
        print("Select an amount to add to the category's value "
              "(negative amounts will be subtracted from the value):")


    @staticmethod
    def menu_for_categories():
        """Provide user with information regarding the category menu then
        direct them to the appropriate functions."""

        print("\n~~You are now in the categories menu.~~")
        while True:
            choice = recite_menu_options(CATEGORY_MENU_OPTIONS)
            if choice == 1:
                Category.display_categories()
            elif choice == 2:
                Category.new_category()
            elif choice == 3:
                Category.delete_category()
            elif choice == 4:
                break

# ____________________________________________________________________________#


class Transaction:

    def __init__(self, amount, payee, category, memo, account, date, UID):
        self.amount = amount
        self.payee = payee
        self.category = category
        self.memo = memo
        self.account = account
        self.date = date
        self.UID = UID


    @staticmethod
    def menu_for_transactions():
        """Provide user with information regarding the transactions menu then
         direct them to the appropriate functions."""

        pass
        # TODO: Build out transactions functions.

# ____________________________________________________________________________#


class Account:

    total_account_balance = 0

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance


    @classmethod
    def new_account(cls):
        """Prompt the user for a name and a number, then create an account
         with that name and balance."""

        while True:
            name = input_blacklist(
                "\nWhat do you want to call your new account?"
                " Enter a blank line to cancel: ",
                str,
                empty_string_allowed=True
            )

            if name == '':
                # User wants to cancel this decision.
                return
            cur = conn.cursor()
            cur.execute("SELECT name FROM Accounts WHERE name=?", (name,))
            check = cur.fetchall()
            # Returns an empty list if the user-supplied name doesn't
            # appear in the Accounts table
            if not check:
                # The name which the user entered is not in the Accounts table.
                break
            else:
                print("\nAn account already exists with that name. "
                      "Please choose a different name.\n")
                continue

        # Now that the name is accepted, prompt the user to add
        # a starting account balance.
        balance = input_blacklist(
            "Please enter a starting account balance (must be non-negative): ",
            float,
            num_lb=0
        )

        # Balance is valid, but may have extra decimal places (beyond 2).
        balance = round(balance,2)

        # Account name and balance have been approved, so add them to the
        # accounts table in the database.
        cur.execute('INSERT INTO Accounts VALUES(?,?)', (name, balance))
        cur.close()
        conn.commit()

        # Finally, update the class attribute for total account balance.
        cls.total_account_balance += balance

        print("\nOkay! You added a new account called %s to your list!" % name)


    @classmethod
    def delete_account(cls):
        """Present user with list of existing accounts, then delete the one
         corresponding to the user's selection."""

        # TODO: Determine how to handle transactions which refer to the deleted account.
        # TODO: Only let users delete accounts with zero transactions (prompt them to handle those transactions themselves).

        num_accounts = 0
        # account_dict maps the user-supplied integer to an account record.
        account_dict = {}

        cur = conn.cursor()
        cur.execute("SELECT name FROM Accounts")

        while True:
            try:
                account_dict[num_accounts + 1] = cur.fetchone()[0]
            except TypeError:
                # cur.fetchone() returns None at the end of the query,
                # which is non-subscriptable.
                if num_accounts == 0:
                    print("\nYou have no accounts! You should add some!")
                break
            else:
                if num_accounts == 0:
                    print("\nWhich account do you want to delete?")
                num_accounts += 1
                print("\t%s)" % num_accounts, account_dict[num_accounts])

        if num_accounts > 0:
            choice_number = user_input_with_error_check_whitelist(
                "Enter the number in front of the account you wish to delete,"
                " or enter 0 to cancel: ",
                range(num_accounts + 1),
                False,
                True
            )
            if choice_number > 0:
                # Update class attribute before deleting record from table.
                cur.execute("SELECT balance FROM Accounts WHERE name=?",
                            (account_dict[choice_number],))
                cls.total_account_balance -= cur.fetchall()[0][0]

                # Now okay to delete record.
                cur.execute("DELETE FROM Accounts WHERE name=?",
                            (account_dict[choice_number],))
                conn.commit()

                print("\nYou have successfully deleted %s from your list"
                      " of accounts." % account_dict[choice_number])

        cur.close()


    @classmethod
    def display_accounts(cls):
        """Query the names and balances of the user's accounts and present them
        in a vertical list."""

        # TODO: Use with statement to open and close the cursor.
        # TODO: Fix floating point errors for large numbers. Use "decimal" module?

        # Here is how to interpret the string format specifiers below:
        # Let's look at {:>#{pad2},.2f} as an example.
        # The ':' means the following characters are 'format_specs'.
        # The '>' means right-justified.
        # The '#' means alternate form. Here, it keeps trailing zeros.
        # The '{pad2}' is a nested format specifier.
        #   Here it simply contains a variable.
        # The ',' groups the digits into sets of 3, separated by a comma.
        # The '.2f' means show two digits after the decimal place.
        #   Note that the 'f' in '.2f' specifies fixed point.

        # Determine the length of the longest string in the name column of the
        # Accounts table (for formatting purposes).
        cur = conn.cursor()
        cur.execute("SELECT MAX(LENGTH(name)) FROM Accounts")
        max_name_length = cur.fetchone()[0]
        if max_name_length is None:
            # The Accounts table contains no data
            print("\nYou have no accounts! You should add some!")
            cur.close()
            return

        # Determine the length of the longest number in the balance column of
        # the Accounts table (for formatting purposes).
        cur.execute("SELECT MAX(balance) FROM Accounts")
        max_balance_length = len("{:#,.2f}".format(cur.fetchone()[0]))

        # Retrieve the name and balance attributes from the Account table.
        cur.execute("SELECT name, balance FROM Accounts")

        print("\nHere are your accounts and their balances:")
        while True:
            try:
                next_account_name, next_account_balance = cur.fetchone()
            except TypeError:
                # cur.fetchone() returns None at the end of the query,
                # which is not iterable (producing a TypeError).
                break
            else:
                output = "{:{pad1}}    $ {:>#{pad2},.2f}".format(
                    next_account_name,
                    next_account_balance,
                    pad1=max(max_name_length, 13),
                    pad2=max_balance_length)
                print("\t%s" % output)

        # Finally, display the total account balance.
        final_line_output = "{:{pad1}}    $ {:>#{pad2},.2f}".format(
            "Total Balance",
            cls.total_account_balance,
            pad1=max(max_name_length, 13),
            pad2=max_balance_length)
        print("\t%s" % ("-"*len(final_line_output)))
        print("\t%s" % final_line_output)

        cur.close()


    @staticmethod
    def menu_for_accounts():
        """Provide user with information regarding the accounts menu then
        direct them to the appropriate functions."""

        print("\n~~You are now in the accounts menu.~~")

        while True:

            choice = recite_menu_options(ACCOUNT_MENU_OPTIONS)

            if choice == 1:
                Account.display_accounts()

            elif choice == 2:
                Account.new_account()

            elif choice == 3:
                Account.delete_account()

            elif choice == 4:
                break

# ____________________________________________________________________________#


def main():
    """Main menu of the program, acting as 'central hub' through which users
    navigate to get to all other parts."""

    global conn
    global user_budgets

    # All files affiliated with this program will be located at the path
    # stored in CONFIG_DIRECTORY.
    if not os.path.exists(CONFIG_DIRECTORY):
        os.makedirs(CONFIG_DIRECTORY)

    user_budgets = os.path.join(CONFIG_DIRECTORY, "User Budgets")
    if not os.path.exists(user_budgets):
        os.makedirs(user_budgets)

    # Here is where the user experience begins:
    print("\nWelcome to Ben's Budget Program!")
    while True:
        conn = which_budget()

        # Now that a budget is selected, update the total account balance.
        cur = conn.cursor()
        cur.execute("SELECT SUM(balance) FROM Accounts")
        Account.total_account_balance = cur.fetchall()[0][0]
        cur.close()
        # A brand new budget has no data, so cur.fetchall returns None.
        if Account.total_account_balance == None:
            Account.total_account_balance = 0

        while True:
            choice = recite_menu_options(MAIN_MENU_OPTIONS)
            if choice == 1:
                Category.menu_for_categories()
            elif choice == 2:
                Transaction.menu_for_transactions()
            elif choice == 3:
                Account.menu_for_accounts()
            elif choice == 4:
                print("\n~~"
                      "You are now returning to the budget selection menu.~~")
                conn.close()
                break
            print("\n~~You are now returning to the main menu.~~")

# ____________________________________________________________________________#


def which_budget():
    """Top-level menu, determines which budget (database) to connect to"""

    # TODO: Make filenames distinct from user-supplied budget names. Then no need to limit user's input!
    # TODO: Provide option to delete an existing budget.

    while True:
        choice = recite_menu_options(WHICH_BUDGET_MENU_OPTIONS)
        if choice == 1:
            # The user wants to create a brand new budget.
            while True:
                budget_name = input_blacklist(
                    "\nPlease choose a name for your new budget, "
                    "or enter a blank line to cancel: ",
                    str,
                    str_bad_chars=('.', ':', '/'),
                    str_bad_chars_positions=(0, None, None),
                    empty_string_allowed=True
                )

                # Now confirm that there isn't an existing budget that
                # already has that name.
                if os.path.isfile(os.path.join(
                        user_budgets, budget_name + '.db')):
                    print("\nA budget already exists with that name. "
                          "Please enter a different name.")
                else:
                    break
            if budget_name == "":
                # User wants to cancel. Loop to top of this function.
                continue
            # Name has been approved, proceed with setting up new database
            # and connecting to it.
            connection = sqlite3.connect(
                os.path.join(user_budgets, budget_name + '.db'))
            cur = connection.cursor()
            cur.execute('CREATE TABLE Categories('
                        'name TEXT,'
                        'value REAL)'
                        )
            cur.execute('CREATE TABLE Accounts('
                        'name TEXT,'
                        'balance REAL)'
                        )
            cur.execute('CREATE TABLE Transactions('
                        'amount REAL,'
                        'payee TEXT,'
                        'category TEXT,'
                        'memo TEXT,'
                        'account TEXT,'
                        'date TEXT,'
                        'UID INTEGER)'
                        )
            cur.close()
            connection.commit()
            print("\nGreat! You have created a brand new budget called %s."
                  % budget_name)
            break

        if choice == 2:
            # The user wants to load an existing budget.
            list_of_budgets = glob.glob(
                "%s/*.db" % user_budgets)  # Pull up list of available budgets
            if len(list_of_budgets) == 0:
                print("\nThere are no existing budgets. "
                      "You should make a new one!")
            else:
                print("\nWhich budget would you like to load?")
                for i in range(len(list_of_budgets)):
                    print("\t%d)" % (i + 1), os.path.splitext(
                        os.path.basename(list_of_budgets[i]))[0])
                budget_number = user_input_with_error_check_whitelist(
                    "Enter the number in front of the budget you wish to load,"
                    " or enter 0 to cancel: ",
                    range(len(list_of_budgets) + 1),
                    False,
                    True
                )
                if budget_number == 0:
                    # User wants to cancel. Loop to top of this function.
                    continue
                else:
                    # Load the budget that corresponds to the number
                    # the user entered.
                    connection = sqlite3.connect(
                        list_of_budgets[budget_number - 1])
                    print("\nBudget loaded: %s" % os.path.splitext(
                        os.path.basename(list_of_budgets[
                                             budget_number - 1]))[0])
                    break

        if choice == 3:
            # Quit the program!
            exit_program()

    return connection

# ____________________________________________________________________________#


def recite_menu_options(list_of_options):
    """Present user with a series of options and make them choose one."""

    print("\nWhat would you like to do?")
    for i in range(len(list_of_options)):
        print("Press %d to %s" % (i + 1, list_of_options[i]))

    return user_input_with_error_check_whitelist(
        "Enter your choice here: ",
        range(1, len(list_of_options)+1),
        False,
        True
    )

# ____________________________________________________________________________#


def user_input_with_error_check_whitelist(
        prompt_message, valid_set, upper_only, integer):
    """Receive user input and confirm that it is in the whitelist and is
     the proper type."""

    # TODO: Change input parameters to ask for expected input TYPE, rather than upper_only, integer, whatever.
    # TODO: Currently this function is only called when input should be integers, not strings. upper_only necessary?

    while True:
        user_input = input(prompt_message)
        if upper_only:
            try:
                user_input = user_input.upper()
            except AttributeError:
                print("\nInvalid entry, please try again.\n")
                continue
        elif integer:
            try:
                user_input = int(user_input)
            except ValueError:
                print("\nInvalid entry, please try again.\n")
                continue
        if user_input in valid_set:
            break
        else:
            print("\nInvalid entry, please try again.\n")

    return user_input

# ____________________________________________________________________________#


def input_blacklist(
        prompt,
        input_type,
        num_lb=float('-inf'),
        num_ub=float('inf'),
        str_bad_chars=None,
        str_bad_chars_positions=None,
        empty_string_allowed=False
        ):

    """
    Receive user input and confirm that it's not in the blacklist.

    :param prompt: The message that the user sees when prompted for input.
    :param input_type: The type of input that the user should enter.
    :param num_lb: The lower bound (inclusive) of input, if numerical.
    :param num_ub: The upper bound (inclusive) of input, if numerical.
    :param str_bad_chars: Any characters which are forbidden, if input is text.
    :param str_bad_chars_positions: The corresponding positions of the
            characters in str_bad_chars. If no position is specified for a
            character, this value is 'None'.
    :param empty_string_allowed: Flag to specify whether the empty string
            is acceptable input.
    :return: The user input, once confirmed that it's acceptable.
    """

    while True:

        error_output = None

        user_input = input(prompt).strip()
        # user_input is a string.

        # First check for empty string.
        if user_input == '':
            # Determine if empty string is acceptable.
            if empty_string_allowed:
                # User input is good to go.
                break
            else:
                print("\nInvalid entry, please try again.\n")
                continue

        if input_type is str:

            if str_bad_chars is None:
                # No forbidden characters, so user input is good to go.
                break

            for i in range(len(str_bad_chars)):
                # Make sure each member of str_bad_chars doesn't
                # appear in the input at the wrong position.
                if str_bad_chars_positions[i] is None:
                    # str_bad_chars[i] is not allowed anywhere within string.
                    if str_bad_chars[i] in user_input:
                        # Reject input.
                        error_output = "Invalid entry, cannot contain" \
                                       " {}".format(
                                        str_bad_chars[i]
                        )
                        break

                else:
                    # str_bad_chars[i] is not allowed at the specific location
                    # specified by str_bad_chars_positions[i], but allowed
                    # elsewhere.
                    if str_bad_chars[i] in user_input[
                            str_bad_chars_positions[i]]:
                        # Reject input.
                        error_output = "Invalid entry, character at position" \
                                       " {} cannot be '{}'".format(
                                        str_bad_chars_positions[i],
                                        str_bad_chars[i]
                        )
                        break

            if error_output is not None:
                print("\n%s" % error_output)
                continue
            else:
                # User input is good to go.
                break

        else:
            # input_type is either int or float.

            if input_type is int:
                try:
                    user_input = int(user_input)
                except ValueError:
                    print("\nInvalid entry, please try again.\n")
                    continue

            elif input_type is float:
                try:
                    user_input = float(user_input)
                except ValueError:
                    print("\nInvalid entry, please try again.\n")
                    continue

            # Now check to make sure user_input is in range.
            if (user_input < num_lb) or (user_input > num_ub):
                error_output = "Invalid entry, must be between {} and" \
                         " {} (inclusive).\n".format(
                            num_lb,
                            num_ub
                )
                print("\n%s" % error_output)
                continue

            # user_input is good to go.
            break

    return user_input

# ____________________________________________________________________________#


def exit_program():
    """Exit the program gracefully (with exit code 0)."""

    print("\nThanks for using Ben's Budget Program. See you later!")
    raise SystemExit

# ____________________________________________________________________________#


if __name__ == "__main__":
    main()

"""
Here are ideas of next steps and features:
-Add a Delete Existing Budget option to the main menu.2

-Implement some sense of time. Consider making the time frame variable, based on user input.
-Expand the display_categories() function to show more than just the category names. Ideas for expansion include:
    -Showing a table with category names as rows, and other attributes (such as budget_value) as columns.
    -Similar to YNAB, show total transactions for the given time period.
-Build out the transactions section of the program.
-Consider making a function that prompts the user "Press enter to continue" and doesn't continue until they do.
    -Call this function every time they enter some input (after the immediate results of their input is shown to them.
    -For example:
        -the program prompts them for a menu item,
        -they enter a number,
        -the program tells them what the immediate result of their input is,
        -the program calls this press_enter_to_continue function
-Python does not have a switch statement, so the current use of if/elif/else will have to do.
-Allow users to create their own subsets of categories (distinct from the idea of super-categories).
    -Allow users to see spending patterns/trends in just that subset.
-Use regular expressions to check user input (and make sure it's valid).
-Regarding the user_input_with_error_check_whitelist() function, in order to make it universal we need to consider cases where:
    1) The input needs to be within a set (valid_set);
    2) The input needs to meet a certain criteria (such as input > 0);
    3) The input needs to take into consideration the database (such as not be a duplicate, or must be a duplicate, or whatever);
    4) The input should be converted from string to some other type (int, float, bool?).
    Ideally, any time the program asks for user input, this function (or the blacklist function) should be called.
    If it seems like there's a special case where user input should be requested directly, then we probably need to expand this function!
        For example, the function new_account() currently requests input directly. Opportunity to change this?
    If I need to create, for example, the set of all positive floats (option #1 instead of #2 above), then I can create a subclass
        of the set class, and define its __contains__(self, item) method so that it returns True when item >= 0.
-Implementing classes and OOP instead of procedural programming:
    Make a Category class, an Account class, and a Transaction class.
        And then each category, account, and transaction will be instances of these classes (and therefore will be objects).
        But how do I do this using the SQL database?
            Maybe whenever I read data from the database into memory, it gets stored as an object?
                YES! YES. Danny confirmed that this is an extremely common way of handling data that is read into memory from a database.
    Make a Menu class!
        And then each menu can be its own object, with its own list of options stored as an attribute.
        The user's input choice should be stored as an attribute.
        But how can I avoid the if...elif...elif... chains in the functions that call recite_menu_options() ?
    Once I implement classes in my code, it might make sense to incorporate an Object-Relational Mapping (ORM) to replace my SQL commands.

Discussion with Dad on 11/26/16:
-Implement config files
    config files save user preferences ("configurations")
    Module: configparser
    ~/Library/Application Support/Bens Budget Program
    

"""