import os
from smtplib import SMTP
from email.mime.text import MIMEText
from config import *


def do_send_mail(results_filename, msg_subject, msg_to):
    if os.path.isfile(results_filename):

        content = open(results_filename).read()
        try:
            msg = MIMEText(content, "plain")
            msg['Subject'] = msg_subject
            msg['From'] = "{}".format(msg_from)
            msg['To'] = ", ".join(msg_to)
            conn = SMTP(smtp_hostname)
            conn.set_debuglevel(False)
            conn.ehlo()
            conn.starttls()
            conn.login(smtp_username, smtp_password)
            conn.sendmail(msg_from, msg_to, msg.as_string())
            conn.close()
            return True
        except Exception as e:
            print("Mail failed - {}".format(e))
            return False
