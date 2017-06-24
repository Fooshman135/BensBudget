#!/usr/bin/env python3

"""
Ben Katz coding sample.

This program was written and designed entirely by Ben Katz. It was created as
a personal project, to showcase knowledge of the Python and SQL languages.

It is designed to be executed by a Python 3.6 interpreter (although earlier
versions of Python 3.x might work too) on Mac OS X. It has not been tested on
other operating systems.

This program will create directories and save files at the following location
(and nowhere else):
    ~/Library/Application Support/Bens Budget Program
Please note that the program will exit if it comes across any operating system
errors or file system errors.

This program is a command line based, personal finance budgeting app. It is a
work-in-progress, but its current development stage is sufficient for
demonstration purposes.

Ben Katz can be contacted at BenCKatz@gmail.com.
Thank you for your consideration.
"""

import os
import sqlite3
import glob

# Bash uses ~ to mean the home directory, but Python doesn't know that.
# That's why we use os.path.expanduser() in the following command.
CONFIG_DIRECTORY = os.path.expanduser(
    '~/Library/Application Support/Bens Budget Program')

WHICH_BUDGET_MENU_OPTIONS = ["make a new budget,",
                             "load an existing budget,",
                             "delete an existing budget,",
                             "quit the program."
                             ]

MAIN_MENU_OPTIONS = ["go to the category menu,",
                     "go to the transactions menu,",
                     "go to the accounts menu,",
                     "choose a different budget or quit the program."
                     ]

CATEGORY_MENU_OPTIONS = ["see your list of budget categories,",
                         "add a new category,",
                         "modify an existing category,",
                         "return to the main menu."
                         ]

CATEGORY_INSTANCE_OPTIONS = ["edit the category's name,",
                             "edit the category's value,",
                             "delete the category,",
                             "return to the category menu."]

ACCOUNT_MENU_OPTIONS = ["see your list of accounts,",
                        "add a new account,",
                        "delete an existing account,",
                        "return to the main menu."
                        ]

TRANSACTION_MENU_OPTIONS = ["view your transactions,",
                            "add a new transaction,",
                            "modify an existing transaction",
                            "return to the main menu."
                            ]

TRANSACTION_INSTANCE_OPTIONS = ["edit the transaction's account,",
                                "edit the transaction's category,",
                                "edit the transaction's amount,",
                                "edit the transaction's payee,",
                                "edit the transaction's date,",
                                "edit the transaction's memo,",
                                "delete the transaction,",
                                "return to the transaction menu."
                                ]

# ____________________________________________________________________________#


