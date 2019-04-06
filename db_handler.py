import sqlite3
import datetime

from expense import Expense

class DbHandler:

    def __init__(self):
        self.db_filename = "db.db"
        self.conn = sqlite3.connect(self.db_filename)

    def add_expense(self, amount, description, category="other", date=datetime.date.today()):
        initial_balance = self.get_balance()

        try:
            new_balance = round(initial_balance + float(amount), 2)
        except ValueError:
            new_balance = initial_balance

        # sql_line = f"INSERT INTO expenses ('amount', 'description', 'category', 'date', 'balance') VALUES \
        #             ({amount}, {description}, {category}, {date}, {new_balance})"
        sql_line = """INSERT INTO expenses(amount, description, category, date, balance) VALUES
                      (?, ?, ?, ?, ?)"""
        self.conn.execute(sql_line, (amount, description, category, date, new_balance))
        self.commit_conn()

    def get_recent_expenses1(self, lookback=5):
        """ Returns a list with tupled expense rows as far back as defined in lookback"""
        # cursor = self.conn.execute(f'SELECT id, max(date) AS "MostRecent" FROM expenses')
        cursor = self.conn.execute('SELECT * FROM expenses ORDER BY date DESC, id DESC')
        try:
            return cursor.fetchall()[:lookback]
        except IndexError:
            # If lookback > length of recorded expenses
            return cursor.fetchall()

    def get_recent_expenses(self, lookback=5):
        """ Returns a list of Expense Class instances for the past {lookback} expenses"""
        cursor = self.conn.execute('SELECT * FROM expenses ORDER BY date DESC, id DESC')
        try:
            return [Expense(e) for e in cursor.fetchall()[:lookback]]
        except IndexError:
            # If lookback > length of recorded expenses
            return cursor.fetchall()

    def get_balance(self):
        """ Returns current balance from expenses table"""
        max_id = self.get_max_id("expenses")

        cursor = self.conn.execute(f"SELECT balance FROM expenses WHERE id={max_id}")
        balance = cursor.fetchone()[0]
        return balance

    def get_max_id(self, table_name):
        """ Returns the max id primary key in provided table_name"""
        cursor = self.conn.execute(f"SELECT max(id) FROM {table_name}")
        return cursor.fetchone()[0]

    def open_conn(self):
        self.conn = sqlite3.connect(self.db_filename)

    def close_conn(self):
        self.conn.close()

    def commit_conn(self):
        self.conn.commit()


class Test:

    def __init__(self):
        self.db = DbHandler()

    def test_current_balance(self):
        print(f"YOUR BALANCE IS ${float(self.db.get_balance())}")

    def test_recent_expenses(self, lookback=5):
        recent_expenses = self.db.get_recent_expenses(lookback)
        #print(recent_expenses)
        for ex in recent_expenses:
            print(f"{ex[2]}: {ex[1]} -- {ex[3]} on {ex[4]}")

    def test_add_expense(self, amount, description, category="other", date=datetime.date.today()):
        self.db.add_expense(amount, description, category, date)

    def test_recent_expenses_creating_Expense_instances(self):
        recent_expense = self.db.get_recent_expenses()
        for ex in recent_expense:
            print(ex)


if __name__ == "__main__":
    test = Test()
    test.test_current_balance()
    #test.test_add_expense("", "", "food")
    #test.test_recent_expenses(3)
    test.test_recent_expenses_creating_Expense_instances()

