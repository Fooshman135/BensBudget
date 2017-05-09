#!/usr/bin/env python
import os
import sqlite3
import glob

# __________________________________________________________________________________________________#


def display_categories():
    """Query the names of the user's categories and present them in a vertical list."""
    cur = conn.cursor()
    cur.execute("SELECT name FROM Categories")
    num_categories = 0
    while True:
        try:
            next_category = cur.fetchone()[0]
        except TypeError:   # cur.fetchone() returns None at the end of the query, which is non-subscriptable.
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

# __________________________________________________________________________________________________#


def new_category():
    """Prompt the user for a name and then create a category with that name."""
    while True:
        name = input("\nWhat do you want to call your new category? Enter a blank line to cancel: ").strip()
        if name == '':
            # User wants to cancel this decision.
            return
        cur = conn.cursor()
        cur.execute("SELECT name FROM Categories WHERE name=?", (name,))
        check = cur.fetchall()
        if not check:
            # The name which the user entered is not already in the Categories table.
            break
        else:
            print("\nA category already exists with that name. Please choose a different name.\n")
            continue

    # Category name has been approved, so add it to the category table in the database.
    cur.execute('INSERT INTO Categories VALUES(?,0)', (name,))
    cur.close()
    conn.commit()

    print("\nOkay! You added a new category called %s to your list!" % name)

# __________________________________________________________________________________________________#


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

# __________________________________________________________________________________________________#


def menu_for_categories():
    """Provide user with information regarding the category menu then direct them to the appropriate functions."""
    CATEGORY_MENU_OPTIONS = ["see your list of budget categories,",
                             "add a new category,",
                             "delete an existing category,",
                             "return to the main menu."
                             ]

    print("\n~~You are now in the categories menu.~~")
    while True:
        choice = recite_menu_options(CATEGORY_MENU_OPTIONS)
        if choice == 1:
            display_categories()
        elif choice == 2:
            new_category()
        elif choice == 3:
            delete_category()
        elif choice == 4:
            break

# __________________________________________________________________________________________________#


def delete_category():
    """Present user with list of existing categories, then delete the one corresponding to the user's selection."""
    # TODO: Transfer category value to "unbudgeted total" category.
    # TODO: Determine how to handle transactions which refer to the deleted category.

    num_categories = 0
    category_dict = {}

    cur = conn.cursor()
    cur.execute("SELECT name FROM Categories")

    while True:
        try:
            category_dict[num_categories + 1] = cur.fetchone()[0]
        except TypeError:   # cur.fetchone() returns None at the end of the query, which is non-subscriptable.
            if num_categories == 0:
                print("\nYou have no categories! You should make some!")
            break
        else:
            if num_categories == 0:
                print("\nWhich category do you want to delete?")
            num_categories += 1
            print("\t%s)" % num_categories, category_dict[num_categories])

    if num_categories > 0:
        choice_number = user_input_with_error_check_whitelist(
            "Enter the number in front of the category you wish to delete, or enter 0 to cancel: ",
            range(num_categories + 1),
            False,
            True
        )
        if choice_number > 0:
            cur.execute("DELETE FROM Categories WHERE name=?", (category_dict[choice_number],))
            conn.commit()
            print("\nYou have successfully deleted %s from your list of categories." % category_dict[choice_number])

    cur.close()

# __________________________________________________________________________________________________#


def menu_for_transactions():
    """Provide user with information regarding the transactions menu then direct them to the appropriate functions."""
    pass
    # TODO: Build out transactions functions.

# __________________________________________________________________________________________________#


def menu_for_accounts():
    """Provide user with information regarding the accounts menu then direct them to the appropriate functions."""
    ACCOUNT_MENU_OPTIONS = ["see your list of accounts,",
                             "add a new account,",
                             "delete an existing account,",
                             "return to the main menu."
                             ]

    print("\n~~You are now in the accounts menu.~~")

    while True:

        choice = recite_menu_options(ACCOUNT_MENU_OPTIONS)

        if choice == 1:
            display_accounts()

        elif choice == 2:
            new_account()

        elif choice == 3:
            delete_account()

        elif choice == 4:
            break

# __________________________________________________________________________________________________#


