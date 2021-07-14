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
out_url = "http://localhost/fruits"

def create_json_dict(in_path):
    """ takes textfiles from in_path and processes them into the desired .JSON format """

    # regex to find txt extensions
    regex = r"((\.txt)$)"
    prod = re.compile(regex, re.IGNORECASE)
    fruits_dict = {}

    # iterate through textfiles in the folder, ignoring subfolders and upload to json file
    txt_paths = [filename for pth, dirs, files in os.walk(in_path) for filename in files] 
    for f in txt_paths:
        if (re.search(prod, f)): # only iterates through files with txt extensions
            try:
                with open(in_path+"/"+f, "r") as description_f:
                    lines = description_f.readlines()
                    id = int(str(f).strip(".txt"))
                    fruits_dict["id"] = id
                    fruits_dict["name"] = lines[0].strip("\n")
                    fruits_dict["weight"] = int(lines[1].strip("\n").strip(" lbs"))
                    fruits_dict["description"] = lines[2].strip("\n")
                    image_name = str(f).strip(".txt")+".jpeg"
                    fruits_dict["image_name"] = image_name

                    # iterate through json_dict and upload JSON file to url
                    json_data = json.dumps(fruits_dict)
                    r = requests.post(out_url, json=json_data)
                    print(json_data)
                    print(r)

            except FileNotFoundError:
                continue # continue iteration if there is no file with the given name

        else:
            continue

create_json_dict(in_dir)

print("JSON dict successfully exported")