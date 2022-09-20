from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
from email.mime.application import MIMEApplication
from configuration import config


def cred():
    config = configparser.ConfigParser()
    config.read('configuration/alerts.ini')
    username = config['alerts']['username']
    password = config['alerts']['password']
    return username, password


# def send_mail(subject='Management Fee - Monthly Report', body_start_message='', body_table=None, body_end_message='',
#               mail_to=['matan@home365.co'], file='Management_fee.xlsx'):
#
#     sender_email, password = cred()
#     message = MIMEMultipart()
#     message['Subject'] = subject
#     message['From'] = sender_email
#     # message['To'] = mail_to
#     if len(mail_to) == 1:
#         receiver_email = mail_to[0]
#         message['To'] = receiver_email
#     else:
#         message['To'] = ", ".join(mail_to)
#
#     part1 = MIMEText(body_start_message, 'plain')
#     part2 = MIMEText(body_table, 'html')
#     part3 = MIMEText(body_end_message, 'plain')
#     message.attach(part1)
#     message.attach(part2)
#     message.attach(part3)
#
#     server = SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login(message['From'], password)
#     if file is not None:
#         with open(file, "rb") as f:
#             attach = MIMEApplication(f.read())
#             attach.add_header('Content-Disposition', 'attachment', filename=file)
#             message.attach(attach)
#     server.send_message(message)
#     # server.sendmail(message['From'], message['To'], msg_body)
#     server.quit()
#
# # email_sender.send_mail(body_start_message=fee_tool.body_start_message, body_table_count=body_count_table,
# #                        body_table_amount=body_amount_table, body_end_message=fee_tool.body_end_message,
# #                        mail_to=fee_tool.email_to)
#
#
# def send_mail(subject='Payments Summary - Daily Report', body_start_message='', body_table_count=None,
#               table_count_headline='', total_amount_headline='', body_table_amount=None, body_end_message='',
#               mail_to=['matan@home365.co']):
#
#     sender_email, password = cred()
#     message = MIMEMultipart()
#     message['Subject'] = subject
#     message['From'] = sender_email
#     # message['To'] = mail_to
#     if len(mail_to) == 1:
#         receiver_email = mail_to[0]
#         message['To'] = receiver_email
#     else:
#         message['To'] = ", ".join(mail_to)
#
#     part1 = MIMEText(body_start_message, 'plain')
#     part2 = MIMEText(table_count_headline, 'plain')
#     part3 = MIMEText(body_table_count, 'html')
#     part4 = MIMEText(total_amount_headline, 'plain')
#     part5 = MIMEText(body_table_amount, 'html')
#     part6 = MIMEText(body_end_message, 'plain')
#     message.attach(part1)
#     message.attach(part2)
#     message.attach(part3)
#     message.attach(part4)
#     message.attach(part5)
#     message.attach(part6)
#
#     server = SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login(message['From'], password)
#     server.send_message(message)
#     server.quit()


def send_mail(subject, table, body_start_message, body_end_message, mail_to, file_name, file_path):

    sender_email = config.MAIL_USERNAME
    password = config.MAIL_PASSWORD
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    # message['To'] = mail_to
    if len(mail_to) == 1:
        receiver_email = mail_to[0]
        message['To'] = receiver_email
    else:
        message['To'] = ", ".join(mail_to)

    message.attach(MIMEText(body_start_message, 'plain'))
    if table is not None:
        message.attach(MIMEText(table, 'html'))

    # for headline, table in tables.items():
    #     message.attach(MIMEText(headline, 'plain'))
    #     message.attach(MIMEText(table, 'html'))
    message.attach(MIMEText(body_end_message, 'plain'))


    server = SMTP('smtp.gmail.com', 587)
    # server = SMTP('smtp.mail.yahoo.com', 465)
    server.starttls()
    server.login(message['From'], password)
    if file_path is not None:
        with open(file_path, "rb") as f:
            attach = MIMEApplication(f.read())
            attach.add_header('Content-Disposition', 'attachment', filename=file_name)
            message.attach(attach)
    server.send_message(message)
    server.quit()


# def send_mail(subject, body_start_message, body_end_message, mail_to):
#     sender_email, password = cred()
#     message = MIMEMultipart()
#     message['Subject'] = subject
#     message['From'] = sender_email
#     # message['To'] = mail_to
#     if len(mail_to) == 1:
#         receiver_email = mail_to[0]
#         message['To'] = receiver_email
#     else:
#         message['To'] = ", ".join(mail_to)
#
#     part1 = MIMEText(body_start_message, 'plain')
#     part2 = MIMEText(body_end_message, 'plain')
#
#     message.attach(part1)
#     message.attach(part2)
#
#     server = SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login(message['From'], password)
#     server.send_message(message)
#     server.quit()
