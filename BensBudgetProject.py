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
from datetime import date as dt
import re
from abc import ABCMeta

# Bash uses ~ to mean the home directory, but Python doesn't know that.
# That's why we use os.path.expanduser() in the following command.
CONFIG_DIRECTORY = os.path.expanduser(
    '~/Library/Application Support/Bens Budget Program')

WHICH_BUDGET_MENU_OPTIONS = ["make a new budget.",
                             "load an existing budget.",
                             "delete an existing budget.",
                             "quit the program.",
                             ]

MAIN_MENU_OPTIONS = ["go to the category menu.",
                     "go to the transactions menu.",
                     "go to the accounts menu.",
                     "choose a different budget or quit the program.",
                     ]

CATEGORY_MENU_OPTIONS = ["see your list of budget categories.",
                         "add a new category.",
                         "modify an existing category.",
                         "return to the main menu.",
                         ]

CATEGORY_INSTANCE_OPTIONS = ["edit the category's name.",
                             "edit the category's value.",
                             "view all transactions for this category.",
                             "delete the category.",
                             "return to the category menu.",
                             ]

ACCOUNT_MENU_OPTIONS = ["see your list of accounts.",
                        "add a new account.",
                        "modify an existing account.",
                        "return to the main menu.",
                        ]

ACCOUNT_INSTANCE_OPTIONS = ["edit the account's name.",
                            "view all transactions for this account.",
                            "delete the account.",
                            "return to the account menu.",
                            ]

TRANSACTION_MENU_OPTIONS = ["view your transactions.",
                            "add a new transaction.",
                            "modify an existing transaction.",
                            "return to the main menu.",
                            ]

TRANSACTION_INSTANCE_OPTIONS = ["edit the transaction's account.",
                                "edit the transaction's category.",
                                "edit the transaction's amount.",
                                "edit the transaction's payee.",
                                "edit the transaction's date.",
                                "edit the transaction's memo.",
                                "delete the transaction.",
                                "return to the transaction menu.",
                                ]

# ____________________________________________________________________________#


