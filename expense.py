

class Expense:
    """ Class for modeling expenses."""

    def __init__(self, db_data_list):
        self.db_id = db_data_list[0]
        self.amount = db_data_list[1]
        self.description = db_data_list[2]
        self.category = db_data_list[3]
        self.date = db_data_list[4]

    def list_widget_format(self):
        amount = self.format_list_wiget(self.amount, 12)
        description = self.format_list_wiget(self.description, 22)
        category = self.format_list_wiget(self.category, 20)
        date = self.format_list_wiget(self.date, 12)

        return f"{amount}{description}{category}{date}"

    def format_list_wiget(self, data, max_length):
        return f"{data}{''*(max_length-len(data))}"
