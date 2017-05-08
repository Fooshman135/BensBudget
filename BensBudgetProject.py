#!/usr/bin/env python

"""
This is my first attempt at a full Python program. The purpose of this program is to:
(1) learn how to code hands-on with Python,
(2) have a project that I can use to demonstrate my abilities,
(3) possibly practice incorporating machine learning principles.

This program will be a budgeting program, inspired by YNAB. It's components shall include:
(1) A list of budget categories (and subcategories), created by the user
(2) A way to add/delete/edit budget categories
(3) A list of transactions, entered by the user
(4) A way to add/delete/edit transactions
(5) A summary of weekly/monthly/annual statistics and trends
(6) Machine learning tool that makes suggestions to the user regarding how they should change their spending
    habits in order to:
    a. Pay down debt
    b. Increase their savings/investment contributions
    c. Anticipate upcoming expenses, using the user's history as the training set
(7) A measure of cash available to be budgeted
(8) For each budget category, there should be an attribute for the budgeted amount assigned to that category.

I expect this to be rough, and not something that people would want to pay money for. However, it needs to be:
COMPLETE    (Must create a minimum viable product, even if missing desirable features)
WORKING,    (One should be able to track their budgeting with this)
EFFICIENT,  (The algorithms should be fast and elegant), and
CLEAN       (The code should be readable, concise, and make sense).

Let's dive in and see what happens!
"""

# __________________________________________________________________________________________________#


def display_categories():

    # SQL command to query the Categories table, showing only the name attribute.
    cur = conn.cursor()
    cur.execute("SELECT name FROM Categories")
    num_categories = 0
    while True:
        try:
            next_category = cur.fetchone()[0]
        except TypeError:   # cur.fetchone() returns None at the end of the query, which is non-subscriptable.
            if num_categories == 0:
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

    # TODO: Provide option for user to cancel this decision and return to previous menu.

    # This function is called whenever the user wants to create a new budget category.
    # First, ask the user what the category's name should be.
    cur = conn.cursor()

    while True:
        name = input("\nWhat do you want to call your new category? ").strip()
        if name == '':
            print("\nInvalid entry, please try again.\n")
            continue
        cur.execute("SELECT name FROM Categories WHERE name=?", (name,))
        check = cur.fetchall()
        if not check:
            # The name which the user entered is not already in the Categories table.
            break
        else:
            print("\nA category already exists with that name. Please choose a different name.\n")
            continue

    # Now add this category to the category table in the .db file.
    cur.execute('INSERT INTO Categories VALUES(?,0)', (name,))
    cur.close()
    conn.commit()

    print("\nOkay! You added a new category called %s to your list!" % name)

# __________________________________________________________________________________________________#


def recite_menu_options(list_of_options):

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

    # TODO: Transfer category value to "unbudgeted total" category.
    # TODO: Determine how to handle transactions which refer to the deleted category.

    # Present the user with a list of categories and ask which one should be deleted (0 for cancel)
    # Then delete that category from table.
    cur = conn.cursor()
    cur.execute("SELECT name FROM Categories")

    num_categories = 0
    category_dict = {}

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
    pass
    # TODO: Build out transactions functions.

# __________________________________________________________________________________________________#


def menu_for_accounts():

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

    # TODO: Also show account balances. Start by changing the SQL query to be "SELECT * FROM Accounts" and use fetchone()[1].

    # SQL command to query the Categories table, showing only the name attribute.
    cur = conn.cursor()
    cur.execute("SELECT name FROM Accounts")
    num_accounts = 0
    while True:
        try:
            next_account_name = cur.fetchone()[0]
        except TypeError:  # cur.fetchone() returns None at the end of the query, which is non-subscriptable.
            if num_accounts == 0:
                print("\nYou have no accounts! You should add some!")
            break
        else:
            if num_accounts == 0:
                print("\nHere are your accounts and their balances:")
            print("\t", next_account_name)
            num_accounts += 1

    cur.close()

# __________________________________________________________________________________________________#


def new_account():

    # TODO: Prompt user to add starting account balance (not just account name).
    # TODO: Add option for user to cancel this decision and return to previous menu.

    # This function is called whenever the user wants to add an account.
    # First, ask the user what the account's name should be.
    cur = conn.cursor()

    while True:
        name = input("\nWhat do you want to call your new account? ").strip()
        if name == '':
            print("\nInvalid entry, please try again.\n")
            continue
        cur.execute("SELECT name FROM Accounts WHERE name=?", (name,))
        check = cur.fetchall()
        if not check:
            # The name which the user entered is not already in the Accounts table.
            break
        else:
            print("\nAn account already exists with that name. Please choose a different name.\n")
            continue

    # Now add this account to the account table in the .db file.
    cur.execute('INSERT INTO Accounts VALUES(?,0)', (name,))
    cur.close()
    conn.commit()

    print("\nOkay! You added a new account called %s to your list!" % name)

