from ._base_obj import base

class BalanceSheetAccount(base):
    obj_type_guid = "6ef13e42-ad89-4d42-9480-546e0c04a411"
    def __init__(self, raw_dict, business_obj):
        super().__init__(obj_type_guid=BalanceSheetAccount.obj_type_guid, raw_dict=raw_dict, business_obj=business_obj)
