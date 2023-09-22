

class SheetsApiHelpers():
    sheets_service = None
    def __init__(self, sheets_service):
        self.sheets_service = sheets_service

    def get_sheet_metadata(self, sheet_id):
        return self.sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
