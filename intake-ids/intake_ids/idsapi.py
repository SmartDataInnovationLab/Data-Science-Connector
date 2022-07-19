

import requests
import json

# Suppress ssl verification warning
requests.packages.urllib3.disable_warnings()


class IdsApi:
    session = None
    recipient = None

    def __init__(self, recipient, auth=("admin", "password")):
        self.session = requests.Session()
        self.session.auth = auth
        self.session.verify = False

        self.recipient = recipient

    def descriptionRequest(self, recipient, elementId = None):
        url = self.recipient + "/api/ids/description"
        params = {}
        if recipient is not None:
            params["recipient"] = recipient
        if elementId is not None:
            params["elementId"] = elementId

        response = self.session.post(url, params=params)
        return json.loads(response.text)

    def contractRequest(self, recipient, resourceId, artifactId, download, contract):
        url = self.recipient + "/api/ids/contract"
        params = {}
        if recipient is not None:
            params["recipient"] = recipient
        if resourceId is not None:
            params["resourceIds"] = resourceId
        if artifactId is not None:
            params["artifactIds"] = artifactId
        if download is not None:
            params["download"] = download

        response = self.session.post(
            url, params=params, json=self.toListIfNeeded(contract)
        )
        return json.loads(response.text)

    def toListIfNeeded(self, obj):
        if isinstance(obj, list):
            return obj
        else:
            return [obj]
