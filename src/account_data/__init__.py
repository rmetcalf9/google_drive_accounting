from decimal import Decimal


class AccountData():
    items = None

    def __init__(self):
        self.items = []

    def add_reciept_line(
        self,
        day_name,
        company,
        method,
        category,
        amount,
        details
    ):
        if amount=="":
            raise Exception("Invalid amount")
        amount = Decimal(amount)
        if (amount<0):
            raise Exception("Negative amount")
        self.items.append({
            "day_name": day_name,
            "company": company,
            "method": method,
            "category": category,
            "amount": amount,
            "details": details,
        })