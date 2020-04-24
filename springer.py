import pandas as pd
import os
import requests

txtcsv = pd.read_excel("downloadURL.xlsx")

for i in txtcsv["English Package Name"].unique():
    os.makedirs(i)
    os.chdir(i)
    count = txtcsv["PDF download URL"][txtcsv["English Package Name"] == i].count()
    print(f"Downloading {count} books in the {i} field.")
    for j in txtcsv["PDF download URL"][txtcsv["English Package Name"] == i]:
        title = txtcsv["Book Title"][txtcsv["PDF download URL"]==j].values[0]
        print(f"Accessing book: {title}.")
        r = requests.get(j, auth=('user', 'pass'))
        open(f"{title}.pdf", 'wb').write(r.content)
        if os.path.isfile(f"{title}.pdf"):
            print(f"{title} is now in the {i} folder.")
        else:
            print(f"{title} failed to download.")
    os.chdir("..")
    print(f"All books in the {i} category have been downloaded.")
