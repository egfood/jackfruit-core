import sys

from core.emailer.abstract_email_sender import AbstractEmailSender
import logging
import json_logging


class StubSender(AbstractEmailSender):

    def send_email(self, *args):
        json_logging.ENABLE_JSON_LOGGING = True
        json_logging.init_non_web()
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        logger.info(args)
        return True
