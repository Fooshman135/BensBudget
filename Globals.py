import os


# GLOBAL CONSTANTS ============================================================

# All files affiliated with this program will be located at the path
# stored in CONFIG_DIRECTORY.
CONFIG_DIRECTORY = os.path.expanduser(
    '~/Library/Application Support/Ben\'s Budget Program')

USER_BUDGETS = os.path.join(CONFIG_DIRECTORY, "User Budgets")



# GLOBAL VARIABLES ============================================================

# conn is the sqlite3 connection to the active database.
conn = None

# SELECTED_BUDGET_NAME is the name of the budget corresponding to the
# active database.
SELECTED_BUDGET_NAME = None

# GUI is a flag that determines whether the UI is GUI (if True) or
#  CLI (if False).
GUI = False







