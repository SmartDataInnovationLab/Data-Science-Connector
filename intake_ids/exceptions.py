from requests import Response

class ConnectorError(Exception):
    pass

def raise_for_connector_status(r: Response):
    if 400 <= r.status_code < 500:
        raise ConnectorError(str(r.status_code) + ": " + str(r.content))
    else:
        r.raise_for_status()