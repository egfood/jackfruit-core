from abc import abstractmethod

import json_logging
import logging
import sys


class AbstractEmailSender:

    @abstractmethod
    def send_email(self, email_origin: str, email_subject: str, email_text: str, *recipients: list):
        """
        Send email
        Returns response when email was sent
        Or throws Exception
        """
        pass

    def send(self, *args):
        """
        send_email() wrapper
        catches the exception and logged it
        returns the email response or exception
        """
        try:
            return self.send_email(*args)
        except Exception as e:
            json_logging.ENABLE_JSON_LOGGING = True
            json_logging.init_non_web()
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.ERROR)
            logger.addHandler(logging.StreamHandler(sys.stdout))
            logger.error(e)
            return e
