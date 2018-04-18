import requests
import pprint
import os
import csv
import urllib.request

scotch_csv = sys.argv[1]
subscription_key = sys.argv[1]
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

scotch_list = []
with open(scotch_csv, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        print(row[1])
        scotch_list.append(row[1])
print(scotch_list)

for scotch in scotch_list:
    print(scotch)
    img_dir = "content/images/" + scotch
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    search_term = scotch + " Bottle"
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": search_term, "textDecorations":False, "count": 10}
    params["offset"] = 50
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    for value in search_results["value"]:
        url = value["contentUrl"]
        print(url)
        filename = url.split("/")[-1]
        file_name = img_dir + "/" + filename
        try:
            urllib.request.urlretrieve(url, file_name)
        except:
            print("Got error for (" + scotch + ") :" + url)
    #pprint.pprint(search_results)