class Category:

    # unassigned_funds is not ever allowed to become negative.
    # This is enforced by not allowing accounts to have negative balances.
    unassigned_funds = 0

    def __init__(self, name, value):
        self.name = name
        self.value = value

    @classmethod
    def new_category(cls):
        """Prompt the user for a name and then create a category with that
        name. User can't enter a negative value in this method, but some
        transactions can make the value negative."""

        cur = conn.cursor()
        while True:

            name = input_validation(
                "\nWhat do you want to call your new category? "
                "Enter a blank line to cancel: ",
                str,
                empty_string_allowed=True
            )

            if name == '':
                # User wants to cancel this decision.
                cur.close()
                return

            cur.execute("SELECT name FROM Categories WHERE name=?", (name,))
            check = cur.fetchall()
            if not check:
                # The name which the user entered is not already
                # in the Categories table.
                break
            else:
                print("\nA category already exists with that name. "
                      "Please choose a different name.\n")
                continue

        # Category name has been approved, so now ask if user would like
        # to assign a value.
        print(
            "\nOkay! You added a new category called %s to your list!" % name)
        if cls.unassigned_funds > 0:
            output = "There is ${:,.2f} available to be assigned to " \
                     "categories. How much would you like to assign to {} " \
                     "now? Enter a number: ".format(cls.unassigned_funds, name)
            value = input_validation(
                output,
                float,
                num_lb=0,
                num_ub=cls.unassigned_funds
                )
            # value is valid, but may have extra decimal places (beyond 2).
            value = round(value, 2)
            print("\n${:,.2f} has been added to {}.".format(value, name))

        else:
            # Unassigned funds = 0, so value must also be set to 0.
            value = 0
            output = "There is $0 available to be assigned to categories," \
                     " so {}'s value will be $0 for now.".format(name)
            print(output)

        # Category name and value have been approved, so add them
        # to the Categories table in the database.
        cur.execute('INSERT INTO Categories VALUES(?,?)', (name, value))
        conn.commit()
        cur.close()

        # Finally, update the class attribute for total account balance.
        cls.unassigned_funds -= value

        press_key_to_continue()

    def delete_category(self):
        """Ask user for confirmation before deleting, and then delete."""

        # TODO: Determine how to handle transactions which refer to the deleted category.

        # Ask the user to confirm that the category should be deleted.
        # If yes, then delete it.
        text = "Are you sure that you want to delete the {} category? ".format(
                self.name)

        confirmation = input_validation(
            text+"Enter 1 for yes, 0 for no: ",
            int,
            num_lb=0,
            num_ub=1
        )

        if confirmation == 1:
            # Delete the category.
            Category.unassigned_funds += self.value
            cur = conn.cursor()
            cur.execute("DELETE FROM Categories WHERE name=?",
                        (self.name,))
            conn.commit()
            print("\nYou have successfully deleted %s from your"
                  " list of categories." % self.name)
            cur.close()
            press_key_to_continue()
        return confirmation

    @classmethod
    def display_categories(cls):
        """Query the names and values of the user's categories and present them
        in a vertical list."""

        # TODO: Use with statement to open and close the cursor.
        # TODO: Fix floating point errors for large numbers. Use "decimal" module?
        # TODO: If categories have negative balances, alert the user.

        # Here is how to interpret the string format specifiers below:
        # Let's look at {:>#{pad2},.2f} as an example.
        # The ':' means the following characters are 'format_specs'.
        # The '>' means right-justified.
        # The '{pad2}' is a nested format specifier.
        #   Here it contains a variable for the total number of characters.
        # The ',' groups the digits into sets of 3, separated by a comma.
        # The '.2f' means show two digits after the decimal place.
        #   Note that the 'f' in '.2f' specifies fixed point.

        cur = conn.cursor()
        cur.execute("SELECT name, value FROM Categories")
        instance_list = [Category(name=i[0], value=i[1])
                         for i in cur.fetchall()]

        if len(instance_list) == 0:
            # The Categories table contains no data
            print("\nYou have no categories! You should make some!")
            cur.close()
            press_key_to_continue()
            return

        # Now determine the longest name and balance (when printed).
        max_name_length = 16        # 16 is the length of "Unassigned Funds".
        max_balance_length = len("{:,.2f}".format(abs(cls.unassigned_funds)))
        for category in instance_list:
            if len(category.name) > max_name_length:
                max_name_length = len(category.name)
            instance_balance = "{:,.2f}".format(abs(category.value))
            if len(instance_balance) > max_balance_length:
                max_balance_length = len(instance_balance)

        # Print each category row by row.
        print("\nHere are your categories and their values:")
        for category in instance_list:
            minus = "   -$" if category.value < 0 else "    $"
            output = "{:{pad1}}{}{:>{pad2},.2f}".format(
                category.name,
                minus,
                abs(category.value),
                pad1=max_name_length,
                pad2=max_balance_length,
                )
            print("\t%s" % output)

        # Finally, display the unassigned funds.
        minus = "   -$" if cls.unassigned_funds < 0 else "    $"
        final_line_output = "{:{pad1}}{}{:>{pad2},.2f}".format(
            "Unassigned Funds",
            minus,
            cls.unassigned_funds,
            pad1=max_name_length,
            pad2=max_balance_length)
        print("\t%s" % ("-"*len(final_line_output)))
        print("\t%s" % final_line_output)

        cur.close()
        print()
        press_key_to_continue()

    @staticmethod
    def choose_category():
        """This method is called anytime we need an instance of a Category.
        Once the user selects a category, we create an instance of it.
        Then we can call instance methods on that category."""

        num_categories = 0
        category_dict = {}

        cur = conn.cursor()
        cur.execute("SELECT name FROM Categories")

        while True:
            try:
                category_dict[num_categories + 1] = cur.fetchone()[0]
            except TypeError:
                # cur.fetchone() returns None at the end of the query,
                # which is non-subscriptable.
                if num_categories == 0:
                    print(
                        "\nYou have no categories! You should make some!")
                    press_key_to_continue()
                break
            else:
                if num_categories == 0:
                    print("\nWhich category do you want to select?")
                num_categories += 1
                print("\t%s)" % num_categories,
                      category_dict[num_categories])

        if num_categories > 0:
            choice_number = input_validation(
                "Enter the number in front of the category you wish to "
                "select, or enter 0 to cancel: ",
                int,
                num_lb=0,
                num_ub=num_categories
            )

            if choice_number > 0:
                # Create object instance and copy data into memory.
                cur.execute("SELECT * FROM Categories WHERE name=?",
                            (category_dict[choice_number],))
                temp = cur.fetchall()[0]
                selected_category = Category(
                    name=temp[0],
                    value=temp[1]
                    )
                print("\nYou have selected the {} category.".format(
                    selected_category.name))
                cur.close()
                press_key_to_continue()
                return selected_category

        cur.close()
        return None

    def update_category_name(self):
        """Given a Category instance, allow user to update the instance's
        name."""

        print("\nYour category name is currently {}.".format(self.name))
        output = "What would you like to rename it as? " \
                 "Enter a blank line to cancel: "
        cur = conn.cursor()
        while True:
            name = input_validation(
                output,
                str,
                empty_string_allowed=True
            )

            if name == '':
                # User wants to cancel this decision.
                cur.close()
                return

            if name == self.name:
                # User typed the same name as what the category already has.
                print("\nCategory name will remain {}.".format(self.name))
                cur.close()
                press_key_to_continue()
                return

            cur.execute("SELECT name FROM Categories WHERE name=?", (name,))
            check = cur.fetchall()
            if not check:
                # The name which the user entered is not already
                # in the Categories table.
                break
            else:
                print("\nA category already exists with that name. "
                      "Please choose a different name.\n")
                continue

        # Name has been approved, so update the database.
        cur.execute("UPDATE Categories SET name=? WHERE name=?",
                    (name, self.name))
        conn.commit()
        cur.close()

        # Inform the user of the result.
        output = "You have changed the category name from {} to {}.".format(
            self.name,
            name
            )
        print("\n%s" % output)
        self.name = name
        press_key_to_continue()

    def update_category_value(self):
        """Given a Category instance, allow user to update the instance's
         value."""

        minus = "-$" if self.value < 0 else "$"

        output = "Your {} category currently has a value of {}{:,.2f}.".format(
            self.name,
            minus,
            abs(self.value)
            )
        print("\n%s" % output)
        output = "Your total amount of unassigned funds is ${:,.2f}.".format(
            Category.unassigned_funds)
        print(output)

        # In the special case where both the category and the unassigned
        # funds have $0, don't make user enter any input.
        if Category.unassigned_funds == 0 and self.value <= 0:
            print("Since neither of these are positive, you can't update the "
                  "value right now.")
            press_key_to_continue()
            return

        if self.value < 0:
            lower = 0
            output = "Select a positive amount to add to the " \
                     "category's value: "
        else:
            lower = self.value*(-1)+0
            output = "Select an amount to add to the category's value " \
                     "(negative amounts will be subtracted from the value): "

        diff = input_validation(
            output,
            float,
            num_lb=lower,
            num_ub=Category.unassigned_funds
            )

        # Update the class attributes
        self.value += diff
        Category.unassigned_funds -= diff

        # Now to update the value in the database.
        cur = conn.cursor()
        cur.execute("UPDATE Categories SET value=? WHERE name=?",
                    (self.value, self.name))
        conn.commit()

        # Inform the user of the result.
        if diff == 0:
            output = "No change was made to the category's value."
        elif diff > 0:
            output = "You added an additional ${:,.2f} to the {} category's" \
                     " value.".format(diff, self.name)
        elif diff < 0:
            output = "You subtracted ${:,.2f} from the {} category's" \
                     " value.".format(diff*(-1), self.name)

        print("\n%s" % output)
        cur.close()
        press_key_to_continue()

    @staticmethod
    def menu_for_categories():
        """Provide user with information regarding the category menu then
        direct them to the appropriate functions."""

        # TODO: Within Category_instance_menu, add option to view transactions associated with the selected category.
        # TODO: Within Category_instance_menu, add option to create a new transaction with that category.

        print("\n~~You are now in the categories menu.~~")
        while True:
            choice = recite_menu_options(CATEGORY_MENU_OPTIONS)
            if choice == 1:
                Category.display_categories()
            elif choice == 2:
                Category.new_category()
            elif choice == 3:
                instance = Category.choose_category()
                if instance is not None:
                    # Object instance is now in memory.
                    # Present user with category instance menu.
                    while True:
                        # Display the selected Category's attributes at the
                        # top of the menu.
                        minus = "   -$" if instance.value < 0 else "    $"
                        output = "{}{}{:>,.2f}".format(
                                instance.name,
                                minus,
                                abs(instance.value)
                                )
                        print()
                        print("-"*len(output))
                        print(output)
                        print("-"*len(output))
                        choice2 = recite_menu_options(
                            CATEGORY_INSTANCE_OPTIONS)
                        if choice2 == 1:
                            instance.update_category_name()
                        elif choice2 == 2:
                            instance.update_category_value()
                        elif choice2 == 3:
                            confirmation = instance.delete_category()
                            if confirmation == 1:
                                break
                        elif choice2 == 4:
                            break
                    print("\n~~You are now returning to the category menu.~~")
            elif choice == 4:
                break

