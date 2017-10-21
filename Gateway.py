import Globals
import sqlite3
import os


def create_database_with_tables(name):
    """Create a new .db file within USER_BUDGETS directory and name it
    as the input. Also create tables."""

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
    return connection




def query_entire_table(table_name):
    cur = Globals.conn.cursor()
    sql = "SELECT * FROM {}".format(table_name)
    cur.execute(sql)
    query_results = cur.fetchall()
    cur.close()
    return query_results





