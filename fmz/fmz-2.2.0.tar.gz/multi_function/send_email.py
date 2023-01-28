# encoding = utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(title: str, text: str, name: str, receiver: str):
    try:
        sender = '2372769798@qq.com'
        password = "dttkrtttevtvdicg"
        smtp_address = "smtp.qq.com"
        port = 465
        message = MIMEText(text, 'html', 'utf-8')
        multi_msg = MIMEMultipart()
        multi_msg.attach(message)
        multi_msg['Subject'] = title
        multi_msg['From'] = name
        multi_msg['To'] = receiver
        content = multi_msg.as_string()
        server = smtplib.SMTP_SSL(smtp_address, port)
        server.login(sender, password)
        server.sendmail(sender, receiver, content)
        server.quit()
        return True
    except:
        return False