from ._base_obj import base
import datetime
import pytz
import Constants

class Payment(base):
    obj_type_guid = "79f99d26-e43a-4ecb-a9c9-0774601a9b2e"
    def __init__(self, raw_dict, business_obj):
        super().__init__(obj_type_guid=Payment.obj_type_guid, raw_dict=raw_dict, business_obj=business_obj)

    def generate_line(
        account_guid,
        amount,
        accounts_payable_supplier=None,
        purchase_invoice=None
    ):
        if account_guid is None:
            raise Exception("Invalid accout")
        Constants.enforce_decimal(amount, "amount")
        return {
            'Account': account_guid,
            'AccountsPayableSupplier': accounts_payable_supplier,
            'PurchaseInvoice': purchase_invoice,
            'Amount': str(amount)
        }

    def create(
        business_obj,
        reference,
        description,
        paid_from_account_guid,
        lines,
        supplier_guid=None,
        date=datetime.datetime.now(pytz.timezone("UTC")).strftime("%Y-%m-%d")
    ):
        payee = "Other"
        if supplier_guid is not None:
            payee = "Supplier"
        # TODO Add code for customer payee
        create_json = {
            "Date": date,
            "Reference": reference,
            "PaidFrom": paid_from_account_guid,
            "Cleared": "OnTheSameDate",
            "BankClearDate": None,
            "ExchangeRate": 0.0,
            "ExchangeRateIsInverse": False,
            "Payee": payee,
            "Customer": None,
            "Supplier": supplier_guid,
            "Contact": None,
            "Description": description,
            "Lines": lines,
            "InventoryLocation": None,
            "HasLineNumber": False,
            "HasLineDescription": False,
            "QuantityColumn": False,
            "UnitPriceColumn": False,
            "Discount": False,
            "DiscountType": "Percentage",
            "AmountsAreTaxExclusive": False,
            "FixedTotal": False,
            "FixedTotalAmount": 0.0,
            "BalancingAmount": None,
            "CustomTheme": False,
            "PaymentCustomTheme": None,
            "AutomaticReference": False,
            "HasPaymentCustomTitle": False,
            "PaymentCustomTitle": None,
            "ShowTaxAmountColumn": False,
            "HasPaymentFooters": False,
            "PaymentFooters": None,
            "CustomFields": None,
            "CustomFields2": None
        }
        return Payment._create(business_obj=business_obj, obj_type_guid=Payment.obj_type_guid, create_json=create_json)
