#!/usr/bin/env python3


import requests

# Suppress ssl verification warning
requests.packages.urllib3.disable_warnings()


class SubscriptionApi:
    session = None
    recipient = None

    def __init__(self, recipient, auth=("admin", "password")):
        self.session = requests.Session()
        self.session.auth = auth
        self.session.verify = False

        self.recipient = recipient

    def create_subscription(self, data={}):
        response = self.session.post(self.recipient + "/api/subscriptions", json=data)
        return response.headers["Location"]

    def subscription_message(self, data={}, params={}):
        response = self.session.post(
            self.recipient + "/api/ids/subscribe", json=data, params=params
        )
        return response

    def get_subscriptions(self):
        response = self.session.get(self.recipient + "/api/subscriptions")
        return response
