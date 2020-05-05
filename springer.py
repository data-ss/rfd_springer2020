import pandas as pd
import requests
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from tqdm import tqdm

### Functions and calls to Google Pydrive to automatically upload to Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

def createDriveFolder(folderName):
    folder_metadata = {'title' : folderName, 'mimeType' : 'application/vnd.google-apps.folder'}
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    foldertitle = folder['title']
    folderid = folder['id']
    print('title: %s, id: %s' % (foldertitle, folderid))
    return folderid

def uploadDriveFile(folderid, file_path):
    file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folderid}], 'title': os.path.basename(os.path.abspath(file_path))})
    file.SetContentFile(os.path.abspath(file_path))
    file.Upload()
###

txtcsv = pd.read_excel("downloadURL.xlsx")

for i in tqdm(txtcsv["English Package Name"].unique()):
    os.makedirs(i) # create directory
    os.chdir(i) # change working directory into new directory
    drive_id = createDriveFolder(i)
    count = txtcsv["PDF download URL"][txtcsv["English Package Name"] == i].count() # tally up how many books in this field
    print(f"\nDownloading {count} books in the {i} field.\n")
    for j in tqdm(txtcsv["PDF download URL"][txtcsv["English Package Name"] == i]):
        title = txtcsv["Book Title"][txtcsv["PDF download URL"]==j].values[0].replace("/", " or ")
        # "/" is not a valid character for naming files or folders so they need to be replaced
        print(f"\nAccessing book: {title}.\n")
        r = requests.get(j, auth=('user', 'pass'))
        open(f"\n{title}.pdf", 'wb').write(r.content)
        if os.path.isfile(f"{title}.pdf"):
            print(f"\n{title} is now in the {i} folder.\n")
        else:
            print(f"\n{title} failed to download.\n")
        uploadDriveFile(drive_id, f"{title}.pdf")
    os.chdir("..")
    print(f"\nAll books in the {i} category have been downloaded.\n")
