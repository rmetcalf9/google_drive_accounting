import json
import inquirer
from appObj import appObj

import account_data_loader
from google_client import GoogleClient, DriveApiHelpers, SheetsApiHelpers
from googleapiclient.discovery import build

settings_file_name="./settings.json"

global_account_data = None
global_settings = None

if __name__ == '__main__':
    appObj = appObj(settings_file_name=settings_file_name)


    print("Start")




    options = []
    options.append(("Load new data from google", load_new_data_from_google))
    options.append(("Display",  print_all))
    options.append(("Quit", None))
    questions = [
        inquirer.List('action',
                      message="What do you want to do?",
                      choices=options,
                      ),
    ]
    while True:
        answers = inquirer.prompt(questions)
        if answers["action"] is None:
            print("Quitting")
            exit(0)
        answers["action"]()

    print("End")
    exit(0)
