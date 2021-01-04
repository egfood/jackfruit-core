import json

from core.emailer.abstract_email_sender import AbstractEmailSender
import requests


class MailGunSender(AbstractEmailSender):

    def __init__(self, api_key, domain_name):
        self.__api_key__ = api_key
        self.__domain_name__ = domain_name

    def send_email(self, email_origin: str, email_subject: str, email_text: str, *recipients: list):
        """
        Returns response json when email was sent
        Or throws requests.exceptions.HTTPError
        """
        response = requests.post(
            "https://api.mailgun.net/v3/" + self.__domain_name__ + "/messages",
            auth=("api", self.__api_key__),
            data={"from": email_origin,
                  "to": recipients,
                  "subject": email_subject,
                  "html": email_text})
        if response.ok:
            return response.json()
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            mailgun_response = json.loads(e.response.text)
            mailgun_err = mailgun_response["message"]
            raise Exception(str(e)+" RESPONSE: "+mailgun_err)
