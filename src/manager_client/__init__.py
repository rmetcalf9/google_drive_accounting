from urllib.parse import urljoin
from base64 import urlsafe_b64encode
import requests
import json
from .supplier import Supplier
from .bankOrCashAccount import BankOrCashAccount
from .subaccounts import SubAccount
from .profitandlossstatementaccounts import ProfitAndLossStatementAccount
from .balancesheetaccounts import BalanceSheetAccount

def _b64encode(string):
    if hasattr(string, "encode"):
        string = string.encode()
    return urlsafe_b64encode(string).decode().rstrip("=")

class Business():
    url=None
    username=None
    password=None
    name=None

    def __init__(self, url, username, password, name):
        self.url=url
        self.username=username
        self.password=password
        self.name=name

    def _get_business_url(self):
        return urljoin(self.url, f"api/{_b64encode(self.name)}/")

    def _call_api(self, method, url, expected_responses=[200]):
        headers = {
            "Accept": "application/json"
        }
        url_to_call=urljoin(self._get_business_url(), url)
        result = method(url_to_call, allow_redirects=True, headers=headers, auth=(self.username, self.password))
        if result.status_code not in expected_responses:
            raise Exception("Request failed")
        return json.loads(result.text)

    def _call_api_get(self, url, expected_responses=[200]):
        return self._call_api(requests.get, url, expected_responses)


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

