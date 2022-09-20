import anomalies_tracker
import tabulate
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from configuration import db_connections as db
from configuration import config
import email_sender
from pretty_html_table import build_table
import os


class Anomaly:

    def __init__(self, anomaly_type_id, anomaly_type_name, handling_by, id_name, key_reference_id, query, file_name,
                 mail_to, subject, intro_mail, slack_channel_code):
        self.anomaly_type_id = anomaly_type_id
        self.anomaly_type_name = anomaly_type_name
        self.handling_by = handling_by
        self.id_name = id_name
        self.key_reference_id = key_reference_id
        self.query = query
        self.file_name = file_name
        if file_name is not None:
            self.file_path = '../' + os.path.join(config.EXCEL_PATH, self.file_name)
        else:
            self.file_path = None

        self.mail_to = mail_to
        self.subject = subject
        self.intro_mail = intro_mail
        self.end_mail = 'Best Of Luck,\nAnomaly Detection Engine'
        self.slack_channel_code = slack_channel_code

    def applying_anomaly(self):
        df = db.importDataFromPG(self.query)
        if len(df) > 0:
            anomalies_tracker.tracking_anomalies(df, self.id_name, self.anomaly_type_id, self.anomaly_type_name,
                                                 self.handling_by, self.key_reference_id)

            # f = df.to_excel(self.file_path)
            table = build_table(df, config.TABLE_COLOR)
            email_sender.send_mail(self.subject, table, self.intro_mail, self.end_mail, self.mail_to, self.file_name,
                                   self.file_path)
            if self.slack_channel_code is not None:
                try:
                    a = tabulate.tabulate(df)
                    print(a)
                    client = WebClient(token=config.SLACK_TOKEN)
                    f_res = client.files_upload(file=self.file_path, channels=self.slack_channel_code,
                                                initial_comment=self.subject + "\n" + self.intro_mail + "\n", )

                except SlackApiError as e:
                    print(f"Error: {e}")

        else:
            anomalies_tracker.close_all(self.anomaly_type_id)