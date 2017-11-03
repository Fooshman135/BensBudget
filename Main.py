import LL_Services
import Views
import HL_Services
import Globals


# ____________________________________________________________________________#
def main():

    # Note that, in the below dictionary values, the parentheses are omitted
    # intentionally.
    WHICH_BUDGET_MENU_OPTIONS = {
        "make a new budget.": HL_Services.create_budget_and_load_it,
        "load an existing budget.": HL_Services.load_budget,
        "delete an existing budget.": HL_Services.delete_budget,
        "quit the program.": HL_Services.exit_program,
        }

    LL_Services.create_directory(Globals.USER_BUDGETS)
    Views.display_output("\nWelcome to Ben's Budget Program!")
    while True:
        LL_Services.menu_header({"BUDGET SELECTION MENU:": ""})
        choice = HL_Services.recite_menu_options_and_get_selection(list(WHICH_BUDGET_MENU_OPTIONS.keys()))
        WHICH_BUDGET_MENU_OPTIONS[choice]()

# ____________________________________________________________________________#
if __name__ == "__main__":
    main()