# ____________________________________________________________________________#


class Transaction:

    def __init__(self, uid, account, category, amount, payee, date, memo):
        self.uid = uid
        self.account = account
        self.category = category
        self.amount = amount
        self.payee = payee
        self.date = date
        self.memo = memo

    @staticmethod
    def new_transaction():
        """Prompt the user to complete the fields and then create a transaction
        with that information. By design, this method does not restrict the
        user from entering an amount that would cause the category's value
        to become negative, but it does restrict the user from entering an
        amount that would cause the account's balance to become negative."""

        # Verify that at least one account and at least one category exist.
        cur = conn.cursor()
        cur.execute("SELECT name, balance FROM Accounts")
        account_list = cur.fetchall()
        if len(account_list) == 0:
            # Accounts table is empty. Direct user back to transactions menu.
            output = "You have no accounts. Try again once you've created" \
                     " at least one account and at least one category."
            print("\n%s" % output)
            cur.close()
            press_key_to_continue()
            return
        cur.execute("SELECT name, value FROM Categories")
        category_list = cur.fetchall()
        if len(category_list) == 0:
            # Categories table is empty. Direct user back to transactions menu.
            output = "You have no categories. Try again once you've created" \
                     " at least one account and at least one category."
            print("\n%s" % output)
            cur.close()
            press_key_to_continue()
            return
        # Instantiate the Transactions class, to be filled in piece by piece.
        instance = Transaction(None, None, None, None, None, None, None)


        # Determine whether transaction is an inflow or an outflow.
        output = "\nWhat type of transaction is this?" \
                 "\n\t1) Income\n\t2) Expense"
        print(output)
        output = "Enter the corresponding number of your answer, or" \
                 " enter 0 to cancel: "
        is_expense = input_validation(
            output,
            int,
            num_lb=0,
            num_ub=2
        )
        if is_expense == 0:
            # User wants to cancel.
            print("\nCanceling this transaction.")
            press_key_to_continue()
            cur.close()
            return
        # Map the input value for is_expense to True (1) or False (0).
        is_expense -= 1
        if is_expense:
            print("\nTransaction type: Expense")
        else:
            print("\nTransaction type: Income")


        # Ask user to choose an amount.
        output = "What is the amount of this transaction?" \
                 " Enter a blank line to cancel: "
        amount = input_validation(
            output,
            float,
            num_lb=0,
            empty_string_allowed=True
        )
        if amount == '':
            # User wants to cancel.
            print("\nCanceling this transaction.")
            cur.close()
            press_key_to_continue()
            return
        # Amount is valid, but may have extra decimal places (beyond 2).
        amount = round(amount, 2)
        output = "Amount entered: ${:,.2f}".format(amount)
        print("\n%s" % output)
        instance.amount = amount * -1 if is_expense else amount


        # Ask user to choose an account.
        print("Choose an account to fund this transaction with.")
        for i in range(len(account_list)):
            print("\t%d)" % (i + 1), account_list[i][0])
        output = "Enter the number in front of the account you want " \
                 "to select, or enter 0 to cancel: "
        account_num = input_validation(
            output,
            int,
            num_lb=0,
            num_ub=len(account_list)
            )
        if account_num == 0:
            # User wants to cancel.
            print("\nCanceling this transaction.")
            cur.close()
            press_key_to_continue()
            return
        else:
            if abs(instance.amount) > account_list[
                        account_num- 1][1] and is_expense == True:
                output = "\nThe selected account's balance is too low" \
                         " (${:,.2f}). Please add at least ${:,.2f} to the" \
                         " account and then try again.".format(
                    account_list[account_num- 1][1],
                    abs(instance.amount) - account_list[account_num- 1][1])
                print(output)
                print("\nCanceling this transaction.")
                cur.close()
                press_key_to_continue()
                return
            else:
                output = "\nAccount selected: {}".format(
                    account_list[account_num-1][0])
                print(output)
                instance.account = account_list[account_num-1][0]


        # Ask user to choose a category.
        assign_category = True
        if not is_expense:
            # Category is optional.
            output = "Since this is an income transaction, assigning" \
                     " a category to it is optional."
            print(output)
            output = "Would you like to assign a category to this" \
                     " transaction? Enter 1 for 'Yes' and 0 for 'No': "
            assign_category = input_validation(
                output,
                int,
                num_lb=0,
                num_ub=1
            )
        if assign_category:
            print("Assign a category to this transaction.")
            for i in range(len(category_list)):
                print("\t%d)" % (i + 1), category_list[i][0])
            output = "Enter the number in front of the category you want " \
                     "to select, or enter 0 to cancel: "
            category_num = input_validation(
                output,
                int,
                num_lb=0,
                num_ub=len(category_list)
                )
            if category_num == 0:
                # User wants to cancel.
                print("\nCanceling this transaction.")
                cur.close()
                press_key_to_continue()
                return
            else:
                output = "\nCategory selected: {}".format(
                    category_list[category_num-1][0])
                print(output)
                instance.category = category_list[category_num-1][0]


        # Ask the user to select a payee.
        # Ask the user to select a date.
        # Ask the user to add a memo (optional).


        # Now assign a UID to the transaction.
        cur.execute("SELECT MAX(uid) FROM Transactions")
        uid_max = cur.fetchall()
        instance.uid = 1 if uid_max[0][0] == None else uid_max[0][0] + 1


        # It's finally time to add this record to the database.
        cur.execute('INSERT INTO Transactions VALUES(?,?,?,?,?,?,?)', (
            instance.uid,
            instance.account,
            instance.category,
            instance.amount,
            instance.payee,
            instance.date,
            instance.memo
            )
        )
        conn.commit()


        # Update the category's value (or unassigned_funds value).
        if instance.category is not None:
            cur.execute("SELECT value FROM Categories WHERE name=?",
                        (instance.category,))
            temp = cur.fetchall()[0][0]
            cur.execute("UPDATE Categories SET value=? WHERE name=?",
                        (temp + instance.amount, instance.category))
            conn.commit()
        else:
            # Since the transaction doesn't deduct funds from any category,
            # it must instead deduct funds from unassigned_funds.
            Category.unassigned_funds += instance.amount


        # Update the account's value, as well as total_account_balance.
        cur.execute("SELECT balance FROM Accounts WHERE name=?",
                    (instance.account,))
        temp = cur.fetchall()[0][0]
        cur.execute('UPDATE Accounts SET balance=? WHERE name=?',
                    (temp + instance.amount, instance.account))
        conn.commit()
        Account.total_account_balance += instance.amount


        # Inform the user of success.
        print("Your transaction has been successfully added!")
        cur.close()
        press_key_to_continue()


    def delete_transaction(self):
        """Ask user for confirmation before deleting, and then delete."""

        # TODO: Currently shows uid at the end, show different attribute(s) instead.
        # TODO: When deleting transactions whose amounts are positive, need to worry about account balance going negative? What about unassigned_funds?

        # Ask the user to confirm that the transaction should be deleted.
        # If yes, then delete it.
        output = "Are you sure that you want to delete this transaction?" \
               " Enter 1 for yes, 0 for no: "

        confirmation = input_validation(
            output,
            int,
            num_lb=0,
            num_ub=1
            )

        if confirmation:
            # Delete the transaction.
            cur = conn.cursor()
            cur.execute("SELECT balance FROM Accounts WHERE name=?",
                        (self.account,))
            temp = cur.fetchall()[0][0]
            cur.execute("UPDATE Accounts SET balance=? WHERE name=?",
                        (temp - self.amount, self.account))
            conn.commit()
            Account.total_account_balance -= self.amount

            if self.category is None:
                # Funds were originally taken from unassigned_funds.
                Category.unassigned_funds -= self.amount
            else:
                # Funds were originally taken from self.category.
                cur.execute("SELECT value FROM Categories WHERE name=?",
                            (self.category,))
                temp = cur.fetchall()[0][0]
                cur.execute("UPDATE Categories SET value=? WHERE name=?",
                            (temp - self.amount, self.category))
                conn.commit()

            cur.execute("DELETE FROM Transactions WHERE uid=?",
                        (self.uid,))
            conn.commit()
            print("\nYou have successfully deleted %s from your"
                  " list of transactions." % self.uid)
            cur.close()
            press_key_to_continue()
        return confirmation

    @staticmethod
    def display_transactions():
        pass

    @staticmethod
    def choose_transaction():
        """This method is called anytime we need an instance of a transaction.
        Once the user selects a transaction, we create an instance of it.
        Then we can call instance methods on that transaction."""

        # TODO: Currently shows only uid, change to a different attribute(s)

        num_transactions = 0
        transactions_dict = {}

        cur = conn.cursor()
        cur.execute("SELECT * FROM Transactions")

        while True:
            try:
                transactions_dict[num_transactions + 1] = cur.fetchone()[0]
            except TypeError:
                # cur.fetchone() returns None at the end of the query,
                # which is non-subscriptable.
                if num_transactions == 0:
                    print(
                        "\nYou have no transactions! You should add some!")
                    press_key_to_continue()
                break
            else:
                if num_transactions == 0:
                    print("\nWhich transaction do you want to select?")
                num_transactions += 1
                print("\t%s)" % num_transactions,
                      transactions_dict[num_transactions])

        if num_transactions > 0:
            choice_number = input_validation(
                "Enter the number in front of the transaction you wish to "
                "select, or enter 0 to cancel: ",
                int,
                num_lb=0,
                num_ub=num_transactions
            )

            if choice_number > 0:
                # Create object instance and copy data into memory.
                cur.execute("SELECT * FROM Transactions WHERE uid=?",
                            (transactions_dict[choice_number],))
                temp = cur.fetchall()[0]
                selected_transaction = Transaction(
                    uid=temp[0],
                    account=temp[1],
                    category=temp[2],
                    amount=temp[3],
                    payee=temp[4],
                    date=temp[5],
                    memo=temp[6]
                    )
                print("\nYou have selected the {} transaction.".format(
                    selected_transaction.uid))
                cur.close()
                press_key_to_continue()
                return selected_transaction

        cur.close()
        return None


    def update_transaction_payee(self):
        pass

    def update_transaction_category(self):
        pass

    def update_transaction_account(self):
        pass

    def update_transaction_memo(self):
        pass

    def update_transaction_amount(self):
        pass

    def update_transaction_date(self):
        pass

    @staticmethod
    def menu_for_transactions():
        """Provide user with information regarding the transactions menu then
         direct them to the appropriate functions."""

        # TODO: Change the 'header' information at the top of the transaction_instance menu.

        print("\n~~You are now in the transactions menu.~~")
        while True:
            choice = recite_menu_options(TRANSACTION_MENU_OPTIONS)
            if choice == 1:
                Transaction.display_transactions()
            elif choice == 2:
                Transaction.new_transaction()
            elif choice == 3:
                instance = Transaction.choose_transaction()
                if instance is not None:
                    # Object instance is now in memory.
                    # Present user with transaction instance menu.
                    while True:
                        # Display the selected transaction's attributes at the
                        # top of the menu.
                        output = "Payee: {}    Amount: ${:>,.2f}    " \
                                 "Category: {}    Account: {}".format(
                            instance.payee,
                            instance.amount,
                            instance.category,
                            instance.account
                            )
                        print()
                        print("-" * len(output))
                        print(output)
                        print("-" * len(output))
                        choice2 = recite_menu_options(
                            TRANSACTION_INSTANCE_OPTIONS)
                        if choice2 == 1:
                            instance.update_transaction_account()
                        elif choice2 == 2:
                            instance.update_transaction_category()
                        elif choice2 == 3:
                            instance.update_transaction_amount()
                        elif choice2 == 4:
                            instance.update_transaction_payee()
                        elif choice2 == 5:
                            instance.update_transaction_date()
                        elif choice2 == 6:
                            instance.update_transaction_memo()
                        elif choice2 == 7:
                                confirmation = instance.delete_transaction()
                                if confirmation == 1:
                                    break
                        elif choice2 == 8:
                            break
                    print("\n~~You are now returning to the "
                          "transaction menu.~~")
            elif choice == 4:
                break

