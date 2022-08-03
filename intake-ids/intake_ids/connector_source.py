import json
from intake.source import base
from abc import ABCMeta, abstractmethod

from .idsapi import IdsApi
from .resourceapi import ResourceApi

def driver_args(representation, resource, provider_url, consumer_url):
    return {
        "provider_url": provider_url,
        "consumer_url": consumer_url,
        "representation": representation['@id'],
        "resource": resource['@id'],
    }

class ConnectorSource(base.DataSource, metaclass=ABCMeta):
    def __init__(self, provider_url, consumer_url, resource, representation, metadata=None):
        self.provider_url = provider_url
        self.consumer_url = consumer_url
        self.resource = resource
        self.representation = representation
        self.consumer = IdsApi(consumer_url)
        self.consumerResources = ResourceApi(consumer_url)

        super(ConnectorSource, self).__init__(metadata=metadata)

    def ids_artifact(self):
        rep = self.consumer.descriptionRequest(self.provider_url + "/api/ids/data", self.representation)
        if not "ids:instance" in rep or len(rep["ids:instance"]) <= 0:
            raise ValueError('Representation doesn\'t contain artifact')

        return rep["ids:instance"][0]["@id"]

    def ids_metadata(self):
        rep = self.consumer.descriptionRequest(self.provider_url + "/api/ids/data", self.representation)
        if not "dtypes" in rep:
            raise ValueError('Representation doesn\'t contain intake dtypes')
        dtypes = json.loads(rep["dtypes"])

        return dtypes

    def ids_data(self):
        offer = self.consumer.descriptionRequest(self.provider_url + "/api/ids/data", self.resource)
        obj = offer["ids:contractOffer"][0]["ids:permission"][0]
        artifact = self.ids_artifact()
        obj["ids:target"] = artifact

        response = self.consumer.contractRequest(
            self.provider_url + "/api/ids/data", self.resource, artifact, False, obj
        )

        # Pull data
        agreement = response["_links"]["self"]["href"]
        artifacts = self.consumerResources.get_artifacts_for_agreement(agreement)
        first_artifact = artifacts["_embedded"]["artifacts"][0]["_links"]["self"]["href"]
        
        return self.consumerResources.get_data(first_artifact).content

    @abstractmethod
    def _get_schema(self):
        pass

    @abstractmethod
    def _get_partition(self, _):
        pass
    
    def _close(self):
        pass