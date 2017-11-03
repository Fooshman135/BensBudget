import Globals
import LL_Services

# ____________________________________________________________________________#
def display_output(text):
    """All output text should be routed through here.
    This function states whether to pass it along to a CLI view function
    or a GUI view function."""
    if Globals.GUI == True:
        # GUI output
        pass
    else:
        # CLI output
        print(text)


# ____________________________________________________________________________#
def display_input(prompt):
    """All input text should be routed through here.
    This function states whether to pass it along to a CLI view function
    or a GUI view function."""
    if Globals.GUI == True:
        # GUI output
        pass
    else:
        # CLI output
        try:
            user_input = raw_input(prompt).strip()  # Python 2.X
        except NameError:
            user_input = input(prompt).strip()  # Python 3.X
        return user_input


# ____________________________________________________________________________#
def display_error_message(text="\nInvalid entry, please try again."):
    if Globals.GUI == True:
        # GUI output
        pass
    else:
        # CLI output
        print(text)


# ____________________________________________________________________________#
def press_key_to_continue():
    """Prompts the user to hit a button before displaying the next menu."""
    try:
        raw_input("Press Enter to continue... ")    # Python 2.X
    except NameError:
        input("Press Enter to continue... ")        # Python 3.X
    print()     # Prints a blank line.




# ____________________________________________________________________________#
def print_rows(table, col_names, show_nums=False):
    """Given a table of data (implemented as a list of objects), print out
     the rows with proper formatting.

     :param table: A list of object instances whose attributes are to be
     displayed in tabular format. Each row of the table corresponds to a
     single object, and each column corresponds to an object attribute.
     Note that every object in this list are from the same class.
     :param col_names: A list of strings corresponding to a subset of the
     attributes of the objects in the 'table' list. This might be equal to
     the full list of attributes. Each string must be spelled exactly as
     the attribute is spelled, including casing. Only the attributes whose
     names appear in this parameter will be printed.
     :param show_nums: A flag that determines whether to display
     incrementing integers in front of each row (to assist user selection).
     """

    top = ""
    num = 1

    # The following variables can be tweaked to change the formatting
    # of the output.
    left_margin = 5
    gap = 6


    # Calculate maximum lengths for each column for formatting purposes.
    max_dict = LL_Services.find_max_of_each_obj_attr(table)
    for name in col_names:
        if len(name) > max_dict[name]:
            max_dict[name] = len(name)
        # Print top row and dividing line.
        top += "{}{:{pad}}".format(
            " "*gap,
            name.title(),
            pad=max_dict[name],
        )

    top = top.lstrip()
    print("{}{}".format(" "*left_margin, top))
    print("{}{}".format(" "*left_margin, "-"*len(top)))

    # Now print all the other rows.
    for obj in table:
        output = ""
        for name in col_names:
            att = getattr(obj, name)
            right_justified = False
            if type(att) == str or type(att) == int:
                concat = str(att)
            elif type(att) == float:
                minus = "-$" if att < 0 else "$"
                concat = minus + "{:,.2f}".format(abs(att))
                right_justified = True
            elif type(att) == dt:
                concat = att.strftime("%m/%d/%Y")
            elif att is None:
                concat = ""
            else:
                raise Exception("Ben Katz - developer error.")
            if right_justified:
                output = output + "{}{:>{pad}}".format(
                    " "*gap,
                    concat,
                    pad=max_dict[name],
                )
            else:
                output = output + "{}{:{pad}}".format(
                    " "*gap,
                    concat,
                    pad=max_dict[name],
                )
        output = output.strip()

        temp = str(num) + ")" if show_nums else ""
        print("{:{pad}}{}".format(
            temp,
            output,
            pad=left_margin),
        )
        num += 1


# ____________________________________________________________________________#
def print_list(str_list, show_nums=False):
    """Receives a list of strings and prints them each on their own line.

    :param str_list: A list containing only strings, each of which needs to
    be printed on its own line.
    :param show_nums: A flag that determines whether a number should be shown
    in front of each string.
    :return: Nothing.
    """

    left_margin = 5
    num = 1

    for string in str_list:
        temp = str(num) + ")" if show_nums else ""
        print("{:{pad}}{}".format(
            temp,
            string,
            pad=left_margin),
        )
        num += 1



