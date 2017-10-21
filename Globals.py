import os


# GLOBAL CONSTANTS ============================================================

CONFIG_DIRECTORY = os.path.expanduser(
    '~/Library/Application Support/Ben\'s Budget Program')

USER_BUDGETS = os.path.join(CONFIG_DIRECTORY, "User Budgets")



# GLOBAL VARIABLES ============================================================

conn = None

# GUI is a flag that determines whether the UI is GUI (if True) or
#  CLI (if False).
GUI = False


SELECTED_BUDGET_NAME = None




