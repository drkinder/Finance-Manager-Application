import sys
import datetime
from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox, QMainWindow, QLineEdit, QTableWidget,
                             QTableWidgetItem, QGridLayout, QApplication, QPushButton)
from db_handler import DbHandler


class AddExpensePopup(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.db = DbHandler()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        grid.setSpacing(1)

        amount_title = QLabel('Amount  ')
        grid.addWidget(amount_title, 0, 0)
        self.amount = QLineEdit(self)
        grid.addWidget(self.amount, 0, 1)

        description_title = QLabel('Description  ')
        grid.addWidget(description_title, 1, 0)
        self.description = QLineEdit(self)
        grid.addWidget(self.description, 1, 1)

        date_title = QLabel('Date (yyyy-mm-dd)  ')
        grid.addWidget(date_title, 2, 0)
        self.date = QLineEdit(self)
        self.date.setPlaceholderText(str(datetime.date.today()))
        grid.addWidget(self.date, 2, 1)

        category_title = QLabel('Category  ')
        grid.addWidget(category_title, 3, 0)
        self.category = QComboBox(self)
        self.category.addItem("food and drink")
        self.category.addItem("entertainment")
        self.category.addItem("self edification")
        self.category.addItem("video game")
        self.category.addItem("travel")
        self.category.addItem("bills")
        self.category.addItem("other")
        grid.addWidget(self.category, 3, 1)

        self.submit_button = QPushButton('Add Expense', self)
        self.submit_button.clicked.connect(self.add_expense)
        grid.addWidget(self.submit_button, 4, 2)

        self.setLayout(grid)
        self.setGeometry(300, 300, 500, 200)
        self.setWindowTitle('Add Expense')
        self.amount.setFocus()
        self.show()

    def add_expense(self):
        amount = self.amount.text()
        description = self.description.text()
        date = self.get_date()
        category = str(self.category.currentText())

        if self.are_valid_entries(amount, date):
            self.db.add_expense(amount, description, category, date)
            self.reset_add_expense_widgets()
        else:
            # ADD POPUP WARNING
            print("INVALID ENTRIES")

    def get_date(self):
        if self.date.text() == "":
            return str(datetime.date.today())
        return self.date.text()

    def print_expense_data(self, amount, description, category, date):
        print(f"amount: {amount}")
        print(f"description: {description}")
        print(f"date: {date}")
        print(f"category: {category}")

    def are_valid_entries(self, amount, date):
        try:
            float(amount)
        except ValueError:
            print("INVALID AMOUNT")
            return False

        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("INVALID DATE")
            return False

        return True

    def reset_add_expense_widgets(self):
        """ Resets all widgets in AddExpensePopup window so another expense can be added."""
        self.amount.setText("")
        self.description.setText("")
        self.date.setText(str(datetime.date.today()))


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.db = DbHandler()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        grid.setSpacing(1)

        self.balance = QLabel(f'Balance: {self.db.get_balance()}')
        grid.addWidget(self.balance, 0, 0)

        self.expense_table = QTableWidget(self)
        self.load_db_data()
        grid.addWidget(self.expense_table, 1, 0)

        refresh_expenses_btn = QPushButton('Refresh Expenses', self)
        refresh_expenses_btn.clicked.connect(self.load_db_data)
        grid.addWidget(refresh_expenses_btn, 2, 0)

        add_expense_btn = QPushButton('Add Expense', self)
        add_expense_btn.clicked.connect(self.add_expense_window)
        grid.addWidget(add_expense_btn, 3, 0)

        self.setLayout(grid)

        self.setGeometry(300, 300, 600, 500)
        self.setWindowTitle('Review')
        self.show()

    def load_db_data(self):

        self.balance.setText(f'Balance: {self.db.get_balance()}')

        self.expense_table.setRowCount(0)
        self.expense_table.setRowCount(5)

        self.expense_table.setColumnCount(0)
        self.expense_table.setColumnCount(5)

        self.expense_table.setHorizontalHeaderLabels(['Amount', 'Description', 'Category', 'Date', 'Balance'])

        expenses = self.db.get_all_expenses()

        for row_idx, row_data in enumerate(expenses):
            self.expense_table.insertRow(row_idx)
            for column_idx, data in enumerate(row_data):
                if column_idx > 0:
                    self.expense_table.setItem(row_idx, column_idx-1, QTableWidgetItem(str(data)))

    def add_expense_window(self):
        self.add_expense_popup = AddExpensePopup()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
