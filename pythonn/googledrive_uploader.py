import google.auth
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Path to your OAuth 2.0 credentials file
CLIENT_SECRETS_FILE = "client_secret_1005985003754-346uaprpsccoueoip1gm6cd6rsbtk4ha.apps.googleusercontent.com.json"

# Scopes for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Authentication flow to get credentials
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_local_server(port=0)

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
