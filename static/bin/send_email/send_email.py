import smtplib

from static.bin.send_email import config
from static.bin.send_email import send


def send_email(name, mail, subject, message):
    msg = "From {} \n{} \n\n{}".format(name, mail, message)
    try:
        server = smtplib.SMTP("smtp.mail.ru")
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = "Subject: {}\n\n{}".format(subject, msg)
        server.sendmail(config.EMAIL_ADDRESS, send.SEND_ADDRESS, message)
        server.quit()
    except:
        print("ОШИБОЧКА)")
