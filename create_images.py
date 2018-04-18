#!/usr/local/bin/python3

import requests
import pprint
import os
import csv
import urllib.request
import urllib.parse

bing_subscription_key = sys.argv[1]
training_key = sys.argv[2]
project_id = sys.argv[3]

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
training_url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v1.1/Training/projects/"

def post_image_data(tag_id, urls):
    data = { "TagIds": [ tag_id ], "Urls": urls }
    create_image_url = training_url + project_id + "/images/url"
    print(create_image_url)
    pprint.pprint(data)
    create_image_headers = { "Training-key": training_key }
    r = requests.post(create_image_url, headers=create_image_headers, data=data)
    r.raise_for_status()

def create_images_from_scotch_tags(scotch_tags):
    pprint.pprint(scotch_tags)
    for scotch_name in scotch_tags:
        tag_id = scotch_tags[scotch_name]
        print("Processing " + scotch_name)
        urls = get_image_urls(scotch_name)
        if urls:
            post_image_data(tag_id, urls)

def get_scotch_tags():
    url = training_url + project_id + "/tags"
    headers = { "Training-key": training_key }
#    print(url)
#    print(headers)
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    results = r.json()
    response = {tag['Name']: tag['Id'] for tag in results['Tags']}
    return response

def get_image_urls(scotch):
    search_term = scotch + " Bottle"
    headers = {"Ocp-Apim-Subscription-Key" : bing_subscription_key}
    params  = {"q": search_term, "textDecorations":False, "count": 10}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    urls = [v["contentUrl"] for v in search_results["value"]]
    return urls


scotch_tags = get_scotch_tags()
create_images_from_scotch_tags(scotch_tags)
#post_image_data('f99bdc3d-88cf-43ea-b146-fcbcb1abbb24', ["https://www.whisky.com/typo3temp/GB/044ef18811.jpg", "http://www.awardrobeofwhisky.com/bottle/miniature-aberfeldy-12-year-bottle_front_image.jpg"])
