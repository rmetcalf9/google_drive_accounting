import inquirer

import Constants
from manager_client import Business
from .uiHelper import UiHelper
from decimal import Decimal

# http://localhost:55667/purchase-invoice-view?
# ogYNVGVzdCBCdXNpbmVzc6oGSS9wdXJjaGFzZS1pbnZvaWNlcz9vZ1lOVkdWemRDQkNkWE5wYm1WemNfQUxBTUFNQUpBTkFMZ05BT2dOQUxnT0FOQVBBUEFRQUHCDBIJKyYfcPjZB0QRhUN2l_BttqDIDADQDAHYDAA

class ManagerFunctions():
    business = None
    ui_helper = None

    def __init__(self):
        self.business = Business("http://localhost:55667", "apiuser", "password", "Test Business")
        self.ui_helper = UiHelper()

    def menu_main(self):
        options = []
        options.append(("Testing functions", self.menu_testing))
        options.append(("Enter Quick Purchase & Payment", self.cmd_enter_quick_purchase_and_payment))
        options.append(("Back", None))
        questions = [
            inquirer.List('action',
                          message="What do you want to do?",
                          choices=options,
                          ),
        ]

        while True:
            answers = inquirer.prompt(questions)
            if answers["action"] is None:
                return
            answers["action"]()

    def menu_testing(self):
        options = []
        options.append(("Reset Cache", self.cmd_reset_cache))
        options.append(("List all suppliers", self.cmd_list_suppliers))
        options.append(("List Bank or Cash accounts", self.cmd_list_bank_or_cash_accounts))
        options.append(("List sub accounts", self.cmd_list_sub_accounts))
        options.append(("List balance sheet accounts", self.cmd_list_balance_sheet_accounts))
        options.append(("List profit and loss statement accounts", self.cmd_list_profit_and_loss_statement_accounts))
        options.append(("List quick purchase invoice accounts", self.cmd_list_quick_purchase_invoice_accounts))
        options.append(("Show First PO", self.cmd_show_first_po))
        options.append(("Create PO", self.cmd_create_test_purchase_invoice))
        options.append(("Show First Payment", self.cmd_show_first_payment))
        options.append(("Create Payment", self.cmd_create_test_supplier_payment))
        options.append(("Output Useful URLs", self.cmd_output_useful_urls))

        options.append(("Back", None))
        questions = [
            inquirer.List('action',
                          message="What do you want to do?",
                          choices=options,
                          ),
        ]

        while True:
            answers = inquirer.prompt(questions)
            if answers["action"] is None:
                return
            answers["action"]()

    def cmd_output_useful_urls(self):
        for obj_type_key in self.business.simple_obj_types.keys():
            obj_type=self.business.simple_obj_types[obj_type_key]
            print(f"{obj_type.__name__}: {self.business._get_business_url() + obj_type.obj_type_guid}")

    def cmd_list_suppliers(self):
        suppliers = self.business.suppliers()
        for supplier in suppliers:
            print(supplier.Name())

    def cmd_list_bank_or_cash_accounts(self):
        bankorcashaccounts = self.business.bankorcashaccouts()
        for bankorcashaccount in bankorcashaccounts:
            print(bankorcashaccount.Name())

    def cmd_reset_cache(self):
        print(self.business.caching_obj_loader.reset_cache())

    def cmd_list_sub_accounts(self):
        subaccounts = self.business.subaccounts()
        for subaccount in subaccounts:
            print(subaccount.Name())

    def cmd_list_balance_sheet_accounts(self):
        balancesheetaccounts = self.business.balancesheetaccounts()
        for balancesheetaccount in balancesheetaccounts:
            print(balancesheetaccount.Name())

    def cmd_list_profit_and_loss_statement_accounts(self):
        profitandlossstatementaccounts = self.business.profitandlossstatementaccounts()
        for profitandlossstatementaccount in profitandlossstatementaccounts:
            print(profitandlossstatementaccount.Name())

    def cmd_list_quick_purchase_invoice_accounts(self):
        for account in self.business.get_quick_purchase_invoice_accounts():
            print(account.Name())

    def cmd_show_first_po(self):
        first_po = self.business.purchaseinvoices()[0]
        print(first_po.full_data())

    def cmd_show_first_payment(self):
        first_payment = self.business.payments()[0]
        print(first_payment.full_data())


    def cmd_create_test_purchase_invoice(self):
        #for purchaseinvoice in self.business.purchaseinvoices():
        #    print("DD", purchaseinvoice.full_data())

        supplier = self.ui_helper.prompt_for_obj(
                prompt="Select supplier",
                obj_lis=self.business.suppliers()
        )

        qty = self.ui_helper.get_decimal_value(
            prompt="Enter Quantity",
            default="1.0"
        )
        purchase_unit_price = self.ui_helper.get_decimal_value(
            prompt="Enter Unit Price",
            default=""
        )

        account = self.ui_helper.prompt_for_obj(
                prompt="Select account for expenditure category",
                obj_lis=self.business.get_quick_purchase_invoice_accounts()
        )

        lines = []
        lines.append(self.business.simple_obj_types["PurchaseInvoice"].generate_line(
            account_guid=account.Key(),
            qty=qty,
            purchas_unit_price=purchase_unit_price
        ))
        response = self.business.simple_obj_types["PurchaseInvoice"].create(
            business_obj=self.business,
            description="Manager Debug Test Invoice",
            supplier_guid=supplier.Key(),
            lines=lines
        )
        print("Response:", response.full_data())

    def cmd_create_test_supplier_payment(self):
        supplier = self.ui_helper.prompt_for_obj(
                prompt="Select supplier",
                obj_lis=self.business.suppliers()
        )
        paid_from_account_guid = self.ui_helper.prompt_for_obj(
                prompt="Select account this was paid from",
                obj_lis=self.business.bankorcashaccouts()
        )

        amount = self.ui_helper.get_decimal_value(
            prompt="Enter Amount",
            default=""
        )
        account = self.ui_helper.prompt_for_obj(
                prompt="Select account for expenditure category",
                obj_lis=self.business.get_quick_purchase_invoice_accounts()
        )

        lines = []
        lines.append(self.business.simple_obj_types["Payment"].generate_line(
            account_guid=account,
            amount=amount
        ))
        response = self.business.simple_obj_types["Payment"].create(
            business_obj=self.business,
            reference="Manager Debug Test supplier payment",
            description="Description of test payment",
            paid_from_account_guid=paid_from_account_guid.Key(),
            supplier_guid=supplier.Key()
        )
        print("Response:", response.full_data())

    def cmd_enter_quick_purchase_and_payment(self):
        supplier = self.ui_helper.prompt_for_obj(
                prompt="Select supplier",
                obj_lis=self.business.suppliers()
        )
        account = self.ui_helper.prompt_for_obj(
                prompt="Select account for expenditure category",
                obj_lis=self.business.get_quick_purchase_invoice_accounts()
        )
        description = self.ui_helper.get_text_value(
            prompt="Enter Description"
        )
        qty = self.ui_helper.get_decimal_value(
            prompt="Enter Quantity",
            default="1.0"
        )
        purchase_unit_price = self.ui_helper.get_decimal_value(
            prompt="Enter Unit Price",
            default=""
        )
        paid_from_account_guid = self.ui_helper.prompt_for_obj(
                prompt="Select account this was paid from",
                obj_lis=self.business.bankorcashaccouts()
        )

        print("Creating invoice")
        invoice_lines = []
        invoice_lines.append(self.business.simple_obj_types["PurchaseInvoice"].generate_line(
            account_guid=account.Key(),
            qty=qty,
            purchas_unit_price=purchase_unit_price
        ))
        invoice = self.business.simple_obj_types["PurchaseInvoice"].create(
            business_obj=self.business,
            description=description,
            supplier_guid=supplier.Key(),
            lines=invoice_lines
        )
        print("Now creating payment")
        payment_lines = []
        payment_lines.append(self.business.simple_obj_types["Payment"].generate_line(
            account_guid=Constants.BalanceSheetAccountsPayableAccountUuid,
            amount=purchase_unit_price * qty,
            accounts_payable_supplier=supplier.Key(),
            purchase_invoice=invoice.Key(),
        ))
        response2 = self.business.simple_obj_types["Payment"].create(
            business_obj=self.business,
            reference=None,
            lines=payment_lines,
            description=description,
            paid_from_account_guid=paid_from_account_guid.Key(),
            supplier_guid=supplier.Key()
        )

