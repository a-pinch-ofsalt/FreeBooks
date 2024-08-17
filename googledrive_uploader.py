from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    creds = None
    # Load environment variables
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    # Check for existing credentials
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no valid credentials, prompt for login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config({
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
                }
            }, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for future runs
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

credentials = authenticate_google_drive()


# Build the Google Drive API service
drive_service = build('drive', 'v3', credentials=credentials)

# Folder name
folder_name = 'FreeBooks'

# Check if the folder already exists
query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
response = drive_service.files().list(q=query, fields='files(id, name)').execute()
folder = response.get('files', [])

if not folder:
    # Folder doesn't exist, create it
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
    folder_id = folder.get('id')
else:
    # Folder exists, retrieve its ID
    folder_id = folder[0].get('id')

def uploadBookToGoogleDrive(bookTitle, bookFilepath):
    file_metadata = {
        'name': bookTitle + '.epub', 
        'parents': [folder_id]  # Specify the folder ID
    }

    media = MediaFileUpload(bookFilepath, mimetype='application/epub+zip')

    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
