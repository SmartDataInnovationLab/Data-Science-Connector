#!/usr/bin/env python3


from resourceapi import ResourceApi

connector = ResourceApi("http://provider-dataspace-connector")
artifact = connector.create_artifact(
    data={
        "title": "string",
        "description": "string",
        "accessUrl": "https://string",
        "basicAuth": {"key": "string", "value": "string"},
        "apiKey": {"key": "string", "value": "string"},
        "value": "string",
        "automatedDownload": True,
    }
)

success = connector.update_artifact(
    artifact=artifact,
    data={
        "title": "string",
        "description": "string",
        "accessUrl": "https://string",
        "basicAuth": {"key": "string", "value": "string"},
        "apiKey": {"key": "string", "value": "string"},
        "value": "string",
        "automatedDownload": True,
    },
)

exit(not success)  # Exit success == 0 but True == 1
