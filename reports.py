#!/usr/bin/env python3

import csv
from datetime import date

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

"""
Creates PDF report
"""

dict = {}

with open('/mnt/c/users/geomaedhros/code_test/g_autom/test_report/transactions.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["city"] not in dict:
            dict[row["city"]] = 1

        else:
            dict[row["city"]] += 1
    
#Turns the data in dict into a list of lists.
table_data = [["test", "city",]]
for keys, values in dict.items():
    table_data.append([keys, values])

print_text = ""
for line in table_data:
    print_text += "name: "+str(line[1]) + "<br/>"
    print_text += "weight: "+str(line[1]) + "<br/>" + "<br/>"
print(print_text)

def generate(filename, title, data):
  styles = getSampleStyleSheet()
  report = SimpleDocTemplate(filename)
  report_title = Paragraph(title, styles["h3"])
  report_info = Paragraph(data, styles["BodyText"])
  empty_line = Spacer(1,3)
  report.build([report_title, empty_line, report_info, empty_line])

today = date.today().strftime("%d/%m/%Y") # dd/mm/YY
path = '/mnt/c/users/geomaedhros/code_test/g_autom/test_report/processed.pdf'

report_title = "Processed Update on {}".format(today)
generate(path, report_title, print_text)
