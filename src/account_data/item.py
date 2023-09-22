from decimal import Decimal

str_seperator=",:#\"\";'''"

def create_from_string(str):
    sp = str.split(str_seperator)
    return Item(
        day_name=sp[0],
        company=sp[1],
        method=sp[2],
        category=sp[3],
        amount=sp[4],
        details=sp[5]
    )

class Item():
    day_name=None
    company=None
    method=None
    category=None
    amount=None
    details=None

    def __init__(
        self,
        day_name,
        company,
        method,
        category,
        amount,
        details
    ):
        if len(day_name) != 10:
            raise Exception("Invalid day")
        if day_name[4] != " ":
            raise Exception("Invalid day")
        if day_name[7] != " ":
            raise Exception("Invalid day")
        if amount=="":
            raise Exception("Invalid amount")
        amount = Decimal(amount)
        if amount<0:
            raise Exception("Negative amount")

        self.day_name=day_name
        self.company=company
        self.method=method
        self.category=category
        self.amount=amount
        self.details=details

    def to_serealizable_string(self):
        return f"{self.day_name}{str_seperator}{self.company}{str_seperator}{self.method}{str_seperator}{self.category}{str_seperator}{str(self.amount)}{str_seperator}{self.details}"