from ._base_obj import base

class BankOrCashAccount(base):
    obj_type_guid = "1408c33b-6284-4f50-9e31-48cbea21f3cf"
    def __init__(self, raw_dict, business_obj):
        super().__init__(obj_type_guid=BankOrCashAccount.obj_type_guid, raw_dict=raw_dict, business_obj=business_obj)

