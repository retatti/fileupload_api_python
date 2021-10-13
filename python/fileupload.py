from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/drive']

def set_api():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # creds = flow.run_local_server(port=5000)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    return service

def upload(service, fname, ftype):
    file_metadata = {'name': fname}
    media = MediaFileUpload(fname, mimetype=ftype)
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    # print('File ID: %s' % file.get('id'))
    return file.get('id')

def set_share(service, fid):
    service.permissions().create(body={"role":"reader", "type":"anyone"}, fileId=fid).execute()

def get_link(service, fid):
    page_token = None
    flink = None
    # query = "mimeType = 'plain/text'"

    while True:
        response = service.files().list(spaces='drive',
                                            fields='nextPageToken, files(id, name, webViewLink)',
                                            pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            if file.get('id') == fid:
                flink = file.get('webViewLink')
            # print('Found file: %s (%s) (%s)' % (file.get('id'), file.get('name'), file.get('webViewLink')))
        page_token = response.get('nextPageToken', None)
        if page_token is None or not flink is None:
            break

    return flink


def display(service):
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(*)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)



def main():
    # Post PDF file

    fname = 'test.txt'
    ftype = 'plain/text'

    # Set info of the Drive v3 API 
    service = set_api()

    # Upload PDF file to google drive 
    fid = upload(service, fname, ftype)

    # Set up shared file
    set_share(service, fid)

    # Get share link of uploaded PDF file
    flink = get_link(service, fid)

    if flink is None:
        raise Exception

    # Delete PDF file on the server

    # Return share link
    print(flink)

    return flink




if __name__ == '__main__':
    main()