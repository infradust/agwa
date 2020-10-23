import json
import base64
import smtplib
import os
from email.message import EmailMessage
from typing import Dict, Any, List


LABELS = os.getenv('DETECTION_LABELS')
LABELS = frozenset(label.lower() for label in LABELS.split(',')) if LABELS else {'plant'}
SMTP = os.getenv('SMTP_HOST') or 'localhost'
EMAIL_TO = os.getenv('EMAIL_TO') or 'test@test.com'
EMAIL_FROM = os.getenv('EMAIL_FROM') or 'planter@test.com'
SUBJECT = os.getenv('EMAIL_SUBJECT') or 'Plant detected'


def send_email(sender, s3_file: str):
    msg = EmailMessage()
    msg.set_content(s3_file)
    msg['Subject'] = SUBJECT
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    sender.send_message(msg)


def handler(event, context):
    sender = smtplib.SMTP()

    for record in event['Records']:
        info = json.loads(base64.b64decode(record['data']))
        detection: Dict[str, Any] = info['detection']
        labels: List[Dict[str, Any]] = detection['Labels']
        detected = any(label['Name'].lower() in LABELS for label in labels)
        if detected:
            send_email(sender, info['s3'])

    sender.quit()
