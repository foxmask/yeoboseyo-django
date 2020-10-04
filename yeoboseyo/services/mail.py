# coding: utf-8
"""
   여보세요 Service Mail
"""
# std lib
from __future__ import unicode_literals
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import getLogger
import smtplib
# yeoboseyo
from yeoboseyo.services import Service

# create logger
logger = getLogger(__name__)

__all__ = ['Mail']


class Mail(Service):

    email_server = 'localhost'
    email_sender = 'root'
    email_receiver = ''

    def __init__(self):
        """
        init parms
        """
        super().__init__()
        self.email_server = settings.EMAIL_SERVER
        self.email_sender = settings.EMAIL_SENDER
        self.email_receiver = settings.EMAIL_RECEIVER

    def save_data(self, trigger, entry) -> bool:
        """
        Send a new mail
        :param trigger: current trigger
        :param entry: data from Feeds
        :return: boolean
        """
        logger.debug("%s From: %s - To: %s - Title: %s" %
                     (self.email_server, self.email_sender, self.email_receiver, entry.title))

        body = self.create_body_content(trigger.description, entry)

        msg = MIMEMultipart('alternative')

        part1 = MIMEText(body.encode('utf-8'), 'plain', 'utf-8')
        part2 = MIMEText(body.encode('utf-8'), 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)

        msg['Subject'] = entry.title
        msg['From'] = self.email_sender
        msg['To'] = self.email_receiver

        with smtplib.SMTP(self.email_server) as s:
            s.sendmail(self.email_sender, self.email_receiver, msg.as_string())
            return True
