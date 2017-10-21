from datetime import date as dt
import Views
import Globals
import os
import re
import glob

# ____________________________________________________________________________#
def create_user_directory():
    """Create a directory to store user data for this app, unless one
    already exists."""

    # All files affiliated with this program will be located at the path
    # stored in CONFIG_DIRECTORY.
    if not os.path.exists(Globals.USER_BUDGETS):
        os.makedirs(Globals.USER_BUDGETS)



# ____________________________________________________________________________#
def menu_header(header_dict):
    """Print a menu header showing the items within header_list. The keys
    of the dictionary are expected to be strings, and the values are expected
    to be floats, strings, datetime.date objects, or NoneType."""

    output = ""
    gap = "    "

    for key in header_dict:
        if type(header_dict[key]) == str:
            item_gap = " "
            value = header_dict[key]
        elif type(header_dict[key]) == float:
            item_gap = " -$" if header_dict[key] < 0 else " $"
            value = "{:,.2f}".format(abs(header_dict[key]))
        elif type(header_dict[key]) == dt:
            item_gap = " "
            value = str(header_dict[key].strftime("%m/%d/%Y"))
        elif header_dict[key] is None:
            item_gap = " "
            value = "(None)"
        output = output + gap + key + item_gap + value

    output = output.strip()
    Views.display_output("")
    Views.display_output("-" * len(output))
    Views.display_output(output)
    Views.display_output("-" * len(output))




# ____________________________________________________________________________#
def float_validate(user_input, num_lb=float('-inf'), num_ub=float('inf')):
    """Confirms that input is a float (or int) and is in the correct range.
     Returns True if both tests pass, and False otherwise.
     user_input will be of type str.
     """

    # Check to make sure user didn't input 'inf' or '-inf'
    if user_input in ['inf', '-inf']:
        return False

    try:
        user_input = float(user_input)
    except ValueError:
        # user input was not of type float
        return False

    # Now check to make sure user_input is in range.
    if (user_input < num_lb) or (user_input > num_ub):
        # user input is not in the correct range.
        return False

    return True


# ____________________________________________________________________________#
def int_validate(user_input, num_lb=float('-inf'), num_ub=float('inf')):
    """Confirms that input is an integer and is in the correct range.
     Returns True if both tests pass, and False otherwise.
     user_input will be of type str.
     """

    try:
        user_input = int(user_input)
    except ValueError:
        # user input was not of type int
        return False

    # Now check to make sure user_input is in range.
    if (user_input < num_lb) or (user_input > num_ub):
        # user input is not in the correct range.
        return False

    return True


# ____________________________________________________________________________#
def date_validate(user_input):
    """Confirm that input is in MM/DD/YYYY format, and is a real date."""

    regex = '^\d\d/\d\d/\d\d\d\d$'
    match = re.search(regex, user_input)
    if not match:
        # User input didn't match the regex.
        return False

    # User input matched the regex. Convert to datetime.date format.
    temp = user_input.split('/')
    month = int(temp[0])
    day = int(temp[1])
    year = int(temp[2])
    try:
        user_input = dt(month=month, day=day, year=year)
    except ValueError:
        # The input was not a real date.
        return False

    try:
        user_input.strftime("%m/%d/%Y")
    except ValueError:
        # User is running Python 2.x and date precedes 01/01/1900.
        return False

    return True


# ____________________________________________________________________________#
def check_for_existing_budget(name):
    """Checks directory of existing budgets to see if one already exists with
    the name the user has provided.
    Input name is of type str.
    Return True if no existing budget has that name, False otherwise."""

    if os.path.isfile(just_name_to_full_filepath(name)):
        # A budget does exist with that name.
        return False
    return True


# ____________________________________________________________________________#
def is_string_valid_filename(name):
    """Checks to see if input can be used as a Unix filename.
    Returns True is it can be used, False otherwise."""

    regex1 = '^[.].*$'      # Matches if string contains '.' as the first char.
    regex2 = '^.*:+.*$'     # Matches if string contains ':' anywhere.
    regex3 = '^.*/+.*$'     # Matches if string contains '/' anywhere.

    match1 = re.search(regex1, name)
    match2 = re.search(regex2, name)
    match3 = re.search(regex3, name)

    if match1 or match2 or match3:
        # name matches with at least one of the regexs above - bad!
        return False
    return True


# ____________________________________________________________________________#
def get_all_budgets(directory):
    """Returns a list of all .db files located at the input directory.
    Input is of type str, output is of type list."""
    return glob.glob("%s/*.db" % directory)


# ____________________________________________________________________________#
def full_filepath_to_just_name(full_filepath):
    return os.path.splitext(os.path.basename(full_filepath))[0]


# ____________________________________________________________________________#
def just_name_to_full_filepath(name):
    return os.path.join(Globals.USER_BUDGETS, name + '.db')




