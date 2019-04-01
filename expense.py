

class Expense:

    def __init__(self):
        self.db_id = 0
        self.amount = 0
        self.description = ""
        self.category = ""
        self.date = ""

    def fill_data(self, db_id, amount, description, category, date):
        self.db_id = db_id
        self.amount = amount
        self.description = description
        self.category = category
        self.date = date
