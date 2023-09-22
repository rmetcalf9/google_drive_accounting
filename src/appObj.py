import json
import inquirer

import account_data_loader
from google_client import GoogleClient, DriveApiHelpers, SheetsApiHelpers
from googleapiclient.discovery import build

class appObj():
    settings = None
    account_data = None

    def __init__(self, settings_file_name):
        self.settings = None
        with open(settings_file_name, "r") as fileHandle:
            self.settings = json.load(fileHandle)
        self.account_data = None
        pass


    def cmd_print_all(self):
        if self.account_data is None:
            print("ERROR No data loaded")
            return
        self.account_data.print_all()

    def cmd_load_all_data_from_last_saved(self):
        print("Load latest saved data...")
        self.account_data = account_data_loader.load_from_latest_saved(
            local_save_folder=self.settings["local_saved_data_location"]
        )

    def cmd_load_new_data_from_google(self):
        print("Load new data from google...")
        google_client = GoogleClient( self.settings["google_credentials_file"], self.settings["temporary_token_file"])
        creds = google_client.get_creds()
        drive_api_helpers = DriveApiHelpers(drive_service=build('drive', 'v3', credentials=creds))
        sheets_api_helpers = SheetsApiHelpers(sheets_service=build('sheets', 'v4', credentials=creds))

        print("Searching for id of accounting folder...")
        accounting_folder_id = drive_api_helpers.get_folder_id(path=self.settings["accounting_root"])
        self.settings["accounting_folder_id"] = accounting_folder_id

        print(f"Folder used {self.settings['accounting_root']} - id={self.settings['accounting_folder_id']}")

        global_account_data = account_data_loader.load_account_data_from_google(
            drive_api_helpers=drive_api_helpers,
            sheets_api_helpers=sheets_api_helpers,
            accouting_folder_id=self.settings["accounting_folder_id"],
            local_save_folder=self.settings["local_saved_data_location"]
        )