#!/usr/bin/env python3

import os
import requests
import re
import json


"""
REFERENCE - Desired .JSON format:

{"name": "Watermelon", "weight": 500, "description": "Watermelon is good for relieving heat, eliminating annoyance 
and quenching thirst. It contains a lot of water, which is good for relieving the symptoms of acute fever immediately. 
The sugar and salt contained in watermelon can diuretic and eliminate kidney inflammation. Watermelon also contains 
substances that can lower blood pressure.", "image_name": "010.jpeg"}

"""
json_dict = {}
in_dir = "/home/{}/supplier-data/descriptions".format(os.environ.get('USER')) # input directory: /home/USER/.../descriptions/
url = "http://localhost/upload/"

def create_json_dict(in_path):
    """ takes textfiles from in_path and processes them into the desired .JSON format """

    # regex to find txt extensions
    regex = r"((\.txt)$)"
    prod = re.compile(regex, re.IGNORECASE)

    # iterate through textfiles in the folder, ignoring subfolders and upload to json file
    txt_paths = [filename for pth, dirs, files in os.walk(in_path) for filename in files] 
    for f in txt_paths:
        json_dict[f] = {}
        if (re.search(prod, f)): # only iterates through files with txt extensions
            try:
                with open(in_path+"/"+f, "r") as description_f:
                    id = str(f).strip(".txt")
                    json_dict[f]["id"] = id
                    name = description_f.readline()
                    json_dict[f]["name"] = name.strip("\n")
                    weight = description_f.readline()
                    json_dict[f]["weight"] = weight.strip("\n")
                    description = description_f.readline()
                    json_dict[f]["description"] = description.strip("\n")
                    image_name = str(f).strip(".txt")+".jpeg"
                    json_dict[f]["image_name"] = image_name

            except FileNotFoundError:
                continue # continue iteration if there is no file with the given name

        else:
            continue

create_json_dict(in_dir)

def upload_json_dict(out_url):
    """ Upload JSON dictionary """

    # iterate through json_dict and upload JSON file to url
    for item in json_dict:
        json_item = json.dumps(item)
        r = requests.post(out_url, json=json_item)
        r.json()
        print(json_item)

    print("Upload to {} successful".format(out_url))

upload_json_dict("http://localhost/fruits/")

print("JSON dict successfully exported")