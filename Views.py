import Globals


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



def display_error_message(text):
    if Globals.GUI == True:
        # GUI output
        pass
    else:
        # CLI output
        if text == '':
            print("\nInvalid entry, please try again.")
        else:
            print(text)


def press_key_to_continue():
    """Prompts the user to hit a button before displaying the next menu."""
    try:
        raw_input("Press Enter to continue... ")    # Python 2.X
    except NameError:
        input("Press Enter to continue... ")        # Python 3.X
    print()     # Prints a blank line.