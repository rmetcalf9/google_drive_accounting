from ._base_obj import base

class Supplier(base):
    obj_type_guid = "6d2dc48d-2053-4e45-8330-285ebd431242"
    def __init__(self, raw_dict, business_obj):
        super().__init__(obj_type_guid=Supplier.obj_type_guid, raw_dict=raw_dict, business_obj=business_obj)
