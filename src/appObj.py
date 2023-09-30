import json
import inquirer

import account_data_loader
from google_client import GoogleClient, DriveApiHelpers, SheetsApiHelpers
from googleapiclient.discovery import build

def get_string_with_2_dp(dec):
    a = str(dec).split(".")
    if len(a) == 2:
        if len(a[1]) == 1:
            a[1] += "0"
        if len(a[1]) != 2:
            raise Exception("Wrong number of dp")
        return a[0] + "." + a[1]
    return a[0] + ".00"

def format_decimal_for_display(dec):
    return ((" " * 10) + get_string_with_2_dp(dec))[-10:]

class appObj():
    settings = None
    account_data = None

    def __init__(self, settings_file_name):
        self.settings = None
        with open(settings_file_name, "r") as fileHandle:
            self.settings = json.load(fileHandle)
        self.account_data = None
        self.cmd_load_all_data_from_last_saved()
        if self.account_data is None:
            self.cmd_load_new_data_from_google()


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
        self.account_data = None
        google_client = GoogleClient( self.settings["google_credentials_file"], self.settings["temporary_token_file"])
        creds = google_client.get_creds()
        drive_api_helpers = DriveApiHelpers(drive_service=build('drive', 'v3', credentials=creds))
        sheets_api_helpers = SheetsApiHelpers(sheets_service=build('sheets', 'v4', credentials=creds))

        print("Searching for id of accounting folder...")
        accounting_folder_id = drive_api_helpers.get_folder_id(path=self.settings["accounting_root"])
        self.settings["accounting_folder_id"] = accounting_folder_id

        print(f"Folder used {self.settings['accounting_root']} - id={self.settings['accounting_folder_id']}")

        self.account_data = account_data_loader.load_account_data_from_google(
            drive_api_helpers=drive_api_helpers,
            sheets_api_helpers=sheets_api_helpers,
            accouting_folder_id=self.settings["accounting_folder_id"],
            local_save_folder=self.settings["local_saved_data_location"]
        )

    def _display_totals(self, field):
        if self.account_data is None:
            print("ERROR No data loaded")
            return
        daily_totals = self.account_data.get_totals(field)
        sorted_days = list(daily_totals.keys())
        sorted_days.sort()
        max_key_len = len(max(sorted_days, key=len))
        for day in sorted_days:
            print(f"{((' ' * max_key_len) + day)[-max_key_len:]}, {format_decimal_for_display(daily_totals[day])}")
        print("")


    def cmd_display_daily_totals(self):
        return self._display_totals("day_name")

    def cmd_display_cetegory_totals(self):
        return self._display_totals("category")