class BaseClass (metaclass=ABCMeta):

    @classmethod
    def choose_x(cls):
        """Presents the user with a list of all records from the corresponding
        table, asks for a selection, then instantiates the object and returns
        it."""

        # TODO: Use pagination.

        name_lowercase = cls.__name__.lower()
        object_list = cls.database_to_memory()
        if object_list is None:
            return None
        print("Which {} do you want to select?\n".format(name_lowercase))
        cls.print_rows(
            object_list,
            cls.display_col_names,
            show_nums=True)
        print()
        choice_number = input_validation(
            "Enter the number in front of the {} you wish to "
            "select, or enter 0 to cancel: ".format(name_lowercase),
            int,
            num_lb=0,
            num_ub=len(object_list)
            )
        return None if choice_number == 0 else object_list[choice_number - 1]

    @classmethod
    def display_x(
            cls,
            where_clause = '',
            summary_attr=None,
            summary_attr_name=None
            ):

        # TODO: Use with statement to open and close the cursor.
        # TODO: Fix floating point errors for large numbers. Use "decimal" module?
        # TODO: If categories have negative balances, alert the user.

        name_lowercase = cls.__name__.lower()
        object_list = cls.database_to_memory(where_clause)
        if object_list is None:
            return
        print("\nHere is your {} list:\n".format(name_lowercase))
        cls.print_rows(
            object_list,
            cls.display_col_names,
            )
        print()

        # Now show an (optional) summary metric.
        if summary_attr is not None:
            minus = "-$" if summary_attr < 0 else "$"
            concat = minus + "{:,.2f}".format(abs(summary_attr))
            output = "Your {} is currently {}.".format(
                summary_attr_name,
                concat,
                )
            print(output)
        press_key_to_continue()

    @classmethod
    def database_to_memory(cls, where_clause=''):
        """Queries the entire database table corresponding to the class
        which calls this method, instantiates objects for every record returned
        from the database, and returns all the objects in a list."""
        object_list = []

        cur = conn.cursor()
        sql = "SELECT * FROM {} {}".format(cls.table_name, where_clause)
        cur.execute(sql)
        query_results = cur.fetchall()

        if len(query_results) == 0:
            print("\nYou have none! Try again when you've created at"
                  " least one {}.".format(cls.__name__.lower()))
            press_key_to_continue()
            cur.close()
            return None

        for i in query_results:
            object_list.append(cls.instantiate(i))
        cur.close()
        return object_list

    @staticmethod
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

        max_list = []
        top = ""
        num = 1

        # The following variables can be tweaked to change the formatting
        # of the output.
        left_margin = 5
        gap = 6

        for column in col_names:
            max_list.append(len(column))

        # Calculate maximum lengths for each column for formatting purposes.
        for obj in table:
            for i in range(len(col_names)):
                att = getattr(obj, col_names[i])
                if type(att) == str or type(att) == int:
                    compare = str(att)
                elif type(att) == float:
                    minus = "-$" if att < 0 else "$"
                    compare = minus + "{:,.2f}".format(abs(att))
                elif type(att) == dt:
                    compare = "xx/xx/xxxx"
                elif att is None:
                    continue
                else:
                    raise Exception("Ben Katz - developer error.")

                if max_list[i] < len(compare):
                    max_list[i] = len(compare)

        # Print top row and dividing line.
        for i in range(len(col_names)):
            top = top + "{}{:{pad}}".format(
                " "*gap,
                col_names[i].title(),
                pad=max_list[i],
                )
        top = top.lstrip()
        print("{}{}".format(" "*left_margin, top))
        print("{}{}".format(" "*left_margin, "-"*len(top)))

        # Now print all the other rows.
        for obj in table:
            output = ""
            for i in range(len(col_names)):
                att = getattr(obj, col_names[i])
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
                        pad=max_list[i],
                        )
                else:
                    output = output + "{}{:{pad}}".format(
                        " "*gap,
                        concat,
                        pad=max_list[i],
                        )
            output = output.strip()
            if show_nums:
                temp = str(num) + ")"
                print("{:{pad}}{}".format(
                    temp,
                    output,
                    pad=left_margin),
                    )
                num += 1
            else:
                print("{}{}".format(" "*left_margin, output))


    def update_attribute(self, attr_str):

        cur = conn.cursor()

        titlecase = False
        flag = False
        lower = float('-inf')
        upper = float('inf')
        empty = True
        output = "Enter a new {} for this {} (or enter a blank line" \
                 " to cancel): ".format(
                    attr_str,
                    self.__class__.__name__.lower()
                    )

        if self.__class__.__name__ == 'Category':
            primary_key_name = 'name'
            primary_key_value = self.name
        elif self.__class__.__name__ == 'Transaction':
            primary_key_name = 'uid'
            primary_key_value = self.uid
        elif self.__class__.__name__ == 'Account':
            primary_key_name = 'name'
            primary_key_value = self.name
        else:
            raise Exception("Ben Katz - developer error.")

        # Report the attribute's current value.
        old_attr = getattr(self, attr_str)
        new_type = type(old_attr)
        if type(old_attr) == str:
            old_value = old_attr
        elif type(old_attr) == int:
            old_value = old_attr
            empty = False
        elif type(old_attr) == float:
            minus = "-$" if old_attr < 0 else "$"
            old_value = "{}{:,.2f}".format(minus, abs(old_attr))
        elif type(old_attr) == dt:
            old_value = old_attr.strftime('%m/%d/%Y')
        elif old_attr is None:
            old_value = "not set"
            if attr_str == 'memo':
                new_type = str
            elif attr_str == 'category':
                new_type = int
            else:
                raise Exception("Ben Katz - developer error.")
        else:
            raise Exception("Ben Katz - developer error.")

        text = "Your {}'s {} is currently {}.".format(
            self.__class__.__name__.lower(),
            attr_str,
            old_value,
            )
        print("\n%s" % text)

        # If applicable, provide info about limiting input.
        # Check for special cases where value can't be changed right now.
        if self.__class__.__name__ == 'Category' and attr_str == 'value':
            text = "Your total amount of unassigned funds is ${:,.2f}.".format(
                Category.unassigned_funds)
            print(text)
            if old_attr <= 0 and Category.unassigned_funds == 0:
                # In this special case, user can't make any changes.
                print("Since neither of these are positive, you can't update"
                      " the value right now.")
                press_key_to_continue()
                cur.close()
                return

            upper = Category.unassigned_funds + old_attr
            lower = min(0, old_attr)
            if old_attr < 0:
                output = "Select a new amount for the category's value " \
                         "(must be greater than the current amount and " \
                         "preferably non-negative), or a blank line to" \
                         " cancel: "
            else:
                output = "Select a new amount for the category's value " \
                         "(must be non-negative), or a blank line to cancel: "

        elif self.__class__.__name__ == 'Transaction' and attr_str == 'payee':
            titlecase = True
        elif self.__class__.__name__ == 'Transaction' and attr_str == 'memo':
            output = "Enter a new {} for this {} (or enter a blank line" \
                     " to cancel or leave the field empty): ".format(
                        attr_str,
                        self.__class__.__name__.lower(),
                        )
        elif self.__class__.__name__ == 'Transaction' and attr_str == 'amount':
            sql = "SELECT balance FROM Accounts WHERE name=?"
            cur.execute(sql, (self.account,))
            trans_account_bal = cur.fetchall()[0][0]
            lower = ((-1) * trans_account_bal) + self.amount
        elif self.__class__.__name__ == 'Transaction' and (
                        attr_str == 'category' or attr_str == 'account'):
            flag = True
            if attr_str == 'category':
                if self.amount > 0:
                    # Income transaction, allows user to select None
                    # for category.
                    text = "Since this is an income transaction, you can " \
                           "choose to leave the category field blank."
                    print(text)
                    output = "Press 1 to make it blank, 2 to select a " \
                             "category, or 0 to cancel: "
                    choice = input_validation(
                        output,
                        int,
                        num_lb=0,
                        num_ub=2,
                        )
                    if choice == 0:
                        obj = None
                    elif choice == 1:
                        # Create a temporary Categories object whose
                        # attributes are all None.
                        obj = Category.instantiate((None, None))
                    elif choice == 2:
                        obj = Category.choose_x()
                else:
                    obj = Category.choose_x()

            else:
                # Make sure that the transaction's current account can
                # afford to lose the transaction (if it is income).
                cur.execute("SELECT balance FROM Accounts WHERE name=?",
                            (self.account,))
                old_account_bal = cur.fetchall()[0][0]
                if old_account_bal < self.amount:
                    # The old account's balance is too low.
                    print("The balance of this transaction's current account "
                          "would become negative if this transaction were "
                          "to be reassigned. You can't edit the account "
                          "at this time.")
                    press_key_to_continue()
                    cur.close()
                    return

                # User will choose an account (or will choose to cancel).
                # Make sure the account the user selects won't become negative.
                while True:
                    obj = Account.choose_x()
                    if obj is None:
                        break
                    if obj.balance < abs(self.amount) and self.amount < 0:
                        # The new account's balance is too low.
                        print("\nThe balance of the account you selected is"
                              " too low, so you can't select it at this time.")
                        continue
                    break

            if obj is None:
                # User wants to cancel.
                cur.close()
                return
            if obj.name == old_attr:
                # Input is the same as the current value.
                print("\nNo change was made.")
                press_key_to_continue()
                cur.close()
                return
            new_attr = obj.name

        if flag == False:
            while True:
                new_attr = input_validation(
                    output,
                    new_type,
                    num_lb=lower,
                    num_ub=upper,
                    is_titlecased=titlecase,
                    empty_string_allowed=empty,
                    )

                if new_attr == '':
                    # User either wants to cancel this decision, or
                    # clear the field.
                    if attr_str == 'memo' and old_attr is not None:
                        output = "\nWhich action do you want to take?\n\t" \
                                 "1) Clear the field\n\t2) Cancel"
                        print(output)
                        output = "Enter the corresponding number of" \
                                 " your answer: "
                        blank_choice = input_validation(
                            output,
                            int,
                            num_lb=1,
                            num_ub=2,
                            )
                        if blank_choice == 1:
                            # Clear the field.
                            new_attr = None
                        else:
                            # Cancel.
                            cur.close()
                            return
                    else:
                        # The field can't be cleared, so cancel this decision.
                        cur.close()
                        return

                if new_attr == old_attr:
                    # Input is the same as the current value.
                    print("\nNo change was made.")
                    press_key_to_continue()
                    cur.close()
                    return

                if attr_str == primary_key_name:
                    # Need to check if input appears elsewhere in the table.
                    sql = "SELECT name FROM {} WHERE {}=?".format(
                        self.table_name,
                        primary_key_name,
                        )
                    cur.execute(sql, (new_attr,))
                    check2 = cur.fetchall()
                    if len(check2) > 0:
                        text = "A {} already exists with that {}. Please" \
                               " choose a different {}.".format(
                            self.__class__.__name__.lower(),
                            attr_str,
                            attr_str,
                            )
                        print("\n%s" % text)
                        continue
                break

        if self.__class__.__name__ == 'Transaction' and attr_str == "amount":
            # Update associated account balance.
            sql = "UPDATE Accounts SET balance=? WHERE name=?"
            cur.execute(sql, (trans_account_bal + new_attr - old_attr,
                              self.account))
            conn.commit()
            Account.total_account_balance += (new_attr - old_attr)

            # Update associated category value (if there is one).
            sql = "SELECT value FROM Categories WHERE name=?"
            cur.execute(sql, (self.category,))
            temp = cur.fetchall()
            if len(temp) == 0:
                # There is no associated Category for this transaction.
                if new_attr < 0:
                    # Transaction was switched from income to expense, and
                    # it has no category assigned to it.
                    text = "Since you changed this transaction from income " \
                           "to an expense, it now needs a category assigned " \
                           "to it."
                    print("\n%s" % text)

                    cat_obj = Category.choose_x()
                    if cat_obj is None:
                        # User wants to cancel.
                        cur.close()
                        return

                    sql = "UPDATE Transactions SET category=? WHERE uid=?"
                    cur.execute(sql, (cat_obj.name, self.uid))
                    conn.commit()

                    self.category = cat_obj.name

                    # Note that, below, old_attr > 0 and new_attr < 0 always.
                    sql = "SELECT value FROM Categories WHERE name=?"
                    cur.execute(sql, (cat_obj.name,))
                    temp = cur.fetchall()[0][0]
                    sql = 'UPDATE Categories SET value=? WHERE name=?'
                    cur.execute(sql, (temp + new_attr, cat_obj.name))
                    conn.commit()

                    # Update unassigned_funds.
                    Category.unassigned_funds -= old_attr
                else:
                    # Update unassigned_funds.
                    Category.unassigned_funds += (new_attr - old_attr)

            else:
                # Update associated category value.
                temp = temp[0][0]
                sql = "UPDATE Categories SET value=? WHERE name=?"
                cur.execute(sql, (temp + new_attr - old_attr, self.category))
                conn.commit()

        elif self.__class__.__name__ == 'Category' and attr_str == "value":
            # Update unassigned_funds.
            Category.unassigned_funds -= (new_attr - old_attr)

        elif (self.__class__.__name__ == 'Transaction' and
                attr_str == "account"):
            # Update old account balance.
            cur.execute('UPDATE Accounts SET balance=? WHERE name=?',
                        (old_account_bal - self.amount, self.account))
            conn.commit()

            # Update new account balance.
            cur.execute("SELECT balance FROM Accounts WHERE name=?",
                        (new_attr,))
            temp = cur.fetchall()[0][0]
            cur.execute('UPDATE Accounts SET balance=? WHERE name=?',
                        (temp + self.amount, new_attr))
            conn.commit()

        elif (self.__class__.__name__ == 'Transaction' and
                attr_str == "category"):
            if old_attr is None:
                # Transaction is income, so self.amount is always > 0.
                Category.unassigned_funds -= self.amount
            else:
                # Update old category value.
                cur.execute("SELECT value FROM Categories WHERE name=?",
                            (self.category,))
                temp = cur.fetchall()[0][0]
                cur.execute('UPDATE Categories SET value=? WHERE name=?',
                            (temp - self.amount, self.category))
                conn.commit()

            if new_attr is None:
                # Transaction is income (not expense).
                Category.unassigned_funds += self.amount
            else:
                # Update new category value.
                cur.execute("SELECT value FROM Categories WHERE name=?",
                            (new_attr,))
                temp = cur.fetchall()[0][0]
                cur.execute('UPDATE Categories SET value=? WHERE name=?',
                            (temp + self.amount, new_attr))
                conn.commit()

        # Update the database for this record.
        sql = "UPDATE {} SET {}=? WHERE {}=?".format(
            self.table_name,
            attr_str,
            primary_key_name,
            )
        cur.execute(sql, (new_attr, primary_key_value))
        conn.commit()

        # Also update the database for other records which depend
        # on this record.
        if attr_str == primary_key_name:
            # Need to update other records which depend on this record.
            sql = "UPDATE Transactions SET {}=? WHERE {}=?".format(
                self.__class__.__name__.lower(),
                self.__class__.__name__.lower(),
                )
            cur.execute(sql, (new_attr, old_attr))
            conn.commit()

        # Update variable in memory
        setattr(self, attr_str, new_attr)

        # Inform the user of the result.
        if type(new_attr) == float:
            minus = "-$" if new_attr < 0 else "$"
            new_value = "{}{:,.2f}".format(minus, abs(new_attr))
        elif type(new_attr) == dt:
            new_value = new_attr.strftime('%m/%d/%Y')
        elif new_attr is None:
            new_value = 'not set'
        else:
            new_value = new_attr

        output = "You have changed the {} {} from {} to {}.".format(
            self.__class__.__name__.lower(),
            attr_str,
            old_value,
            new_value,
            )
        print("\n%s" % output)

        cur.close()
        press_key_to_continue()

