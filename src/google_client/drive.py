

class DriveApiHelpers():
    drive_service = None
    def __init__(self, drive_service):
        self.drive_service = drive_service

    def get_root_folder_id(self):
        return self.drive_service.files().get(fileId='root').execute()['id']

    def get_item_id(self, parent, name):
        files = self.drive_service.files()
        request = files.list(pageSize=100, q=f"name='{name}' and '{parent}' in parents and trashed=false", fields="nextPageToken, files(id, name, parents)")
        res = []
        while request is not None:
            result = request.execute()
            for file in result["files"]:
                res.append(file)
            request = files.list_next(request, result)
        if len(res) == 0:
            raise Exception(f"Error folder with {name} not found with parent {parent}")
        if len(res) != 1:
            raise Exception("Found too many")
        return res[0]["id"]

    def get_folder_id(self, path):
        if path[0] != "/":
            raise Exception("Path must start with /")
        if path=="/":
            return self.get_root_folder_id()
        path_components = path[1:].split("/")
        if len(path_components) == 1:
            print(path[1:])
            return self.get_item_id(parent=self.get_root_folder_id(), name=path[1:])
        else:
            cur_root = self.get_root_folder_id()
            for path in path_components:
                cur_root = self.get_item_id(parent=cur_root, name=path)
            return cur_root

    def get_all_items_in_folder(self, folder_id, restrict_mimetype=None):
        files = self.drive_service.files()
        query_string = f"'{folder_id}' in parents and trashed=false"
        if restrict_mimetype is not None:
            for mt in restrict_mimetype:
                query_string += f" and mimeType='{mt}'"

        return (files, files.list(pageSize=100, q=query_string, fields="nextPageToken, files(id, name, parents, mimeType)"))
        #Exmpale usage:
        # (files, request) = drive_api_helpers.get_all_items_in_folder(folder_id="1uTSyL7-DZ3PwHYAxv2OQsQvq81lXGX4F")
        # while request is not None:
        #     result = request.execute()
        #     for file in result["files"]:
        #         print("FFF", file)
        #     request = files.list_next(request, result)