# ____________________________________________________________________________#


class Account:

    # TODO: Balance and Starting Balance should be two different attributes of each account instance. Alternatively, SB could be implemented as a transaction (like what YNAB does).
    # TODO: Implement choose_account method and account_instance_menu, just like categories. Except don't include update_account_balance (instead offer to create new transaction with this account).
    # TODO: Accounts should never be allowed to have negative balances. This ensures that unassigned_funds is never negative. This program doesn't allow for credit cards!

    total_account_balance = 0

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    @classmethod
    def new_account(cls):
        """Prompt the user for a name and a number, then create an account
         with that name and balance."""

        # TODO: Implement starting account balance as a transaction. Automatically set payee as "Starting Balance"

        while True:
            name = input_validation(
                "\nWhat do you want to call your new account?"
                " Enter a blank line to cancel: ",
                str,
                empty_string_allowed=True
            )

            if name == '':
                # User wants to cancel this decision.
                return
            cur = conn.cursor()
            cur.execute("SELECT name FROM Accounts WHERE name=?", (name,))
            check = cur.fetchall()
            # Returns an empty list if the user-supplied name doesn't
            # appear in the Accounts table
            if not check:
                # The name which the user entered is not in the Accounts table.
                break
            else:
                print("\nAn account already exists with that name. "
                      "Please choose a different name.\n")
                continue

        # Now that the name is accepted, prompt the user to add
        # a starting account balance.
        balance = input_validation(
            "Please enter a starting account balance (must be non-negative): ",
            float,
            num_lb=0
            )

        # Balance is valid, but may have extra decimal places (beyond 2).
        balance = round(balance, 2)

        # Account name and balance have been approved, so add them to the
        # accounts table in the database.
        cur.execute('INSERT INTO Accounts VALUES(?,?)', (name, balance))
        cur.close()
        conn.commit()

        # Finally, update the class attribute for total account balance.
        cls.total_account_balance += balance
        Category.unassigned_funds += balance

        print("\nOkay! You added a new account called %s to your list!" % name)
        press_key_to_continue()

    @classmethod
    def delete_account(cls):
        """Present user with list of existing accounts, then delete the one
         corresponding to the user's selection."""

        # TODO: Only let users delete accounts with zero transactions (prompt them to handle those transactions themselves).

        num_accounts = 0
        # account_dict maps the user-supplied integer to an account record.
        account_dict = {}

        cur = conn.cursor()
        cur.execute("SELECT name FROM Accounts")

        while True:
            try:
                account_dict[num_accounts + 1] = cur.fetchone()[0]
            except TypeError:
                # cur.fetchone() returns None at the end of the query,
                # which is non-subscriptable.
                if num_accounts == 0:
                    print("\nYou have no accounts! You should add some!")
                    press_key_to_continue()
                break
            else:
                if num_accounts == 0:
                    print("\nWhich account do you want to delete?")
                num_accounts += 1
                print("\t%s)" % num_accounts, account_dict[num_accounts])

        if num_accounts > 0:
            choice_number = input_validation(
                "Enter the number in front of the account you wish to delete,"
                " or enter 0 to cancel: ",
                int,
                num_lb=0,
                num_ub=num_accounts
            )

            if choice_number > 0:

                cur.execute("SELECT balance FROM Accounts WHERE name=?",
                            (account_dict[choice_number],))
                temp = cur.fetchall()[0][0]

                # Check to see if unassigned funds will become negative.
                # If so, prompt user to change category values first.
                if Category.unassigned_funds - temp < 0:
                    output = "This account's balance (${:,.2f}) exceeds the" \
                             " amount of unassigned funds (${:,.2f}), so it" \
                             " can't be deleted yet.".format(
                                temp,
                                Category.unassigned_funds
                                )
                    print("\n%s" % output)
                    output = "Please free up at least ${:,.2f} from your" \
                             " categories' values before deleting this" \
                             " account.".format(temp-Category.unassigned_funds)
                    print(output)

                else:
                    # Update class attribute before deleting record from table.
                    cls.total_account_balance -= temp
                    Category.unassigned_funds -= temp

                    # Now okay to delete record.
                    cur.execute("DELETE FROM Accounts WHERE name=?",
                                (account_dict[choice_number],))
                    conn.commit()

                    print("\nYou have successfully deleted %s from your list"
                          " of accounts." % account_dict[choice_number])

                press_key_to_continue()
        cur.close()

    @classmethod
    def display_accounts(cls):
        """Query the names and balances of the user's accounts and present them
        in a vertical list."""

        # TODO: Use with statement to open and close the cursor.
        # TODO: Fix floating point errors for large numbers. Use "decimal" module?

        # Here is how to interpret the string format specifiers below:
        # Let's look at {:>#{pad2},.2f} as an example.
        # The ':' means the following characters are 'format_specs'.
        # The '>' means right-justified.
        # The '{pad2}' is a nested format specifier.
        #   Here it simply contains a variable.
        # The ',' groups the digits into sets of 3, separated by a comma.
        # The '.2f' means show two digits after the decimal place.
        #   Note that the 'f' in '.2f' specifies fixed point.

        cur = conn.cursor()
        cur.execute("SELECT name, balance FROM Accounts")
        instance_list = [Account(name=i[0], balance=i[1])
                         for i in cur.fetchall()]

        if len(instance_list) == 0:
            # The Accounts table contains no data
            print("\nYou have no accounts! You should add some!")
            cur.close()
            press_key_to_continue()
            return

        # Now determine the longest name and balance (when printed).
        total_balance_string = "{:,.2f}".format(cls.total_account_balance)
        max_balance_length = len(total_balance_string)
        max_name_length = 13        # 13 is the length of "Total balance".
        for account in instance_list:
            if len(account.name) > max_name_length:
                max_name_length = len(account.name)

        # Print each account row by row.
        print("\nHere are your accounts and their balances:")
        for account in instance_list:
            output = "{:{pad1}}    ${:>{pad2},.2f}".format(
                account.name,
                account.balance,
                pad1=max_name_length,
                pad2=max_balance_length
                )
            print("\t%s" % output)

        # Finally, display the total account balance.
        final_line_output = "{:{pad1}}    ${:>{pad2},.2f}".format(
            "Total Balance",
            cls.total_account_balance,
            pad1=max_name_length,
            pad2=max_balance_length)
        print("\t%s" % ("-"*len(final_line_output)))
        print("\t%s" % final_line_output)

        cur.close()
        print()
        press_key_to_continue()

    @staticmethod
    def menu_for_accounts():
        """Provide user with information regarding the accounts menu then
        direct them to the appropriate functions."""

        print("\n~~You are now in the accounts menu.~~")

        while True:

            choice = recite_menu_options(ACCOUNT_MENU_OPTIONS)

            if choice == 1:
                Account.display_accounts()

            elif choice == 2:
                Account.new_account()

            elif choice == 3:
                Account.delete_account()

            elif choice == 4:
                break

