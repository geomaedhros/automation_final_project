#!/usr/bin/env python3

import os
from types import DynamicClassAttribute
import requests
import re
import json
import sys
import reports 
import report_email
from datetime import date


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
                    json_data = json.dump(fruits_dict) # vs. .dumps - creates JSON type
                    r = requests.post(out_url, json=json_data)
                    print(json_data)
                    print(r)

            except FileNotFoundError:
                continue # continue iteration if there is no file with the given name

        else:
            continue

create_json_dict(in_dir)


def main(argv):
    """Process the JSON data, generate a full report out of it and send it via mail."""
    
    # creates report 
    today = date.today().strftime("%d/%m/%Y") # dd/mm/YY
    attachment = '/tmp/processed.pdf'
    title = "Processed Update on {}".format(today)

    #Turns the data in dict into a list of lists.
    table_data = [["name", "weight"]]
    for keys, values in dict.fruits_items():
        table_data.append([keys, values])

    paragraph = ""
    for line in table_data:
        paragraph += "name: "+str(line[1]) + "<br/>"
        paragraph += "weight: "+str(line[1]) + "<br/>" + "<br/>"
    
    reports.generate_report(attachment, title, paragraph)

    # send the PDF report as an email attachment

    sender =  "automation@example.com"
    receiver = "{}@example.com".format(os.environ.get('USER'))
    subject = "Upload Completed - Online Fruit Store"
    body =  "All fruits are uploaded to our website successfully. A detailed list is attached to this email."

    message = report_email.generate(sender, receiver, subject, body, attachment)
    report_email.send_email(message)

if __name__ == "__main__":
    main(sys.argv)