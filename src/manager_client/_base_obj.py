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

    def _get_obj_url(self):
        return urljoin(self.obj_type_guid, self.Key() + ".json")

    def _load_full_dict(self, force=False):
        if not force:
            if self.full_dict is not None:
                return
        self.full_dict = self.business_obj._call_api_get(url=self._get_obj_url())