def display_accounts():
    """Query the names and balances of the user's accounts and present them in a vertical list."""
    # TODO: Show balances as right-justified. Make sure long balances and long names don't clash.
    # TODO: Show total balance (across all accounts) at the bottom.
    # TODO: Use with statement to open and close the cursor.

    # Determine the length of the longest string in the name column of the Accounts table (for formatting purposes).
    cur = conn.cursor()
    cur.execute("SELECT MAX(LENGTH(name)) FROM Accounts")
    max_name_length = cur.fetchone()[0]
    if max_name_length is None:
        # The Accounts table contains no data
        print("\nYou have no accounts! You should add some!")
        cur.close()
        return

    # Retrieve the name and balance attributes from the Account table.
    cur.execute("SELECT name, balance FROM Accounts")
    num_accounts = 0
    while True:
        try:
            next_account_name, next_account_balance = cur.fetchone()
        except TypeError:  # cur.fetchone() returns None at the end of the query, which is not iterable.
            break
        else:
            if num_accounts == 0:
                print("\nHere are your accounts and their balances:")
            # %-*s means print next_account_name, left-justified, and then print spaces until
            #   the total number of characters equals the value of max_name_length.
            # This ensures that the next_account_balance values are lined up properly.
            print("\t%-*s    $%.2f" % (max_name_length, next_account_name, next_account_balance))
            num_accounts += 1

    cur.close()

# __________________________________________________________________________________________________#


def new_account():
    """Prompt the user for a name and a number, then create an account with that name and balance."""
    while True:
        name = input("\nWhat do you want to call your new account? Enter a blank line to cancel: ").strip()
        if name == '':
            # User wants to cancel this decision.
            return
        cur = conn.cursor()
        cur.execute("SELECT name FROM Accounts WHERE name=?", (name,))
        check = cur.fetchall()  # Returns an empty list if the user-supplied name doesn't appear in the Accounts table
        if not check:
            # The name which the user entered is not already in the Accounts table.
            break
        else:
            print("\nAn account already exists with that name. Please choose a different name.\n")
            continue

    # Now that the name is accepted, prompt the user to add a starting account balance.
    while True:
        balance = input("Please enter a starting account balance (must be non-negative): ")
        try:
            balance = float(balance)
        except ValueError:
            print("\nInvalid entry, please try again.\n")
            continue
        else:
            if balance < 0:
                print("\nBalance must be non-negative. Please try again.\n")
                continue
            else:
                break

    # Account name and balance have been approved, so add them to the accounts table in the database.
    cur.execute('INSERT INTO Accounts VALUES(?,?)', (name, balance))
    cur.close()
    conn.commit()

    print("\nOkay! You added a new account called %s to your list!" % name)

# __________________________________________________________________________________________________#


def delete_account():
    """Present user with list of existing accounts, then delete the one corresponding to the user's selection."""
    # TODO: figure out what to do with balance (assuming it's non-zero).
    # TODO: Determine how to handle transactions which refer to the deleted account.
    # TODO: Only let users delete accounts with zero transactions (prompt them to handle those transactions themselves).

    num_accounts = 0
    account_dict = {}

    cur = conn.cursor()
    cur.execute("SELECT name FROM Accounts")

    while True:
        try:
            account_dict[num_accounts + 1] = cur.fetchone()[0]
        except TypeError:   # cur.fetchone() returns None at the end of the query, which is non-subscriptable.
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
            "Enter the number in front of the account you wish to delete, or enter 0 to cancel: ",
            range(num_accounts + 1),
            False,
            True
        )
        if choice_number > 0:
            cur.execute("DELETE FROM Accounts WHERE name=?", (account_dict[choice_number],))
            conn.commit()
            print("\nYou have successfully deleted %s from your list of accounts." % account_dict[choice_number])

    cur.close()

# __________________________________________________________________________________________________#


def user_input_with_error_check_whitelist(prompt_message, valid_set, upper_only, integer):
    """Receive user input and confirm that it is in the whitelist and is the proper type."""
    # TODO: AttributeError raised when upper_only==True and user_input isn't a string.
    # TODO: Change input parameters to ask for expected input TYPE, rather than upper_only, integer, whatever.
    # TODO: Currently this function is only called when input should be integers, not strings. upper_only necessary?
    while True:
        user_input = input(prompt_message)
        if upper_only:
            user_input = user_input.upper()
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

# __________________________________________________________________________________________________#


def user_input_with_error_check_blacklist(prompt_message, invalid_tuple, specific_location):
    """Receive user input and confirm that it's not on the blacklist (certain characters in specific locations)."""

    # TODO: Find ways to improve this function. I'm sure it can be made better!

    bad_input = True
    while bad_input:
        bad_input = False   # Innocent until proven guilty (for every iteration of the while loop).
        user_input = input(prompt_message).strip()
        if user_input == '':    # Explicitly check for empty string.
            bad_input = True
            print("\nInvalid entry, please try again.\n")
            continue
        for i in range(len(invalid_tuple)):     # Make sure each member of invalid_tuple doesn't appear in the input.
            if specific_location[i] is None:    # Not allowed at any location.
                if invalid_tuple[i] in user_input:
                    # Reject input.
                    bad_input = True
                    print("\nInvalid entry, please try again.\n")
                    break
            else:           # Not allowed at the specific location in specific_location[i], but allowed elsewhere.
                if invalid_tuple[i] in user_input[specific_location[i]]:
                    # Reject input.
                    bad_input = True
                    print("\nInvalid entry, please try again.\n")
                    break

    return user_input

