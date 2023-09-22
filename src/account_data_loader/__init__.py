import account_data as ad
from google_client import MIMETYPE_FOLDER, MIMETYPE_SPREADSHEET
import os
import shutil

latest_loaded_from_google_file_name="/latest_loaded_from_google.dat"

def load_from_latest_saved(local_save_folder):
    if not os.path.exists(f"{local_save_folder}{latest_loaded_from_google_file_name}"):
        return None
    account_data = ad.AccountData()
    account_data.load_from_file(filename=f"{local_save_folder}{latest_loaded_from_google_file_name}")
    return account_data

def load_account_data_from_google(drive_api_helpers, sheets_api_helpers, accouting_folder_id, local_save_folder):
    account_data = ad.AccountData()

    (files, request) = drive_api_helpers.get_all_items_in_folder(folder_id=accouting_folder_id,restrict_mimetype=[MIMETYPE_FOLDER])
    while request is not None:
        result = request.execute()
        for file in result["files"]:
            spreadsheet_id = get_spreadsheet_for_day(drive_api_helpers, file["id"], file["name"])
            load_day(sheets_api_helpers=sheets_api_helpers, spreadsheet_id=spreadsheet_id, day_name=file["name"], account_data=account_data)
        request = files.list_next(request, result)

    if local_save_folder==None:
        raise Exception("ERROR")
    if local_save_folder.strip()=="":
        raise Exception("ERROR")
    if local_save_folder.strip()=="/":
        raise Exception("ERROR")
    if local_save_folder.strip()==".":
        raise Exception("ERROR")
    if local_save_folder[-1]=="/":
        raise Exception("ERROR")
    if os.path.exists(local_save_folder):
        shutil.rmtree(local_save_folder)
    os.mkdir(local_save_folder)
    account_data.save_to_file(filename=f"{local_save_folder}{latest_loaded_from_google_file_name}")

    return account_data

def get_spreadsheet_for_day(drive_api_helpers, day_folder_id, day_name):
    (files, request) = drive_api_helpers.get_all_items_in_folder(folder_id=day_folder_id,restrict_mimetype=[MIMETYPE_SPREADSHEET])
    if request is None:
        raise Exception(f"Loading day {day_name}- no spreadsheet present")
    spread_sheets=[]
    while request is not None:
        result = request.execute()
        for file in result["files"]:
            spread_sheets.append(file)
        request = files.list_next(request, result)
    if len(spread_sheets) != 1:
        raise Exception("0 or more than one spreadsheets in accounting folder")

    return spread_sheets[0]['id']

def load_day(sheets_api_helpers, spreadsheet_id, day_name, account_data):
    print(f"Loading {day_name} spreadsheet = {spreadsheet_id}...")
    metadata = sheets_api_helpers.get_sheet_metadata(sheet_id=spreadsheet_id)
    if len(metadata["sheets"]) != 1:
        raise Exception(f"More than one sheet in worksheet for {day_name}")
    sheet = metadata["sheets"][0]

    result = sheets_api_helpers.sheets_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet["properties"]["title"],
        valueRenderOption='FORMATTED_VALUE',
        dateTimeRenderOption='SERIAL_NUMBER'
    ).execute()
    values = result.get('values', [])
    if not values:
        print(f'No data found in sheet for {day_name}.')
        return
    for row in values:
        load_sheet_row(row=row, day_name=day_name, account_data=account_data)

def load_sheet_row(row, day_name, account_data):
    if len(row)==0:
        return
    if row[0]=="":
        return
    details=""
    if len(row)==5:
        details=row[4]
    else:
        if len(row) < 4:
            raise Exception(f"{day_name} Not enough data in row")
    account_data.add_reciept_line(
        day_name=day_name,
        company=row[0],
        method=row[1],
        category=row[2],
        amount=row[3],
        details=details
    )