# ____________________________________________________________________________#


class Category(BaseClass):

    # unassigned_funds is not ever allowed to become negative.
    unassigned_funds = 0
    unassigned_funds_name = "Unassigned Funds"
    table_name = "Categories"
    display_col_names = [
        "name",
        "value",
        ]


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
                empty_string_allowed=True,
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
                num_ub=cls.unassigned_funds,
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

        # First check to see if there are any transactions for this category.
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Transactions WHERE Category=?",
                    (self.name,))
        temp = cur.fetchone()[0]
        if temp > 0:
            # There are transactions assigned to this category.
            if temp == 1:
                output = "There is 1 transaction assigned to {}. Reassign" \
                         " that transaction to another category or delete" \
                         " it, and then try again.".format(self.name)
            else:
                output = "There are {} transactions assigned to {}. Reassign" \
                        " those transactions to other categories or delete" \
                         " them, and then try again.".format(
                            temp,
                            self.name,
                            )
            print("\n%s" % output)
            cur.close()
            press_key_to_continue()
            confirmation = 0
            return confirmation

        # Ask the user to confirm that the category should be deleted.
        text = "\nAre you sure that you want to delete the" \
               " {} category? ".format(self.name)
        confirmation = input_validation(
            text+"Enter 1 for yes, 0 for no: ",
            int,
            num_lb=0,
            num_ub=1,
            )
        if confirmation == 1:
            # Delete the category.
            Category.unassigned_funds += self.value
            cur.execute("DELETE FROM Categories WHERE name=?", (self.name,))
            conn.commit()
            print("\nYou have successfully deleted %s from your"
                  " list of categories." % self.name)
            cur.close()
            press_key_to_continue()
        return confirmation

    @classmethod
    def menu_for_categories(cls):
        """Provide user with information regarding the category menu then
        direct them to the appropriate functions."""

        # TODO: Within Category_instance_menu, add option to create a new transaction with that category.

        print("\n~~You are now in the categories menu.~~")
        while True:
            menu_header({"CATEGORIES MENU": ""})
            choice = recite_menu_options(CATEGORY_MENU_OPTIONS)
            if choice == 1:
                Category.display_x(
                    summary_attr=cls.unassigned_funds,
                    summary_attr_name=cls.unassigned_funds_name,
                    )
            elif choice == 2:
                Category.new_category()
            elif choice == 3:
                print()
                instance = Category.choose_x()
                if instance is not None:
                    # Object instance is now in memory.
                    # Present user with category instance menu.
                    print("\nYou have selected the {} category.".format(
                            instance.name))
                    press_key_to_continue()
                    while True:
                        menu_header({
                            "Name:": instance.name,
                            "Value:": instance.value,
                            })
                        choice2 = recite_menu_options(
                            CATEGORY_INSTANCE_OPTIONS)
                        if choice2 == 1:
                            instance.update_attribute('name')
                        elif choice2 == 2:
                            instance.update_attribute('value')
                        elif choice2 == 3:
                            Transaction.display_x(
                                'WHERE category="{}"'.format(instance.name))
                        elif choice2 == 4:
                            confirmation = instance.delete_category()
                            if confirmation:
                                break
                        elif choice2 == 5:
                            break
                    print("\n~~You are now returning to the categories"
                          " menu.~~")
            elif choice == 4:
                break

    @staticmethod
    def instantiate(attributes):
        """Given the attribute fields as input, this method instantiates a
        single object and returns it. The database query that produces the
        input is performed elsewhere. The order of the attributes in the
        inputs (represented by the index subscript) must match up with the
        order of the attributes in the code below."""

        return Category(
            name=attributes[0],
            value=attributes[1],
            )

