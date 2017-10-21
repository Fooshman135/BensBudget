

class Category:

    table_name = "Categories"

    def __init__(self, name, value):
        self.name = name
        self.value = value


    @staticmethod
    def instantiate(attributes):
        """Given the attribute fields as input, this method instantiates a
        single object and returns it. The database query that produces the
        input is performed elsewhere. The order of the attributes in the
        inputs (represented by the index subscript) must match up with the
        order of the attributes in the code below."""

        return Category(
            name=str(attributes[0]),    # str() is added for Python 2.X users
            value=attributes[1],
            )

    @classmethod
    def menu_for_categories(self):
        pass


class Transaction:

    table_name = "Transactions"

    def __init__(self, uid, account, category, amount, payee, date, memo):
        self.uid = uid
        self.account = account
        self.category = category
        self.amount = amount
        self.payee = payee
        self.date = date
        self.memo = memo


    @staticmethod
    def instantiate(attributes):
        """Given the attribute fields as input, this method instantiates a
        single object and returns it. The database query that produces the
        input is performed elsewhere. The order of the attributes in the
        inputs (represented by the index subscript) must match up with the
        order of the attributes in the code below."""

        # The below two lines are added for Python 2.X users.
        temp_c = attributes[2] if attributes[2] is None else str(attributes[2])
        temp_m = attributes[6] if attributes[6] is None else str(attributes[6])

        return Transaction(
            uid=attributes[0],
            account=str(attributes[1]),   # str() is added for Python 2.X users
            category=temp_c,
            amount=attributes[3],
            payee=str(attributes[4]),     # str() is added for Python 2.X users
            date=attributes[5],
            memo=temp_m,
            )

    @classmethod
    def menu_for_transactions(self):
        pass


class Account:

    table_name = "Accounts"

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance


    @staticmethod
    def instantiate(attributes):
        """Given the attribute fields as input, this method instantiates a
        single object and returns it. The database query that produces the
        input is performed elsewhere. The order of the attributes in the
        inputs (represented by the index subscript) must match up with the
        order of the attributes in the code below."""

        return Account(
            name=str(attributes[0]),    # str() is added for Python 2.X users
            balance=attributes[1],
            )


    @classmethod
    def menu_for_accounts(self):
        pass

