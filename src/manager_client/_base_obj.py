from urllib.parse import urljoin

# When the object is created the raw_dict contains the fields that appeared when the object was retrieved as part of
#  as list.
# The full_dict is populated on demand when detail fields are requested

class base():
    raw_dict = None
    full_dict = None
    business_obj = None
    obj_type_guid = None
    def __init__(self, obj_type_guid, raw_dict, business_obj):
        self.raw_dict = raw_dict
        self.single_query_dict = None
        self.business_obj = business_obj
        self.obj_type_guid = obj_type_guid

    def Key(self):
        return self.raw_dict["Key"]

    def Name(self):
        return self.raw_dict["Name"]

    def Timestamp(self):
        return self.raw_dict["Timestamp"]

    def _load_full_dict(self, force=False):
        if not force:
            if self.full_dict is not None:
                return
        self.full_dict = self.business_obj.caching_obj_loader.get(
            obj_type_guid=self.obj_type_guid,
            key=self.Key(),
            force=force
        )

    def _create(business_obj, obj_type_guid, create_json):
        result = business_obj._call_api_post(
            url=obj_type_guid + ".json",
            post_dict=create_json
        )
        if result["Success"] != True:
            raise Exception("Create failed")
        return business_obj.get_simple_obj(obj_type_guid=obj_type_guid, key=result["Key"])

    def full_data(self):
        self._load_full_dict()
        return {
            "raw_dict": self.raw_dict,
            "full_dict": self.full_dict
        }