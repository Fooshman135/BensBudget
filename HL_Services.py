import Views
import LL_Services
import Gateway
import Globals
import Models



# ____________________________________________________________________________#
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
            Views.display_error_message()
            continue
        break

    return list_of_options[int(choice_num)-1]


# ____________________________________________________________________________#
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
    Gateway.create_database_with_tables(budget_name)
    Views.display_output("\nGreat! You have created a brand new budget "
        "called %s." % budget_name)
    Views.press_key_to_continue()
    return budget_name



# ____________________________________________________________________________#
def create_budget_and_load_it():

    budget_name = new_budget()
    if budget_name is not None:
        # User created a budget, now load it.
        Gateway.establish_db_connection(LL_Services.just_name_to_full_filepath(budget_name))
        main_menu()


# ____________________________________________________________________________#
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







# ____________________________________________________________________________#
def load_budget():

    list_of_budgets = LL_Services.get_all_budgets(Globals.USER_BUDGETS)
    if len(list_of_budgets) == 0:
        Views.display_output("\nThere are no existing budgets. You should make a new one!")
        Views.press_key_to_continue()
        return
    Views.display_output("\nWhich budget would you like to load?\n")

    name_list = [LL_Services.full_filepath_to_just_name(budget) for budget in list_of_budgets]
    Views.print_rows(name_list, ['Budgets'], show_nums=True)
    Views.display_output("")

    while True:
        budget_number = Views.display_input( "Enter the number in front of the budget you wish to load, or enter 0 to cancel: ")
        proceed = LL_Services.int_validate(
            budget_number,
            num_lb=0,
            num_ub=len(list_of_budgets),
        )
        if proceed == False:
            Views.display_error_message()
            continue
        break

    budget_number = int(budget_number)
    if budget_number > 0:
        # Load the budget that corresponds to the number the user entered.
        Gateway.establish_db_connection(list_of_budgets[budget_number - 1])
        Views.display_output("\nBudget loaded: %s" % Globals.SELECTED_BUDGET_NAME)
        main_menu()




# ____________________________________________________________________________#
def delete_budget():
    pass


# ____________________________________________________________________________#
def exit_program():
    """Exit the program gracefully (with exit code 0)."""

    print("\nThanks for using Ben's Budget Program. See you later!")
    try:
        Globals.conn.close()
    except AttributeError:
        # The variable conn was never set.
        pass
    raise SystemExit