# __________________________________________________________________________________________________#


def which_budget():
    """Top-level menu which determines which budget (database) to connect to"""
    # TODO: Make filenames distinct from user-supplied budget names. Then no need to limit user's input!
    # TODO: Provide option to delete an existing budget.
    WHICH_BUDGET_MENU_OPTIONS = [
        "make a new budget,",
        "load an existing budget,",
        "quit the program."
    ]

    while True:
        choice = recite_menu_options(WHICH_BUDGET_MENU_OPTIONS)
        if choice == 1:
            # The user wants to create a brand new budget.
            while True:
                budget_name = user_input_with_error_check_blacklist(
                    "\nPlease choose a name for your new budget, or enter 0 to cancel: ",
                    ('.', ':', '/'),
                    (0, None, None)
                )
                # Now confirm that there isn't an existing budget that already has that name.
                if os.path.isfile(os.path.join(user_budgets, budget_name + '.db')):
                    print("\nA budget already exists with that name. Please enter a different name.")
                else:
                    break
            if budget_name == "0":
                # User wants to cancel. Loop to top of this function.
                continue
            # Name has been approved, proceed with setting up new database and connecting to it.
            connection = sqlite3.connect(os.path.join(user_budgets, budget_name + '.db'))
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
            print("\nGreat! You have created a brand new budget called %s." % budget_name)
            break

        if choice == 2:
            # The user wants to load an existing budget.
            list_of_budgets = glob.glob("%s/*.db" % user_budgets)   # Pull up list of available budgets
            if len(list_of_budgets) == 0:
                print("\nThere are no existing budgets. You should make a new one!")
            else:
                print("\nWhich budget would you like to load?")
                for i in range(len(list_of_budgets)):
                    print("\t%d)" % (i + 1), os.path.splitext(os.path.basename(list_of_budgets[i]))[0])
                budget_number = user_input_with_error_check_whitelist(
                    "Enter the number in front of the budget you wish to load, or enter 0 to cancel: ",
                    range(len(list_of_budgets) + 1),
                    False,
                    True
                )
                if budget_number == 0:
                    # User wants to cancel. Loop to top of this function.
                    continue
                else:
                    # Load the budget that corresponds to the number the user entered.
                    connection = sqlite3.connect(list_of_budgets[budget_number - 1])
                    print("\nBudget loaded: %s" % os.path.splitext(
                        os.path.basename(list_of_budgets[budget_number - 1]))[0])
                    break

        if choice == 3:
            # Quit the program!
            exit_program()

    return connection

# __________________________________________________________________________________________________#


def exit_program():
    """Exit the program gracefully (with exit code 0)."""
    print("\nThanks for using Ben's Budget Program. See you later!")
    raise SystemExit

# __________________________________________________________________________________________________#


def main():
    """Main menu of the program, acting as 'central hub' through which users navigate to get to all other parts."""
    MAIN_MENU_OPTIONS = ["go to the category menu,",
                         "go to the transactions menu,",
                         "go to the accounts menu,",
                         "choose a different budget or quit the program."
                         ]
    global conn
    global config_directory
    global user_budgets

    # All files affiliated with this program will be located at the path stored in config_directory
    # Bash uses ~ to mean the home directory, but Python doesn't know that.
    # That's why we use os.path.expanduser() in the following command.
    config_directory = os.path.expanduser('~/Library/Application Support/Bens Budget Program')
    if not os.path.exists(config_directory):
        os.makedirs(config_directory)

    user_budgets = os.path.join(config_directory, "User Budgets")
    if not os.path.exists(user_budgets):
        os.makedirs(user_budgets)

    # Here is where the user experience begins:
    print("\nWelcome to Ben's Budget Program!")
    while True:
        conn = which_budget()
        while True:
            choice = recite_menu_options(MAIN_MENU_OPTIONS)
            if choice == 1:
                menu_for_categories()
            elif choice == 2:
                menu_for_transactions()
            elif choice == 3:
                menu_for_accounts()
            elif choice == 4:
                print("\n~~You are now returning to the budget selection menu.~~")
                conn.close()
                break
            print("\n~~You are now returning to the main menu.~~")

# __________________________________________________________________________________________________#


if __name__ == "__main__":
    main()

"""
Here are ideas of next steps and features:
-Add a Delete Existing Budget option to the main menu.
-Add a Delete Category option to the Categories menu.
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

Discussion with Dad on 11/26/16:
-Implement config files
    config files save user preferences ("configurations")
    Module: configparser
    ~/Library/Application Support/Bens Budget Program
    

"""