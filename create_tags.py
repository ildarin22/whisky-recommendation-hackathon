#!/usr/local/bin/python3
 
import requests
import pprint
import os
import csv
import sys
import urllib.request
import urllib.parse

training_key = sys.argv[1]
project_id = sys.argv[2]

if not training_key or not project_id:
    print('Missing training_key or project_id')
    exit

base_url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v1.1/Training/projects/" + project_id + "/tags"

def create_tags(scotch_list, training_key, base_url):
    scotch_tags = {}
    for scotch in scotch_list:
        print("processing " + scotch)
        # Bad developers need to be taken out and shot for multiple ?
        url = base_url + "?name=" + urllib.parse.quote_plus(scotch)
        headers = { "Training-key" : training_key }
        #print(url)
        #pprint.pprint(headers)
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        scotch_tags[scotch] = result['Id']
        #pprint.pprint(result)

def get_scotch_list(scotch_file):
    scotch_list = []
    with open(scotch_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            print(row[1])
            scotch_list.append(row[1])
    return scotch_list


scotch_list = get_scotch_list('content/data/whisky.csv')
scotch_tags = create_tags(scotch_list, training_key, base_url)
pprint.pprint(scotch_tags)
