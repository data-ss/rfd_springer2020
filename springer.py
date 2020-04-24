import pandas as pd
import os
import requests

txtcsv = pd.read_excel("downloadURL.xlsx")

for i in txtcsv["English Package Name"].unique():
    os.makedirs(i) # create directory
    os.chdir(i) # change working directory into new directory
    count = txtcsv["PDF download URL"][txtcsv["English Package Name"] == i].count() # tally up how many books in this field
    print(f"Downloading {count} books in the {i} field.")
    for j in txtcsv["PDF download URL"][txtcsv["English Package Name"] == i]:
        title = txtcsv["Book Title"][txtcsv["PDF download URL"]==j].values[0].replace("/", " or ")
        # "/" is not a valid character for naming files or folders so they need to be replaced
        print(f"Accessing book: {title}.")
        r = requests.get(j, auth=('user', 'pass'))
        open(f"{title}.pdf", 'wb').write(r.content)
        if os.path.isfile(f"{title}.pdf"):
            print(f"{title} is now in the {i} folder.")
        else:
            print(f"{title} failed to download.")
    os.chdir("..")
    print(f"All books in the {i} category have been downloaded.")