# __________________________________________________________________________________________________#


def delete_account():

    # TODO: figure out what to do with balance (assuming it's non-zero).
    # TODO: Determine how to handle transactions which refer to the deleted account.

    # Present the user with a list of accounts and ask which one should be deleted (0 for cancel)
    # Then delete that account from table.
    cur = conn.cursor()
    cur.execute("SELECT name FROM Accounts")

    num_accounts = 0
    account_dict = {}

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
    # Display prompt_message to the user and then receive input.
    # Then determine whether the input is in valid_set.
    # If it is, return the input.
    # Otherwise print an error message and loop back to prompt the user again.

    while True:

        if upper_only:
            user_input = input(prompt_message).upper()
        else:
            user_input = input(prompt_message)

        if integer:
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
    # Display prompt_message to the user and then receive input.
    # Then determine whether any of the members within invalid_tuple appear in the input at the location
    #   specified by the corresponding member within specific_location.
    # If none of the members in invalid_tuple meet the criteria in specific_location, return the user input.
    # If at least one member meets the criteria, print an error message and loop back and prompt the user again.

    bad_input = True
    while bad_input:
        
        # Innocent until proven guilty (for every iteration of the while loop).
        bad_input = False

        user_input = input(prompt_message).strip()

        # Explicitly check for empty string.
        if user_input == '':
            bad_input = True
            print("\nInvalid entry, please try again.\n")
            continue

        for i in range(len(invalid_tuple)):

            if specific_location[i] is None:

                if invalid_tuple[i] in user_input:
                    # Break out of for loop and go back to top of while loop.
                    bad_input = True
                    print("\nInvalid entry, please try again.\n")
                    break

            else:

                if invalid_tuple[i] in user_input[specific_location[i]]:
                    # Break out of for loop and go back to top of while loop.
                    bad_input = True
                    print("\nInvalid entry, please try again.\n")
                    break

    return user_input

# __________________________________________________________________________________________________#


def which_budget():
    WHICH_BUDGET_MENU_OPTIONS = [
        "make a new budget,",
        "load an existing budget,",
        "quit the program."
    ]

    while True:

        choice = recite_menu_options(WHICH_BUDGET_MENU_OPTIONS)

        if choice == 1:
            # The user wants to create a brand new budget.
            # First prompt the user to name the new budget. Also validate their input.
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

            # Create a new .db file (located in the User_Budgets folder) with that name.
            conn = sqlite3.connect(os.path.join(user_budgets, budget_name + '.db'))

            # Now create an empty tables for categories, transactions, and accounts.
            cur = conn.cursor()

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
            conn.commit()

            # Then finally go to the main menu.
            print("\nGreat! You have created a brand new budget called %s." % budget_name)
            break

        if choice == 2:
            # The user wants to load an existing budget.
            # First pull up a list of available budgets from the user_budgets folder.

            list_of_budgets = glob.glob("%s/*.db" % user_budgets)

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
                    conn = sqlite3.connect(list_of_budgets[budget_number - 1])
                    print("\nBudget loaded: %s" % os.path.splitext(
                        os.path.basename(list_of_budgets[budget_number - 1]))[0])
                    break

        if choice == 3:
            # Quit the program!
            exit_program()

    return conn

# __________________________________________________________________________________________________#


def exit_program():
    print("\nThanks for using Ben's Budget Program. See you later!")
    raise SystemExit

# #####################################   START OF PROGRAM   ########################################

import os
import sqlite3
import glob

MAIN_MENU_OPTIONS = ["go to the category menu,",
                     "go to the transactions menu,",
                     "go to the accounts menu,",
                     "choose a different budget or quit the program."
                     ]

# All config/installation files will be located here:
config_directory = os.path.expanduser('~/Library/Application Support/Bens Budget Program')
# Bash uses ~ to mean the home directory, but Python doesn't know that.
# That's why we use os.path.expanduser() in the previous command.

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


# ######################################   END OF PROGRAM   #########################################

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

Discussion with Dad on 11/26/16:
-Implement config files
    config files save user preferences ("configurations")
    Module: configparser
    ~/Library/Application Support/Bens Budget Program
    

"""