# ____________________________________________________________________________#


def main():
    """Main menu of the program, acting as 'central hub' through which users
    navigate to get to all other parts."""

    # TODO replace 'cur.fetchall()[0][0]' with a better sqlite3 method.
    # TODO: Instead of 'conn' being a global variable, make it a class attribute of some class (?)

    global conn

    # All files affiliated with this program will be located at the path
    # stored in CONFIG_DIRECTORY.
    if not os.path.exists(CONFIG_DIRECTORY):
        os.makedirs(CONFIG_DIRECTORY)

    user_budgets = os.path.join(CONFIG_DIRECTORY, "User Budgets")
    if not os.path.exists(user_budgets):
        os.makedirs(user_budgets)

    # Here is where the user experience begins:
    print("\nWelcome to Ben's Budget Program!")
    while True:
        conn = which_budget(user_budgets)

        # Now that a budget is selected, update the total account balance.
        cur = conn.cursor()
        cur.execute("SELECT SUM(balance) FROM Accounts")
        Account.total_account_balance = cur.fetchall()[0][0]

        # A brand new budget has no data, so cur.fetchall returns None.
        if Account.total_account_balance is None:
            Account.total_account_balance = 0

        # Also update the unassigned funds.
        cur.execute("SELECT SUM(value) FROM Categories")
        temp = cur.fetchall()[0][0]

        # A brand new budget has no data, so cur.fetchall returns None.
        if temp is None:
            temp = 0
        Category.unassigned_funds = Account.total_account_balance - temp
        cur.close()

        while True:
            choice = recite_menu_options(MAIN_MENU_OPTIONS)
            if choice == 1:
                Category.menu_for_categories()
            elif choice == 2:
                Transaction.menu_for_transactions()
            elif choice == 3:
                Account.menu_for_accounts()
            elif choice == 4:
                print("\n~~"
                      "You are now returning to the budget selection menu.~~")
                conn.close()
                break
            print("\n~~You are now returning to the main menu.~~")

