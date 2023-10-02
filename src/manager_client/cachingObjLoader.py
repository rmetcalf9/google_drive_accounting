from urllib.parse import urljoin

class CachingObjLoader():
    cache = None
    business_obj = None
    def __init__(self, business_obj):
        self.business_obj = business_obj
        self.cache = {}

    def get_cache_key(self, obj_type_guid, key):
        return obj_type_guid + "/:/" + key

    def get(self, obj_type_guid, key, force=False):
        ck = self.get_cache_key(obj_type_guid, key)
        if ck in self.cache:
            if force:
                del self.cache[ck]
            else:
                return self.cache[ck]
        self.cache[ck] = self.business_obj._call_api_get(url=urljoin(obj_type_guid, key + ".json"))
        return self.cache[ck]

    def reset_cache(self):
        self.cache = {}
