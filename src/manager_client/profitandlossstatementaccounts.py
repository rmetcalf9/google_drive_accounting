from ._base_obj import base

class ProfitAndLossStatementAccount(base):
    obj_type_guid = "26b9e4a5-ce10-4f30-94c7-23a1ca4428f9"
    def __init__(self, raw_dict, business_obj):
        super().__init__(obj_type_guid=ProfitAndLossStatementAccount.obj_type_guid, raw_dict=raw_dict, business_obj=business_obj)

    def Code(self):
        self._load_full_dict()
        if "Code" not in self.full_dict:
            return ""
        return self.full_dict["Code"]