# ____________________________________________________________________________#


def which_budget(user_budgets):
    """Top-level menu, determines which budget (database) to connect to."""

    # TODO: Make filenames distinct from user-supplied budget names. Then no need to limit user's input!
    # TODO: Provide option to delete an existing budget.

    while True:
        choice = recite_menu_options(WHICH_BUDGET_MENU_OPTIONS)
        if choice == 1:
            # The user wants to create a brand new budget.
            while True:
                budget_name = input_validation(
                    "\nPlease choose a name for your new budget, "
                    "or enter a blank line to cancel: ",
                    str,
                    str_bad_chars=('.', ':', '/'),
                    str_bad_chars_positions=(0, None, None),
                    empty_string_allowed=True
                )

                # Now confirm that there isn't an existing budget that
                # already has that name.
                if os.path.isfile(os.path.join(
                        user_budgets, budget_name + '.db')):
                    print("\nA budget already exists with that name. "
                          "Please enter a different name.")
                else:
                    break
            if budget_name == "":
                # User wants to cancel. Loop to top of this function.
                continue
            # Name has been approved, proceed with setting up new database
            # and connecting to it.
            connection = sqlite3.connect(
                os.path.join(user_budgets, budget_name + '.db'))
            cur = connection.cursor()
            cur.execute('CREATE TABLE Categories('
                        'name TEXT,'
                        'value REAL)'
                        )
            cur.execute('CREATE TABLE Accounts('
                        'name TEXT,'
                        'balance REAL)'
                        )
            cur.execute('CREATE TABLE Transactions('
                        'uid INTEGER,'
                        'account TEXT,'
                        'category TEXT,'
                        'amount REAL,'
                        'payee TEXT,'
                        'date TEXT,'
                        'memo TEXT)'
                        )
            cur.close()
            connection.commit()
            print("\nGreat! You have created a brand new budget called %s."
                  % budget_name)
            break

        if choice == 2:
            # The user wants to load an existing budget.
            list_of_budgets = glob.glob(
                "%s/*.db" % user_budgets)  # Pull up list of available budgets.
            if len(list_of_budgets) == 0:
                print("\nThere are no existing budgets. "
                      "You should make a new one!")
            else:
                print("\nWhich budget would you like to load?")
                for i in range(len(list_of_budgets)):
                    print("\t%d)" % (i + 1), os.path.splitext(
                        os.path.basename(list_of_budgets[i]))[0])
                budget_number = input_validation(
                    "Enter the number in front of the budget you wish to load,"
                    " or enter 0 to cancel: ",
                    int,
                    num_lb=0,
                    num_ub=len(list_of_budgets)
                )

                if budget_number > 0:
                    # Load the budget that corresponds to the number
                    # the user entered.
                    connection = sqlite3.connect(
                        list_of_budgets[budget_number - 1])
                    print("\nBudget loaded: %s" % os.path.splitext(
                        os.path.basename(list_of_budgets[
                                             budget_number - 1]))[0])
                    break

        if choice == 3:
            # User wants to delete an existing budget.
            list_of_budgets = glob.glob(
                "%s/*.db" % user_budgets)  # Pull up list of available budgets.
            if len(list_of_budgets) == 0:
                print("\nThere are no existing budgets. "
                      "You should make a new one!")
            else:
                print("\nWhich budget would you like to delete?")
                for i in range(len(list_of_budgets)):
                    print("\t%d)" % (i + 1), os.path.splitext(
                        os.path.basename(list_of_budgets[i]))[0])
                budget_number = input_validation(
                    "Enter the number in front of the budget you wish to"
                    " delete, or enter 0 to cancel: ",
                    int,
                    num_lb=0,
                    num_ub=len(list_of_budgets)
                )

                if budget_number > 0:
                    # Ask the user to confirm their choice.
                    selected_budget = os.path.splitext(os.path.basename(
                            list_of_budgets[budget_number - 1]))[0]
                    output = "Are you sure you want to delete {}? Press 1" \
                             " for yes, 0 for no: ".format(selected_budget)
                    confirmation = input_validation(
                        output,
                        int,
                        num_lb=0,
                        num_ub=1
                    )
                    if confirmation:
                        # Delete the budget that corresponds to the number
                        # the user entered.
                        os.remove(list_of_budgets[budget_number-1])
                        print("\nBudget deleted: {}".format(selected_budget))
                        press_key_to_continue()

        if choice == 4:
            # Quit the program!
            exit_program()

    press_key_to_continue()
    return connection

