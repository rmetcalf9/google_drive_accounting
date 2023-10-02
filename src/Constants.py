
def enforce_decimal(value, field_name="Number"):
    if value.__class__.__name__ != "Decimal":
        raise Exception(field_name + " must be provided as Decimal (provided - " + value.__class__.__name__ + ")")
