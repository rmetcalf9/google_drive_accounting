from urllib.parse import urljoin
from base64 import urlsafe_b64encode
import requests
import json
from .supplier import Supplier
from .bankOrCashAccount import BankOrCashAccount
from .subaccounts import SubAccount
from .profitandlossstatementaccounts import ProfitAndLossStatementAccount
from .balancesheetaccounts import BalanceSheetAccount
from .cachingObjLoader import CachingObjLoader
from .purchaseinvoice import PurchaseInvoice
from .payment import Payment

def _b64encode(string):
    if hasattr(string, "encode"):
        string = string.encode()
    return urlsafe_b64encode(string).decode().rstrip("=")

class Business():
    url=None
    username=None
    password=None
    name=None
    caching_obj_loader=None
    simple_obj_types = {
        "Supplier": Supplier,
        "BankOrCashAccount": BankOrCashAccount,
        "SubAccount": SubAccount,
        "ProfitAndLossStatementAccount": ProfitAndLossStatementAccount,
        "BalanceSheetAccount": BalanceSheetAccount,
        "PurchaseInvoice": PurchaseInvoice,
        "Payment": Payment
    }

    def __init__(self, url, username, password, name):
        self.url=url
        self.username=username
        self.password=password
        self.name=name
        self.caching_obj_loader = CachingObjLoader(business_obj=self)

    def _get_business_url(self):
        return urljoin(self.url, f"api/{_b64encode(self.name)}/")

    def _call_api(self, method, url, data=None, expected_responses=[200]):
        headers = {
            "Accept": "application/json"
        }
        url_to_call=urljoin(self._get_business_url(), url)
        result = method(url_to_call, allow_redirects=True, headers=headers, auth=(self.username, self.password), data=data)
        if result.status_code not in expected_responses:
            print("ERROR")
            print("Call to:", url_to_call)
            print(" Response code:", result.status_code)
            print(" Response text:", result.text)
            raise Exception("Request failed")
        return json.loads(result.text)

    def _call_api_get(self, url, expected_responses=[200]):
        return self._call_api(requests.get, url=url, expected_responses=expected_responses)

    def _call_api_post(self, url, post_dict, expected_responses=[200]):
        return self._call_api(method=requests.post, url=url, expected_responses=expected_responses, data=json.dumps(post_dict))

    def _find_object_class(self, obj_type_guid):
        for object_type_key in self.simple_obj_types.keys():
            if self.simple_obj_types[object_type_key].obj_type_guid==obj_type_guid:
                return self.simple_obj_types[object_type_key]
        return None

    def get_simple_obj(self, obj_type_guid, key):
        obj_class = self._find_object_class(obj_type_guid=obj_type_guid)
        return obj_class(raw_dict={"Key": key}, business_obj=self)

    def suppliers(self):
        ret_val = []
        for supplier in self._call_api_get(Supplier.obj_type_guid + ".json"):
            ret_val.append(Supplier(supplier, business_obj=self))
        return ret_val

    def bankorcashaccouts(self):
        ret_val = []
        for supplier in self._call_api_get(BankOrCashAccount.obj_type_guid + ".json"):
            ret_val.append(BankOrCashAccount(supplier, business_obj=self))
        return ret_val

    def subaccounts(self):
        ret_val = []
        for ite in self._call_api_get(SubAccount.obj_type_guid + ".json"):
            ret_val.append(SubAccount(ite, business_obj=self))
        return ret_val

    def profitandlossstatementaccounts(self):
        ret_val = []
        for ite in self._call_api_get(ProfitAndLossStatementAccount.obj_type_guid + ".json"):
            ret_val.append(ProfitAndLossStatementAccount(ite, business_obj=self))
        return ret_val

    def balancesheetaccounts(self):
        ret_val = []
        for ite in self._call_api_get(BalanceSheetAccount.obj_type_guid + ".json"):
            ret_val.append(BalanceSheetAccount(ite, business_obj=self))
        return ret_val

    def purchaseinvoices(self):
        ret_val = []
        for ite in self._call_api_get(PurchaseInvoice.obj_type_guid + ".json"):
            ret_val.append(PurchaseInvoice(ite, business_obj=self))
        return ret_val

    def payments(self):
        ret_val = []
        for ite in self._call_api_get(Payment.obj_type_guid + ".json"):
            ret_val.append(Payment(ite, business_obj=self))
        return ret_val

    def get_quick_purchase_invoice_accounts(self):
        ret_val = []
        for account in self.profitandlossstatementaccounts():
            if account.Code() is not None:
                if account.Code().startswith("RJM"):
                    ret_val.append(account)
        return ret_val


