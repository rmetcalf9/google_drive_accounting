import json
import inquirer

import account_data_loader
from google_client import GoogleClient, DriveApiHelpers, SheetsApiHelpers
from googleapiclient.discovery import build

settings_file_name="./settings.json"

if __name__ == '__main__':
    settings = None
    with open(settings_file_name, "r") as fileHandle:
        settings = json.load(fileHandle)

    print("Start")

    google_client = GoogleClient( settings["google_credentials_file"], settings["temporary_token_file"])
    creds = google_client.get_creds()
    drive_api_helpers = DriveApiHelpers(drive_service=build('drive', 'v3', credentials=creds))
    sheets_api_helpers = SheetsApiHelpers(sheets_service=build('sheets', 'v4', credentials=creds))

    if "accounting_folder_id" not in settings:
        print("Searching for id of accounting folder...")
        accounting_folder_id = drive_api_helpers.get_folder_id(path=settings["accounting_root"])
        settings["accounting_folder_id"] = accounting_folder_id
        with open(settings_file_name, 'w') as outfile:
            json.dump(settings, outfile, indent=4)

    print(f"Folder used {settings['accounting_root']} - id={settings['accounting_folder_id']}")

    account_data = account_data_loader.load_account_data(
        drive_api_helpers=drive_api_helpers,
        sheets_api_helpers=sheets_api_helpers,
        accouting_folder_id=settings["accounting_folder_id"]
    )

    print("End")
    exit(0)
