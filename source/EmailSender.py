#!/usr/bin/python

# http://naelshiab.com/tutorial-send-email-python/
# http://www.tutorialspoint.com/python/python_sending_email.htm

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

class EmailSender:

    def __init__(self, server, port):
        self.server = smtplib.SMTP(server, port)
        self.server.starttls()

    def login(self, login, password):
        self.fromaddr = login
        self.server.login(login, password)

    def send(self, toaddr, msg):
        self.server.sendmail(self.fromaddr, toaddr, msg)

    def send_with_attachment(self, toaddr, subject, body, file_path):
        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        attachment = open(file_path, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % file_path)
        msg.attach(part)
        self.send(toaddr, msg.as_string())

    def quit(self):
        self.server.quit()