# ____________________________________________________________________________#


class Transaction(BaseClass):

    table_name = "Transactions"
    display_col_names = [
        "payee",
        "amount",
        "date",
        "account",
        "category",
        "memo",
        ]

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
        cur.execute("SELECT COUNT(*) FROM Accounts")
        if cur.fetchall()[0][0] == 0:
            # Accounts table is empty. Direct user back to transactions menu.
            output = "You have no accounts. Try again once you've created" \
                     " at least one account and at least one category."
            print("\n%s" % output)
            cur.close()
            press_key_to_continue()
            return
        cur.execute("SELECT COUNT(*) FROM Categories")
        if cur.fetchall()[0][0] == 0:
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
            num_ub=2,
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
            print("\nTransaction type: Expense.")
        else:
            print("\nTransaction type: Income.")


        # Ask user to choose an amount.
        output = "What is the amount of this transaction?" \
                 " Enter a blank line to cancel: "
        amount = input_validation(
            output,
            float,
            num_lb=0,
            empty_string_allowed=True,
            )
        if amount == '':
            # User wants to cancel.
            print("\nCanceling this transaction.")
            cur.close()
            press_key_to_continue()
            return
        # Amount is valid, but may have extra decimal places (beyond 2).
        amount = round(amount, 2)
        output = "Amount entered: ${:,.2f}.".format(amount)
        print("\n%s" % output)
        instance.amount = amount * -1 if is_expense else amount


        # Ask user to choose an account.
        print("Choose an account to fund this transaction with.")
        account_choice = Account.choose_x()
        if account_choice is None:
            # User wants to cancel.
            print("\nCanceling this transaction.")
            cur.close()
            press_key_to_continue()
            return
        else:
            if abs(instance.amount) > account_choice.balance and is_expense:
                output = "\nThe selected account's balance is too low" \
                         " (${:,.2f}). Please add at least ${:,.2f} to the" \
                         " account and then try again.".format(
                            account_choice.balance,
                            abs(instance.amount) - account_choice.balance,
                            )
                print(output)
                print("Canceling this transaction.")
                cur.close()
                press_key_to_continue()
                return
            else:
                output = "\nAccount selected: {}.".format(account_choice.name)
                print(output)
                instance.account = account_choice.name


        # Ask user to choose a category.
        assign_category = True
        if not is_expense or instance.amount == 0:
            # Category is optional.
            if instance.amount == 0:
                output = "Since this transaction's amount is $0.00," \
                         " assigning a category to it is optional."
            else:
                output = "Since this is an income transaction, assigning" \
                         " a category to it is optional."
            print(output)
            output = "Would you like to assign a category to this" \
                     " transaction? Enter 1 for 'Yes', 0 for 'No': "
            assign_category = input_validation(
                output,
                int,
                num_lb=0,
                num_ub=1,
                )
        if assign_category:
            print("Assign a category to this transaction.")
            category_choice = Category.choose_x()
            if category_choice is None:
                # User wants to cancel.
                print("\nCanceling this transaction.")
                cur.close()
                press_key_to_continue()
                return
            else:
                output = "\nCategory selected: {}.".format(
                    category_choice.name)
                print(output)
                instance.category = category_choice.name
        else:
            print()


        # Ask the user to select a payee.
        output = "Who is the payee for this transaction? Enter a blank" \
                 " line to cancel: "
        payee = input_validation(
            output,
            str,
            is_titlecased=True,
            empty_string_allowed=True,
            )
        if payee == '':
            # User wants to cancel.
            print("\nCanceling this transaction.")
            cur.close()
            press_key_to_continue()
            return
        print("\nPayee entered: {}.".format(payee))
        instance.payee = payee


        # Ask the user to select a date.
        output = "Enter a date for this transaction (MM/DD/YYYY), or a" \
                 " blank line to cancel: "
        date = input_validation(
            output,
            dt,
            empty_string_allowed=True
            )
        if date == '':
            # User wants to cancel.
            print("\nCanceling this transaction.")
            cur.close()
            press_key_to_continue()
            return
        print("\nDate entered: {}.".format(date.strftime("%m/%d/%Y")))
        instance.date = date


        # Ask the user to add a memo (optional).
        output = "Add an (optional) memo here: "
        memo = input_validation(
            output,
            str,
            empty_string_allowed=True,
            )
        if memo != "":
            instance.memo = memo


        # Now assign a UID to the transaction.
        cur.execute("SELECT MAX(uid) FROM Transactions")
        uid_max = cur.fetchall()
        instance.uid = 1 if uid_max[0][0] is None else uid_max[0][0] + 1


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
            # This only happens when transaction is income, not expense.
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
        print("\nYour transaction has been successfully added!")
        cur.close()
        press_key_to_continue()


    def delete_transaction(self):
        """Ask user for confirmation before deleting, and then delete."""

        cur = conn.cursor()
        cur.execute("SELECT balance FROM Accounts WHERE name=?",
                    (self.account,))
        temp = cur.fetchall()[0][0]
        if temp < self.amount:
            # Account balance would become negative, not allowed.
            output = "Deleting this transaction would cause the {}" \
                     " account's balance to become negative. Try again" \
                     " once at least ${:,.2f} is added to the account's" \
                     " current balance.".format(
                        self.account,
                        abs(temp - self.amount)
                        )
            print("\n%s" % output)
            press_key_to_continue()
            confirmation = 0

        elif self.category is None and Category.unassigned_funds < self.amount:
            # unassigned_funds would become negative, not allowed.
            output = "Deleting this transaction would cause the Unassigned" \
                     " Funds to become negative. Try again once at least" \
                     " ${:,.2f}  is added to the Unassigned Funds.".format(
                        abs(Category.unassigned_funds - self.amount)
                        )
            print("\n%s" % output)
            press_key_to_continue()
            confirmation = 0

        else:
            # Ask the user to confirm that the transaction should be deleted.
            output = "\nAre you sure that you want to delete this" \
                     " transaction? Enter 1 for yes, 0 for no: "
            confirmation = input_validation(
                output,
                int,
                num_lb=0,
                num_ub=1,
                )

        if confirmation:
            # Delete the transaction.
            cur.execute("UPDATE Accounts SET balance=? WHERE name=?",
                        (temp - self.amount, self.account))
            conn.commit()
            Account.total_account_balance -= self.amount

            if self.category is None:
                # Funds were originally added to unassigned_funds (income).
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
            print("\nYou have successfully deleted this transaction.")
            press_key_to_continue()

        cur.close()
        return confirmation

    @staticmethod
    def menu_for_transactions():
        """Provide user with information regarding the transactions menu then
         direct them to the appropriate functions."""

        # TODO: Add option for new_transfer (separate method from new_transaction).

        print("\n~~You are now in the transactions menu.~~")
        while True:
            menu_header({"TRANSACTIONS MENU": ""})
            choice = recite_menu_options(TRANSACTION_MENU_OPTIONS)
            if choice == 1:
                Transaction.display_x()
            elif choice == 2:
                Transaction.new_transaction()
            elif choice == 3:
                print()
                instance = Transaction.choose_x()
                if instance is not None:
                    # Object instance is now in memory.
                    # Present user with transaction instance menu.
                    print("\nYou have selected your transaction.")
                    press_key_to_continue()
                    while True:
                        # Display the selected transaction's attributes at the
                        # top of the menu.
                        menu_header({
                            "Payee:": instance.payee,
                            "Amount:": instance.amount,
                            "Date:": instance.date,
                            "Account:": instance.account,
                            "Category:": instance.category,
                            "Memo:": instance.memo,
                            })
                        choice2 = recite_menu_options(
                            TRANSACTION_INSTANCE_OPTIONS)
                        if choice2 == 1:
                            instance.update_attribute('account')
                        elif choice2 == 2:
                            instance.update_attribute('category')
                        elif choice2 == 3:
                            instance.update_attribute('amount')
                        elif choice2 == 4:
                            instance.update_attribute('payee')
                        elif choice2 == 5:
                            instance.update_attribute('date')
                        elif choice2 == 6:
                            instance.update_attribute('memo')
                        elif choice2 == 7:
                            confirmation = instance.delete_transaction()
                            if confirmation:
                                break
                        elif choice2 == 8:
                            break
                    print("\n~~You are now returning to the "
                          "transaction menu.~~")
            elif choice == 4:
                break

    @staticmethod
    def instantiate(attributes):
        """Given the attribute fields as input, this method instantiates a
        single object and returns it. The database query that produces the
        input is performed elsewhere. The order of the attributes in the
        inputs (represented by the index subscript) must match up with the
        order of the attributes in the code below."""

        return Transaction(
            uid=attributes[0],
            account=attributes[1],
            category=attributes[2],
            amount=attributes[3],
            payee=attributes[4],
            date=attributes[5],
            memo=attributes[6],
            )