# ____________________________________________________________________________#


def recite_menu_options(list_of_options):
    """Present user with a series of options and make them choose one."""

    # TODO: Above each menu, show the relevant info like how the category_instance_menu is currently. So show budget name above main menu, 'categories' above category_menu, etc.

    print("\nWhat would you like to do?")
    for i in range(len(list_of_options)):
        print("Press %d to %s" % (i + 1, list_of_options[i]))

    return input_validation(
        "Enter your choice here: ",
        int,
        num_lb=1,
        num_ub=len(list_of_options)
    )

# ____________________________________________________________________________#


def input_validation(
        prompt,
        input_type,
        num_lb=float('-inf'),
        num_ub=float('inf'),
        str_bad_chars=None,
        str_bad_chars_positions=None,
        empty_string_allowed=False
        ):

    """
    Receive user input and verify that it's valid before returning it.

    :param prompt: The message that the user sees when prompted for input.
    :param input_type: The type of input that the user should enter.
    :param num_lb: The lower bound (inclusive) of input, if numerical.
    :param num_ub: The upper bound (inclusive) of input, if numerical.
    :param str_bad_chars: Any characters which are forbidden, if input is text.
    :param str_bad_chars_positions: The corresponding positions of the
            characters in str_bad_chars. If no position is specified for a
            character, this value is 'None'.
    :param empty_string_allowed: Flag to specify whether the empty string
            is acceptable input.
    :return: The user input, once confirmed that it's acceptable.
    """

    while True:

        error_output = None

        user_input = input(prompt).strip()
        # user_input is a string.

        # First check for empty string.
        if user_input == '':
            # Determine if empty string is acceptable.
            if empty_string_allowed:
                # User input is good to go.
                break
            else:
                print("\nInvalid entry, please try again.\n")
                continue

        if input_type is str:

            if str_bad_chars is None:
                # No forbidden characters, so user input is good to go.
                break

            for i in range(len(str_bad_chars)):
                # Make sure each member of str_bad_chars doesn't
                # appear in the input at the wrong position.
                if str_bad_chars_positions[i] is None:
                    # str_bad_chars[i] is not allowed anywhere within string.
                    if str_bad_chars[i] in user_input:
                        # Reject input.
                        error_output = "Invalid entry, cannot contain" \
                                       " {}".format(
                                        str_bad_chars[i]
                                        )
                        break

                else:
                    # str_bad_chars[i] is not allowed at the specific location
                    # specified by str_bad_chars_positions[i], but allowed
                    # elsewhere.
                    if str_bad_chars[i] in user_input[
                            str_bad_chars_positions[i]]:
                        # Reject input.
                        error_output = "Invalid entry, character at position" \
                                       " {} cannot be '{}'".format(
                                        str_bad_chars_positions[i],
                                        str_bad_chars[i]
                                        )
                        break

            if error_output is not None:
                print("\n%s" % error_output)
                continue

        elif input_type is int:
            try:
                user_input = int(user_input)
            except ValueError:
                print("\nInvalid entry, please try again.\n")
                continue
            # Now check to make sure user_input is in range.
            if (user_input < num_lb) or (user_input > num_ub):
                error_output = "Invalid entry, must be between {} and" \
                         " {} (inclusive).\n".format(
                            num_lb,
                            num_ub
                            )
                print("\n%s" % error_output)
                continue

        else:
            # input_type is float.
            try:
                user_input = float(user_input)
            except ValueError:
                print("\nInvalid entry, please try again.\n")
                continue
            # Now check to make sure user_input is in range.
            if (user_input < num_lb) or (user_input > num_ub):
                error_output = "Invalid entry, must be between {:,.2f} and" \
                         " {:,.2f} (inclusive).\n".format(
                            num_lb,
                            num_ub
                            )
                print("\n%s" % error_output)
                continue
            # Finally, if '-0' was entered, turn into +0.
            user_input += 0

        # user_input is good to go.
        break

    return user_input

