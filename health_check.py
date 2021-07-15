#!/usr/bin/env python3
import shutil
import psutil
import socket
import requests
from emails import generate_error_report, send_email

# Variable definition
disk_to_check = "/mnt/c/"
disk_usage_percent = 20
cpu_usage_percent = 80
url_to_check = "http://www.google.de"
host_to_check = "127.0.0.1"

def check_disk_usage(disk, disk_percent):
    """Verifies that there's enough free space on disk"""
    du = shutil.disk_usage(disk)
    free = du.free / du.total * 100
    return free > disk_percent

def check_cpu_usage(cpu_percent):
    """Verifies that there's enough unused CPU"""
    usage = psutil.cpu_percent(1)
    return usage > cpu_percent

def check_connectivity(url):
    """Verifies that there is connection to the url"""
    request = requests.get(url) # returns status
    return request == 200

def check_localhost(host_name):
    localhost = socket.gethostbyname('localhost') # gets host by name e.g. 127.0.0.1
    return localhost == host_name

# If there's not enough disk or CPU, no connectivity or wrong host, print an error
if not check_disk_usage(disk_to_check, disk_usage_percent):
    error_message = "DISK ERROR! - Space in {} below {}%.".format(disk_to_check, disk_usage_percent)

if not check_cpu_usage(cpu_usage_percent)):
    error_message = "CPU ERROR! - CPU usage above {}%.".format(cpu_usage_percent)

if not check_connectivity(url_to_check):
    error_message = "CONNECTIVITY ERROR! Not able to reach {}".format(url_to_check)

if not check_localhost(host_to_check):
    error_message = "LOCALHOST ERROR! Host does not correspond to {}.".format(host_to_check)

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
