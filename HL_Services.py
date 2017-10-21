import Views
import LL_Services
import Gateway
import Globals
import Models





def recite_menu_options(list_of_options):
    """Present user with a series of options and make them choose one."""


    Views.display_output("\nWhat would you like to do?")
    for i in range(len(list_of_options)):
        Views.display_output("Press %d to %s" % (i + 1, list_of_options[i]))

    while True:

        # Request user input
        choice_num = Views.display_input("Enter your choice here: ")

        # int_validation
        valid = LL_Services.int_validate(choice_num, 1, len(list_of_options))

        # If bad, print error and loop. Else, break.
        if valid == False:
            # Input was bad.
            Views.display_error_message("\nInvalid entry, please try again.")
            continue
        break

    return list_of_options[int(choice_num)-1]



def new_budget():
    """The user wants to create a brand new budget."""

    Views.display_output("")

    while True:
        budget_name = Views.display_input(
            "Please choose a name for your new budget, "
            "or enter a blank line to cancel: ")

        # Check for empty string (meaning user wants to cancel)
        if budget_name == "":
            # User wants to cancel.
            return

        # Confirm that it's a valid file name (filesystem allows it).
        valid = LL_Services.is_string_valid_filename(budget_name)
        if valid == False:
            Views.display_error_message(
                "\nInvalid filename, cannot contain '.' at the start and"
                " cannot contain ':' or '/' anywhere.")
            continue

        # Confirm that there isn't an existing budget with that name.
        available = LL_Services.check_for_existing_budget(budget_name)
        if available == False:
            Views.display_error_message(
                "\nA budget already exists with that name. Please enter"
                " a different name.")
            continue

        # Name has been approved. Break out of loop.
        break

    # Proceed with setting up new database and connecting to it.
    connection = Gateway.create_database_with_tables(budget_name)
    Views.display_output("\nGreat! You have created a brand new budget "
        "called %s." % budget_name)
    Views.press_key_to_continue()
    return connection, budget_name




def create_budget_and_load_it():
    try:
        (Globals.conn, Globals.SELECTED_BUDGET_NAME) = new_budget()
    except TypeError:
        # User cancelled instead of creating a new budget.
        pass
    else:
        main_menu()




def main_menu():

    MAIN_MENU_OPTIONS = {
        "go to the category menu.": Models.Category.menu_for_categories,
        "go to the transactions menu.": Models.Transaction.menu_for_transactions,
        "go to the accounts menu.": Models.Account.menu_for_accounts,
        "choose a different budget or quit the program.": lambda: False
    }

    while True:
        LL_Services.menu_header({"MAIN MENU:": Globals.SELECTED_BUDGET_NAME})
        choice = recite_menu_options(list(MAIN_MENU_OPTIONS.keys()))
        next = MAIN_MENU_OPTIONS[choice]()
        if next == False:
            # User wants to go up one level.
            break
        Views.display_output("\n~~You are now returning to the main menu.~~")

    Views.display_output("\n~~You are now returning to the budget selection menu.~~")
    Globals.conn.close()








def load_budget():
    pass


def delete_budget():
    pass



def exit_program():
    """Exit the program gracefully (with exit code 0)."""

    print("\nThanks for using Ben's Budget Program. See you later!")
    try:
        Globals.conn.close()
    except AttributeError:
        # The variable conn was never set.
        pass
    raise SystemExit