# ____________________________________________________________________________#


class Account(BaseClass):

    total_account_balance = 0
    tot_account_bal_name = "Total Account Balance"
    table_name = "Accounts"
    display_col_names = [
        "name",
        "balance",
        ]

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    @classmethod
    def new_account(cls):
        """Prompt the user for a name and a number, then create an account
         with that name and balance."""

        while True:
            name = input_validation(
                "\nWhat do you want to call your new account?"
                " Enter a blank line to cancel: ",
                str,
                empty_string_allowed=True,
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
            num_lb=0,
            )

        # Balance is valid, but may have extra decimal places (beyond 2).
        balance = round(balance, 2)

        # Account name and balance have been approved, so add them to the
        # accounts table in the database.
        cur.execute('INSERT INTO Accounts VALUES(?,?)', (name, balance))
        conn.commit()

        # Create a transaction for the starting balance.
        cur.execute("SELECT MAX(uid) FROM Transactions")
        uid_max = cur.fetchall()
        temp_uid = 1 if uid_max[0][0] is None else uid_max[0][0] + 1
        cur.execute("INSERT INTO Transactions Values(?,?,?,?,?,?,?)", (
            temp_uid,
            name,
            None,
            balance,
            "Starting Balance",
            dt.today(),
            None,
            )
        )
        conn.commit()
        cur.close()

        # Finally, update the class attribute for total account balance.
        cls.total_account_balance += balance
        Category.unassigned_funds += balance

        print("\nOkay! You added a new account called %s to your list!" % name)
        press_key_to_continue()

    def delete_account(self):
        """Present user with list of existing accounts, then delete the one
         corresponding to the user's selection."""

        # Confirm that there are zero transactions assigned to this account.
        cur = conn.cursor()
        sql = "SELECT COUNT(*) FROM Transactions WHERE Account=?"
        cur.execute(sql, (self.name,))
        temp = cur.fetchone()[0]
        if temp > 0:
            # There are transactions assigned to this account.
            if temp == 1:
                output = "There is 1 transaction assigned to {}." \
                         " Reassign that transaction to another" \
                         " account or delete it, and then try" \
                         " again.".format(self.name)
            else:
                output = "There are {} transactions assigned to {}." \
                         " Reassign those transactions to other" \
                         " accounts or delete them, and then try" \
                         " again.".format(
                            temp,
                            self.name,
                            )
            print("\n%s" % output)
            cur.close()
            press_key_to_continue()
            confirmation = 0
            return confirmation

        # Ask the user to confirm that the account should be deleted.
        text = "\nAre you sure that you want to delete the {} " \
               "account? ".format(self.name)
        confirmation = input_validation(
            text + "Enter 1 for yes, 0 for no: ",
            int,
            num_lb=0,
            num_ub=1,
            )
        if confirmation == 1:
            # Delete the account.
            cur.execute("DELETE FROM Accounts WHERE name=?", (self.name,))
            conn.commit()
            text = "You have successfully deleted %s from your " \
                   "list of accounts." % self.name
            print("\n%s" % text)
            cur.close()
            press_key_to_continue()
        return confirmation

    @classmethod
    def menu_for_accounts(cls):
        """Provide user with information regarding the accounts menu then
        direct them to the appropriate functions."""

        print("\n~~You are now in the accounts menu.~~")
        while True:
            menu_header({"ACCOUNTS MENU": ""})
            choice = recite_menu_options(ACCOUNT_MENU_OPTIONS)
            if choice == 1:
                Account.display_x(
                    summary_attr=cls.total_account_balance,
                    summary_attr_name=cls.tot_account_bal_name,
                    )
            elif choice == 2:
                Account.new_account()
            elif choice == 3:
                print()
                instance = Account.choose_x()
                if instance is not None:
                    # Object instance is now in memory.
                    # Present user with transaction instance menu.
                    print("\nYou have selected the {} account.".format(
                            instance.name))
                    press_key_to_continue()
                    while True:
                        # Display the selected account's attributes at the
                        # top of the menu.
                        menu_header({
                            "Name:": instance.name,
                            "Balance:": instance.balance,
                            })
                        choice2 = recite_menu_options(
                            ACCOUNT_INSTANCE_OPTIONS)
                        if choice2 == 1:
                            instance.update_attribute('name')
                        elif choice2 == 2:
                            Transaction.display_x(
                                'WHERE account="{}"'.format(instance.name))
                        elif choice2 == 3:
                            confirmation = instance.delete_account()
                            if confirmation:
                                break
                        elif choice2 == 4:
                            break
                    print("\n~~You are now returning to the account menu.~~")
            elif choice == 4:
                break

    @staticmethod
    def instantiate(attributes):
        """Given the attribute fields as input, this method instantiates a
        single object and returns it. The database query that produces the
        input is performed elsewhere. The order of the attributes in the
        inputs (represented by the index subscript) must match up with the
        order of the attributes in the code below."""

        return Account(
            name=attributes[0],
            balance=attributes[1],
            )

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
        conn, budget_name = which_budget(user_budgets)

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
            menu_header({"MAIN MENU:": budget_name})
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

    while True:
        menu_header({"BUDGET SELECTION MENU": ""})
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
                    empty_string_allowed=True,
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
            # The 'detect_types' line allows the DATE type to survive the
            # round-trip from Python to sqlite3 database to Python again.
            connection = sqlite3.connect(
                os.path.join(user_budgets, budget_name + '.db'),
                detect_types=sqlite3.PARSE_DECLTYPES,
                )
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
                        'date DATE,'
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
                press_key_to_continue()
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
                    num_ub=len(list_of_budgets),
                )

                if budget_number > 0:
                    # Load the budget that corresponds to the number
                    # the user entered.
                    # The 'detect_types' line allows the DATE type to
                    # survive the round-trip from Python to sqlite3 database
                    # to Python again.
                    connection = sqlite3.connect(
                        list_of_budgets[budget_number - 1],
                        detect_types=sqlite3.PARSE_DECLTYPES,
                        )
                    budget_name = os.path.splitext(os.path.basename(
                        list_of_budgets[budget_number - 1]))[0]
                    print("\nBudget loaded: %s" % budget_name)
                    break

        if choice == 3:
            # User wants to delete an existing budget.
            list_of_budgets = glob.glob(
                "%s/*.db" % user_budgets)  # Pull up list of available budgets.
            if len(list_of_budgets) == 0:
                print("\nThere are no existing budgets. "
                      "You should make a new one!")
                press_key_to_continue()
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
                    num_ub=len(list_of_budgets),
                )

                if budget_number > 0:
                    # Ask the user to confirm their choice.
                    selected_budget = os.path.splitext(os.path.basename(
                            list_of_budgets[budget_number - 1]))[0]
                    output = "Are you sure you want to delete {}? Press 1" \
                             " for 'Yes', 0 for 'No': ".format(selected_budget)
                    confirmation = input_validation(
                        output,
                        int,
                        num_lb=0,
                        num_ub=1,
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
    return connection, budget_name

# ____________________________________________________________________________#


def recite_menu_options(list_of_options):
    """Present user with a series of options and make them choose one."""

    print("\nWhat would you like to do?")
    for i in range(len(list_of_options)):
        print("Press %d to %s" % (i + 1, list_of_options[i]))

    return input_validation(
        "Enter your choice here: ",
        int,
        num_lb=1,
        num_ub=len(list_of_options),
    )

# ____________________________________________________________________________#


def input_validation(
        prompt,
        input_type,
        num_lb=float('-inf'),
        num_ub=float('inf'),
        str_bad_chars=None,
        str_bad_chars_positions=None,
        is_titlecased=False,
        empty_string_allowed=False,
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
    :param is_titlecased: Specifies whether a string should be made titlecased.
    :param empty_string_allowed: Flag to specify whether the empty string
            is acceptable input.
    :return: The user input, once confirmed that it's acceptable.
    """

    # TODO: Use regexes when input is str, pass regex as argument? Replaces str_bad_chars and str_bad_chars_positions

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

            if is_titlecased:
                user_input = user_input.title()

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
                                       " {}".format(str_bad_chars[i])
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
                                        str_bad_chars[i],
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
                            num_ub,
                            )
                print("\n%s" % error_output)
                continue

        elif input_type is float:
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
                            num_ub,
                            )
                print("\n%s" % error_output)
                continue
            # Finally, if '-0' was entered, turn into +0.
            user_input += 0

        elif input_type is dt:
            # Input type is a datetime.date object.
            # Input should be in MM/DD/YYYY format.
            regex = '^\d\d/\d\d/\d\d\d\d$'
            match = re.search(regex, user_input)
            if not match:
                # User input didn't match the regex.
                error_output = "Invalid entry, must be in 'MM/DD/YYYY' format."
                print("\n%s" % error_output)
                continue
            # User input matched the regex. Convert to datetime.date format.
            temp = user_input.split('/')
            month = int(temp[0])
            day = int(temp[1])
            year = int(temp[2])
            try:
                user_input = dt(month=month, day=day, year=year)
            except ValueError:
                print("\nInvalid entry, not a real date.")
                continue
        else:
            raise Exception("Ben Katz - developer error.")

        # user_input is good to go.
        break

    return user_input

# ____________________________________________________________________________#


def press_key_to_continue():
    """Prompts the user to hit a button before displaying the next menu."""
    input("Press Enter to continue... ")
    print()     # Prints a blank line.

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
    print()
    print("-" * len(output))
    print(output)
    print("-" * len(output))

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