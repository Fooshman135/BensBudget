import Globals
import sqlite3
import os
import LL_Services


# ____________________________________________________________________________#
def create_database_with_tables(name):
    """Create a new .db file within USER_BUDGETS directory and name it
    as the input. Also create tables.
    Returns a sqlite3.connection object."""

    # The 'detect_types' line allows the DATE type to survive the
    # round-trip from Python to sqlite3 database to Python again.
    connection = sqlite3.connect(
        os.path.join(Globals.USER_BUDGETS, name + '.db'),
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
    connection.close()


# ____________________________________________________________________________#
def establish_db_connection(path_to_db):
    # The 'detect_types' line allows the DATE type to
    # survive the round-trip from Python to sqlite3 database
    # to Python again.
    Globals.conn = sqlite3.connect(
        path_to_db,
        detect_types=sqlite3.PARSE_DECLTYPES,
    )
    Globals.SELECTED_BUDGET_NAME = LL_Services.full_filepath_to_just_name(path_to_db)






