import inquirer

from manager_api import Business as ext_lib_Business
from manager_client import Business


class ManagerFunctions():
    ext_lib_business = None
    business = None

    def __init__(self):
        # Open the business. NOTE: Always use a test business first!
        self.ext_lib_business = ext_lib_Business("http://localhost:55667", "apiuser", "password", "Test Business")
        self.business = Business("http://localhost:55667", "apiuser", "password", "Test Business")

    def menu_main(self):
        options = []
        options.append(("Testing functions", self.menu_testing))
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
        options.append(("*List attributes of business", self.cmd_list_attributes_of_business))
        options.append(("List all suppliers", self.cmd_list_suppliers))
        options.append(("List Bank or Cash accounts", self.cmd_list_bank_or_cash_accounts))
        options.append(("List sub accounts", self.cmd_list_sub_accounts))
        options.append(("List balance sheet accounts", self.cmd_list_balance_sheet_accounts))
        options.append(("List profit and loss statement accounts", self.cmd_list_profit_and_loss_statement_accounts))
        options.append(("List quick purchase invoice accounts", self.cmd_list_quick_purchase_invoice_accounts))
        options.append(("*Create PO", self.cmd_create_test_purchase_invoice))

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

    def _list_objects(self, object_name):
        obj = getattr(self.ext_lib_business, object_name)
        suppliers = obj.list()
        for supplier in suppliers:
            print(supplier.Name)

    def cmd_list_suppliers(self):
        suppliers = self.business.suppliers()
        for supplier in suppliers:
            print(supplier.Name())

    def cmd_list_bank_or_cash_accounts(self):
        bankorcashaccounts = self.business.bankorcashaccouts()
        for bankorcashaccount in bankorcashaccounts:
            print(bankorcashaccount.Name())

    def cmd_list_attributes_of_business(self):
        print(self.ext_lib_business.__dict__)

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
        for account in self._get_quick_purchase_invoice_accounts():
            print(account.Name())

    def _get_quick_purchase_invoice_accounts(self):
        ret_val = []
        for account in self.business.profitandlossstatementaccounts():
            if account.Code() is not None:
                if account.Code().startswith("RJM"):
                    ret_val.append(account)
        return ret_val

    def cmd_create_test_purchase_invoice(self):
        print("TODO")

#CustomFieldsAttribute = Union["model.AmortizationEntry", "model.BillableTime", "model.BusinessDetails", "model.CapitalAccount",
# "model.CreditNote", "model.Customer", "model.DebitNote", "model.DeliveryNote", "model.DepreciationEntry", "model.Employee",
# "model.ExpenseClaim", "model.FixedAsset", "model.Folder", "model.GoodsReceipt", "model.IntangibleAsset", "model.InterAccountTransfer",
# "model.InventoryItem", "model.InventoryKit", "model.InventoryTransfer", "model.InventoryWriteOff", "model.Investment",
# "model.JournalEntry", "model.NonInventoryItem", "model.Payment", "model.Payslip", "model.PayslipContributionItem",
# "model.PayslipDeductionItem", "model.PayslipEarningsItem", "model.ProductionOrder", "model.Project", "model.PurchaseInvoice",
# "model.PurchaseOrder", "model.PurchaseQuote", "model.Receipt", "model.RecurringInterAccountTransfer", "model.RecurringJournalEntry",
# "model.RecurringPayment", "model.RecurringPayslip", "model.RecurringPurchaseInvoice", "model.RecurringPurchaseOrder",
# "model.RecurringReceipt", "model.RecurringSalesInvoice", "model.RecurringSalesOrder", "model.RecurringSalesQuote",
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
