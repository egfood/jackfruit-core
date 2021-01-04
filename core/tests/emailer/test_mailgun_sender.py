import json
from unittest import TestCase
import requests_mock
from core.emailer.mailgun_sender import MailGunSender
from environs import Env


class AdminUrlsTest(TestCase):

    def setUp(self):
        env = Env()
        self.sender = MailGunSender("MAILGUN_API_KEY", "domain")

    @requests_mock.Mocker()
    def test_send_email(self, m):
        m.post('https://api.mailgun.net/v3/domain/messages', text=json.dumps({"message": "Queued. Thank you."}))
        response = self.sender.send("mail@mail.organicfood.by", "subject", "text", ["client@gmail.com"])
        assert response["message"] == "Queued. Thank you."
