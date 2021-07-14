#!/usr/bin/env python3
import requests
import os
import re

# define path where images are located
in_path = "/home/{}/supplier-data/images".format(os.environ.get('USER'))

# define url to upload images to
url = "http://localhost/upload/"

# regex to find image extensions
regex = r"((\.)(jpe?g|png|gif|jfif|bmp|tiff)$)"
prod = re.compile(regex, re.IGNORECASE)

# iterate through files in the image folder, ignoring folders
img_paths = [filename for pth, dirs, files in os.walk(in_path) for filename in files] 
for f in img_paths:
    if (re.search(prod, f)): # only iterates through files with image extensions
        with open(in_path+'/'+f, 'rb') as opened:
            r = requests.post(url, files={'file': opened})

print("Upload to {} successful".format(url))