#CustomFieldsAttribute = Union["model.AmortizationEntry", "model.BillableTime", "model.BusinessDetails", "model.CapitalAccount",
# "model.CreditNote", "model.Customer", "model.DebitNote", "model.DeliveryNote", "model.DepreciationEntry", "model.Employee",
# "model.ExpenseClaim", "model.FixedAsset", "model.Folder", "model.GoodsReceipt", "model.IntangibleAsset", "model.InterAccountTransfer",
# "model.InventoryItem", "model.InventoryKit", "model.InventoryTransfer", "model.InventoryWriteOff", "model.Investment",
# "model.JournalEntry", "model.NonInventoryItem", "model.Payment", "model.Payslip", "model.PayslipContributionItem",
# "model.PayslipDeductionItem"
#
# RecurringSalesInvoice", "model.RecurringSalesOrder", "model.RecurringSalesQuote",
# "model.SalesInvoice", "model.SalesOrder", "model.SalesQuote", "model.SpecialAccount",  "model.TaxCode",
# "model.WithholdingTaxReceipt"]


#{'_url': 'http://localhost:55667', '_name': 'Test Business', '_api_url': 'http://localhost:55667/api/VGVzdCBCdXNpbmVzcw/',
# '_auth': ('apiuser', 'password'), 'headers': {'User-Agent': 'python-requests/2.31.0',
# 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'},
# 'auth': None, 'proxies': {}, 'hooks': {'response': []}, 'params': {}, 'stream': False, 'verify': True, 'cert': None, 'max_redirects': 30, 'trust_env': True,
# 'cookies': <RequestsCookieJar[]>, 'adapters': OrderedDict([('https://', <requests.adapters.HTTPAdapter object at 0x7f7d8388b370>),
# ('http://', <requests.adapters.HTTPAdapter object at 0x7f7d8388b3d0>)]),
# 'TaxCode': <class 'abc.TaxCode'>,
# 'ProfitAndLossStatementGroup': <class 'abc.ProfitAndLossStatementGroup'>,

# 'ProfitAndLossStatementAccount': <class 'abc.ProfitAndLossStatementAccount'>,
# 'BalanceSheetAccount': <class 'abc.BalanceSheetAccount'>,
# 'SubAccount': <class 'abc.SubAccount'>,
# 'Supplier': <class 'abc.Supplier'>,
# 'BankOrCashAccount': <class 'abc.BankOrCashAccount'>}

