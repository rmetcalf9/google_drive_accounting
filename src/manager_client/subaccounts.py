from ._base_obj import base

class SubAccount(base):
    obj_type_guid = "f361339b-932a-4436-b56e-a337c1587c72"
    def __init__(self, raw_dict, business_obj):
        super().__init__(obj_type_guid=SubAccount.obj_type_guid, raw_dict=raw_dict, business_obj=business_obj)