# ____________________________________________________________________________#


def press_key_to_continue():
    """Prompts the user to hit a button before displaying the next menu."""
    input("Press Enter to continue... ")
    print()     # Prints a blank line.

# ____________________________________________________________________________#


def exit_program():
    """Exit the program gracefully (with exit code 0)."""

    print("\nThanks for using Ben's Budget Program. See you later!")
    try:
        conn.close()
    except NameError:
        # The variable conn was never set.
        pass
    raise SystemExit

# ____________________________________________________________________________#


if __name__ == "__main__":
    main()

"""
Here are ideas of next steps and features:
-Implement some sense of time. Consider making the time frame variable, based on user input.
-Allow users to create their own subsets of categories (distinct from the idea of super-categories).
    -Allow users to see spending patterns/trends in just that subset.
-Use regular expressions to check user input (and make sure it's valid).
-Implementing classes and OOP instead of procedural programming:
    Make a Menu class.
        And then each menu can be its own object, with its own list of options stored as an attribute.
        The user's input choice should be stored as an attribute.
        But how can I avoid the if...elif...elif... chains in the functions that call recite_menu_options() ?
    Once I implement classes in my code, it might make sense to incorporate an Object-Relational Mapping (ORM) to replace my SQL commands.
-Implement config files
    config files save user preferences ("configurations")
    Module: configparser
    ~/Library/Application Support/Bens Budget Program
-How restricted should the user be regarding entering in transaction amounts?
    -Answer: Let the user decide! Make it a configuration thing.
        -Add a settings/configurations/properties/preferences menu.
    -For now, default to letting categories go negative, but not accounts.
"""