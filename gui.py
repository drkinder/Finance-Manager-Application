import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QMainWindow,
                             QTextEdit, QGridLayout, QApplication, QPushButton)
from db_handler import DbHandler


class AddExpensePopup(QWidget):

    def __init__(self):
        QWidget.__init__(self)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.db = DbHandler()
        self.initUI()

    def initUI(self):

        balance = QLabel(f'Balance: {self.db.get_balance()}')
        add_expense_btn = QPushButton('Add Expense', self)
        add_expense_btn.clicked.connect(self.add_expense_window)

        # titleEdit = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(1)

        grid.addWidget(balance, 0, 0)
        # grid.addWidget(titleEdit, 1, 1)
        grid.addWidget(add_expense_btn, 1, 0)

        self.setLayout(grid)

        self.setGeometry(300, 300, 800, 500)
        self.setWindowTitle('Review')
        self.show()

    def add_expense_window(self):
        self.add_expense_popup = AddExpensePopup()
        self.add_expense_popup.setGeometry(300, 300, 400, 400)
        self.add_expense_popup.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
