import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from .drive import DriveApiHelpers
from .sheets import SheetsApiHelpers

SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readonly'
]

MIMETYPE_FOLDER="application/vnd.google-apps.folder"
MIMETYPE_SPREADSHEET="application/vnd.google-apps.spreadsheet"

class GoogleClient():
    credential_file = None
    temporary_token_file = None

    def __init__(self, credential_file, temporary_token_file):
        self.credential_file = credential_file
        self.temporary_token_file = temporary_token_file

    def get_creds(self):
        creds = None
        if os.path.exists(self.temporary_token_file):
            creds = Credentials.from_authorized_user_file(self.temporary_token_file, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except:
                    pass
            if not creds.valid:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credential_file, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.temporary_token_file, 'w') as token:
                token.write(creds.to_json())
        return creds
