

class Expense:
    """ Class for modeling expenses."""

    def __init__(self, db_data_list):
        self.db_id = db_data_list[0]
        self.amount = db_data_list[1]
        self.description = db_data_list[2]
        self.category = db_data_list[3]
        self.date = db_data_list[4]
