#!/usr/bin/env python3

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

"""
Creates PDF report
"""

def generate(filename, title, data):
  styles = getSampleStyleSheet()
  report = SimpleDocTemplate(filename)
  report_title = Paragraph(title, styles["h3"])
  report_info = Paragraph(data, styles["BodyText"])
  empty_line = Spacer(1,3)
  report.build([report_title, empty_line, report_info, empty_line])
