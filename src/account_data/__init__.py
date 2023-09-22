from decimal import Decimal
from .item import Item, create_from_string

class AccountData():
    items = None

    def __init__(self):
        self.items = []

    def save_to_file(self, filename):
        with open(filename, 'w') as outfile:
            for item in self.items:
                outfile.write(item.to_serealizable_string())
                outfile.write("\n")

    def load_from_file(self, filename):
        with open(filename, 'r') as infile:
            for line in infile:
                line2 = line.strip()
                self.items.append(create_from_string(line2))

    def print_all(self):
        for item in self.items:
            print(item.to_serealizable_string())

    def add_reciept_line(
        self,
        day_name,
        company,
        method,
        category,
        amount,
        details
    ):
        item = Item(
            day_name,
            company,
            method,
            category,
            amount,
            details
        )
        self.items.append(item)
