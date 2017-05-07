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
(6) Machine learning tool that makes suggestions to the user regarding how they should change their spending habits in order to:
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

#__________________________________________________________________________________________________#
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

#__________________________________________________________________________________________________#
def new_category():

    # This function is called whenever the user wants to create a new budget category.
    # First, ask the user what the category's name should be.
    cur = conn.cursor()

    while True:
        name = input("\nWhat do you want to call your new category? ").strip()
        # Note: I was unable to find a category name that raised an exception, so there is no error-checking here!
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

#__________________________________________________________________________________________________#
def reciteMenuOptions(listOfOptions):
    # TODO: This function should call the user_input_with_error_check_valid() function.

    while True:

        print("\nWhat would you like to do?")
        
        for i in range(len(listOfOptions)):
            print("Press %d to %s" % (i+1, listOfOptions[i]))

        try:
            user_input = int(input("Enter your choice here: "))
        except ValueError:
            print("\nInvalid entry, please try again.")
        else:
            # Now that we've successfully converted the input into an int type, make sure it is in the right range.
            # That is, make sure it is in the set {i+1} for i in range(len(listOfOptions))
            if user_input in range(1,len(listOfOptions)+1):
                break
            else:
                print("\nInvalid entry, please try again.")

    # The input is valid, so we can return it now.
    return user_input

#__________________________________________________________________________________________________#
def menu_for_categories():

    CATEGORY_MENU_OPTIONS = ["see your list of budget categories,",
                             "add a new category,",
                             "return to the main menu."
                             ]

    print("\n~~You are now in the categories menu.~~")

    while True:

        choice = reciteMenuOptions(CATEGORY_MENU_OPTIONS)

        if choice == 1:
            display_categories()
    
        elif choice == 2:
            #my_categories.append(new_category())
            new_category()
    
        elif choice == 3:
            break

#__________________________________________________________________________________________________#
def menu_for_transactions():
    pass
    # TODO: date, payee, category, memo, amount



#__________________________________________________________________________________________________#
def user_input_with_error_check_valid(promptMessage, validSet, upperOnly, integer):
    # This function uses promptMessage inside the input() function to get user input.
    # Then this function determines whether the user input is in validSet.
    # If it is, then return the user input.
    # If it isn't, then print an error message and loop back and prompt the user again.

    while True:

        if upperOnly:
            user_input = input(promptMessage).upper()
        else:
            user_input = input(promptMessage)

        if integer:
            try:
                user_input = int(user_input)
            except ValueError:
                print("\nInvalid entry, please try again.\n")
                continue

        if user_input in validSet:
            break
        else:
            print("\nInvalid entry, please try again.\n")

    return user_input

#__________________________________________________________________________________________________#
def user_input_with_error_check_invalid(promptMessage, invalidTuple, specificLocation):
    # This function uses promptMessage inside the input() function to get user input.
    # Then this function determines whether any of the members within invalidTuple appear in the user input.
    # Each member of invalidTuple may have a criteria regarding where they can't appear, as detailed in specficLocation.
    # If none of the members in invalidTuple meet the criteria in specificLocation, then return the user input.
    # If at least one member meets the criteria, then print an error message and loop back and prompt the user again.

    badInput = True
    while badInput:
        
        # Innocent until proven guilty (for every iteration of the while loop).
        badInput = False

        user_input = input(promptMessage).strip()

        # Don't allow the user to enter the empty string (by just hitting Enter).
        if user_input == '':
            badInput = True
            print("\nInvalid entry, please try again.\n")
            continue

        for i in range(len(invalidTuple)):

            if specificLocation[i] is None:

                if invalidTuple[i] in user_input:
                    # Break out of for loop, print error message, loop back up to top of while loop
                    badInput = True
                    print("\nInvalid entry, please try again.\n")
                    break

            else:

                if invalidTuple[i] in user_input[specificLocation[i]]:
                    # Break out of for loop, print error message, loop back up to top of while loop
                    badInput = True
                    print("\nInvalid entry, please try again.\n")
                    break

    return user_input


#__________________________________________________________________________________________________#
def which_budget():
    which_budget_menu_options = [
        "make a new budget,",
        "load an existing budget,",
        "quit the program."
    ]

    while True:

        choice = reciteMenuOptions(which_budget_menu_options)

        if choice == 1:
            # The user wants to create a brand new budget.
            # First prompt the user to name the new budget. Also validate their input.
            while True:
                budget_name = user_input_with_error_check_invalid(
                    "\nPlease choose a name for your new budget, or enter 0 to cancel: ", ('.', ':'), (0, None)
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

            # Now create an empty Categories table and an empty Transactions table.
            cur = conn.cursor()

            cur.execute('CREATE TABLE Categories('
                      'name TEXT,'
                      'value REAL)'
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
                    print("\t%d)" % (i + 1), list_of_budgets[i])    # TODO: exclude full file path as well as .db
                budget_number = user_input_with_error_check_valid(
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
                    print("\nBudget loaded: %s" % list_of_budgets[budget_number - 1])
                    break

        if choice == 3:
            # Quit the program!
            exit_program()

    return conn

#__________________________________________________________________________________________________#
def exit_program():
    print("\nThanks for using Ben's Budget Program. See you later!")
    raise SystemExit


######################################   START OF PROGRAM   ########################################

# Here is where I import all modules:
import os
import sqlite3
import glob

MAIN_MENU_OPTIONS = ["go to the category menu,",
                     "go to the transactions menu,",
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

        choice = reciteMenuOptions(MAIN_MENU_OPTIONS)

        if choice == 1:
            menu_for_categories()

        elif choice == 2:
            menu_for_transactions()

        elif choice == 3:
            print("\n~~You are now returning to the budget selection menu.~~")
            conn.close()
            break

        print("\n~~You are now returning to the main menu.~~")
          


#######################################   END OF PROGRAM   #########################################


"""
Here are ideas of next steps and features:
-Add a Delete Existing Budget option to the main menu.
-Add a Delete Category option to the Categories menu.
-Implement some sense of time. Consider making the time frame variable, based on user input.
-Expand the display_categories() function to show more than just the category names. Ideas for expansion include:
    -Showing a table with category names as rows, and other attributes (such as budget_value) as columns.
    -Similar to YNAB, show total transctions for the given time period.
-Build out the transactions section of the program.
-Consider making a function that prompts the user "Press enter to continue" and doesn't continue until they do.
    -Call this function everytime they enter some input (after the immediate results of their input is shown to them.
    -For example:
        -the program prompts them for a menu item,
        -they enter a number,
        -the program tells them what the immediate result of their input is,
        -the program calls this press_enter_to_continue function
-Python does not have a switch statement, so the current use of if/elif/else will have to do.
-Allow users to create their own subsets of categories (distinct from the idea of supercategories).
    -Allow users to see spending patterns/trends in just that subset.
-Use regular expressions to check user input (and make sure it's valid).

Discussion with Dad on 11/26/16:
-Implement config files
    config files save user preferences ("configurations")
    Module: configparser
    ~/Library/Application Support/Bens Budget Program
    

"""