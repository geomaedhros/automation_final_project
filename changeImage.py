#!/usr/bin/env python3

import os
import re
from PIL import Image
from PIL import UnidentifiedImageError

def reformat_img(in_path, out_path):
    """ takes images from in_path and converts them to defined format """

    # regex to find image extensions
    regex = r"((\.)(jpe?g|png|gif|jfif|bmp|tiff)$)"
    prod = re.compile(regex, re.IGNORECASE)

    # iterate through files in the image folder, ignoring folders
    img_paths = [filename for pth, dirs, files in os.walk(in_path) for filename in files] 
    for f in img_paths:
        if (re.search(prod, f)): # only iterates through files with image extensions
            try:
                img = Image.open(in_path+"/"+f) # open original image
                rsz_img = img.resize((600, 400)) # resizes the image
                new_img = rsz_img.convert("RGB") # converts image to RGB in order to save it
                new_fname = re.sub(prod, ".jpeg", f) # replaces extension with .jpeg
                new_img.save(out_path+"/"+new_fname, "JPEG") # rename, relocate and save with different format#


            except FileNotFoundError:
                continue # continue iteration if there is no file with the given name

        # if file has no extension, function adds and saves as .jpeg while not throwing errors
        elif os.path.splitext(f)[1] == "":  
            try:
                img = Image.open(in_path+"/"+f) # open original image
                rsz_img = img.resize((600, 400)) # resize the image
                new_img = rsz_img.convert("RGB") # convert image to RGB in order to save it
                new_fname = os.path.splitext(f)[0]+".jpeg" # adds .jpeg extension
                new_img.save(out_path+"/"+new_fname, "JPEG") # rename, relocate and save with different format#
                print(out_path+"/"+new_fname)
                    
            except FileNotFoundError:
                continue # continue iteration if there is no file with the given name

            except UnidentifiedImageError:
                continue # continue iteration if the file format is not correct
            
        else:
            continue

def del_old_img(in_path):
    """ takes old images from in_path and deletes them"""

    # regex to find image extensions that are not jpeg/jpg
    regex = r"((\.)(png|gif|jfif|bmp|tiff)$)"
    prod = re.compile(regex, re.IGNORECASE)

    # iterate through files in the image folder, ignoring folders
    img_paths = [filename for pth, dirs, files in os.walk(in_path) for filename in files] 
    for f in img_paths:
        if (re.search(prod, f)): # only iterates through files with image extensions
            try:
                os.remove(in_path+"/"+f) # remove original image

            except FileNotFoundError:
                continue # continue iteration if there is no file with the given name

            except UnidentifiedImageError:
                continue # continue iteration if the file format is not correct

        else:
            continue

in_dir = "/home/{}/supplier-data/images".format(os.environ.get('USER')) # input directory: /home/USER/.../images
out_dir = "/home/{}/supplier-data/images".format(os.environ.get('USER')) # output directory: /home/USER/.../images

reformat_img(in_dir, out_dir)
del_old_img(in_dir)

print("Image conversion completed.\n")