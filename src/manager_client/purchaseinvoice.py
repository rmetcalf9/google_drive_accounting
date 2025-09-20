from ._base_obj import base
import datetime
import pytz
import Constants

class PurchaseInvoice(base):
    obj_type_guid = "58b9eb90-f6b8-4abc-8ea1-12fd77b8336e"
    def __init__(self, raw_dict, business_obj):
        super().__init__(obj_type_guid=PurchaseInvoice.obj_type_guid, raw_dict=raw_dict, business_obj=business_obj)


    def generate_line(
        account_guid,
        qty,
        purchas_unit_price
    ):
        if account_guid is None:
            raise Exception("Invalid accout")
        Constants.enforce_decimal(qty, "qty")
        Constants.enforce_decimal(purchas_unit_price, "purchas_unit_price")
        return {
            'Account': account_guid,
            'Qty': str(qty),
            'PurchaseUnitPrice': str(purchas_unit_price)
        }

    def create(
        business_obj,
        description,
        supplier_guid,
        lines,
        issue_date=datetime.datetime.now(pytz.timezone("UTC")).strftime("%Y-%m-%d")
    ):
        if lines is None:
            raise Exception("Must supply lines")
        create_json = {
            "IssueDate": issue_date,
            "DueDate": "Net",
            "DueDateDays": None,
            "DueDateDate": None,
            "Reference": None,
            "OrderNumber": None,
            "Supplier": supplier_guid,
            "PurchaseQuote": None,
            "PurchaseOrder": None,
            "ExchangeRate": 0.0,
            "ExchangeRateIsInverse": False,
            "Description": description,
            "Lines": lines,
            "PurchaseInventoryLocation": None,
            "HasLineNumber": False,
            "HasLineDescription": False,
            "Discount": False,
            "DiscountType": "Percentage",
            "AmountsIncludeTax": False,
            "WithholdingTax": False,
            "WithholdingTaxType": "Rate",
            "WithholdingTaxPercentage": 0.0,
            "WithholdingTaxAmount": 0.0,
            "HasPurchaseInvoiceCustomTheme": False,
            "PurchaseInvoiceCustomTheme": None,
            "HideBalanceDue": False,
            "ShowTaxAmountColumn": False,
            "HasPurchaseInvoiceFooters": False,
            "PurchaseInvoiceFooters": None,
            "ClosedInvoice": False,
            "AutomaticReference": False,
            "CustomFields": None,
            "CustomFields2": None
        }
        return PurchaseInvoice._create(business_obj=business_obj, obj_type_guid=PurchaseInvoice.obj_type_guid, create_json=create_json)
