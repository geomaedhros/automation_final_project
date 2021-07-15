#!/usr/bin/env python3

import reports
import emails
import os 
from datetime import date


BASEPATH_SUPPLIER_TEXT_DES = os.path.expanduser('~') + '/supplier-data/descriptions/'
list_text_files = os.listdir(BASEPATH_SUPPLIER_TEXT_DES)

report = []

def process_data(data):
for item in data:
report.append("name: {}<br/>weight: {}\n".format(item[0], item[1]))
return report

text_data = []
for text_file in list_text_files:
with open(BASEPATH_SUPPLIER_TEXT_DES + text_file, 'r') as f:
text_data.append([line.strip() for line in f.readlines()])
f.close()

if __name__ == "__main__":

summary = process_data(text_data)

# Generate a paragraph that contains the necessary summary
paragraph = "<br/><br/>".join(summary)

# Generate the PDF report
title = "Processed Update on {}\n".format(date.today().strftime("%B %d, %Y"))
attachment = "/tmp/processed.pdf"

reports.generate_report(attachment, title, paragraph)

# Send the email
subject = "Upload Completed - Online Fruit Store"
sender = "automation@example.com"
receiver = "{}@example.com".format(os.environ.get('USER'))
body = "All fruits are uploaded to our website successfully. A detailed list is attached to this email."
message = emails.generate_email(sender, receiver, subject, body, attachment)
emails.send_email(message)

Health_check.py script for Automate updating catalog information

#! /usr/bin/env python3

import os
import shutil
import psutil
import socket
from emails import generate_error_report, send_email

def check_cpu_usage():
    """Verifies that there's enough unused CPU"""
    usage = psutil.cpu_percent(1)
    return usage > 80

def check_disk_usage(disk):
    """Verifies that there's enough free space on disk"""
    du = shutil.disk_usage(disk)
    free = du.free / du.total * 100
    return free > 20

def check_available_memory():
    """available memory in linux-instance, in byte"""
    available_memory = psutil.virtual_memory().available/(1024*1024)
    return available_memory > 500

def check_localhost():
    """check localhost is correctly configured on 127.0.0.1"""
    localhost = socket.gethostbyname('localhost')
    return localhost == '127.0.0.1'

if check_cpu_usage():
    error_message = "CPU usage is over 80%"
elif not check_disk_usage('/'):
    error_message = "Available disk space is less than 20%"
elif not check_available_memory():
    error_message = "Available memory is less than 500MB"
elif not check_localhost():
    error_message = "localhost cannot be resolved to 127.0.0.1"
else:
    pass

# send email if any error reported
if __name__ == "__main__":
    try:
        sender = "automation@example.com"
        receiver = "{}@example.com".format(os.environ.get('USER'))
        subject = "Error - {}".format(error_message)
        body = "Please check your system and resolve the issue as soon as possible"
        message = generate_error_report(sender, receiver, subject, body)
        send_email(message)
    except NameError:
        pass