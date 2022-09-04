from __future__ import annotations
from typing import Any

from .idsapi import IdsApi
from .resourceapi import ResourceApi
from .cache import Cache
from .ids_information_model.contract import Contract
from .usage_control.contract import is_artifact_cacheable, select_contract_by_preferable_rules
from .exceptions import raise_for_connector_status

def driver_args(representation, resource, provider_url, consumer_url):
    return {
        "provider_url": provider_url,
        "consumer_url": consumer_url,
        "representation_url": representation['@id'],
        "resource_url": resource['@id'],
    }

class ConnectorController():
    def __init__(self, provider_url, consumer_url, resource_url, representation_url):
        self.provider_url = provider_url
        self.consumer_url = consumer_url
        self.resource = resource_url
        self.representation = representation_url
        self.consumer = IdsApi(consumer_url)
        self.consumerResources = ResourceApi(consumer_url)
        self.cache = Cache(consumer_url, provider_url, resource_url, representation_url)

    def _get_artifacts(self):
        rep = self.consumer.descriptionRequest(self.provider_url + "/api/ids/data", self.representation)
        if not "ids:instance" in rep or len(rep["ids:instance"]) <= 0:
            raise ValueError('Representation doesn\'t contain any artifacts')

        return [x["@id"] for x in rep["ids:instance"]]

    def _obtain_agreement(self, partition):
        if (self.cache.get_agreement(partition) is not None):
            agreement = self.cache.get_agreement(partition)
            return agreement

        artifacts = self._get_artifacts()
        artifact = artifacts[partition]

        res = self.consumer.descriptionRequest(self.provider_url + "/api/ids/data", self.resource)
        offer = select_contract_by_preferable_rules(res["ids:contractOffer"])

        rules = offer.get("ids:permission", []) + offer.get("ids:prohibition", []) + offer.get("ids:obligation", [])
        for rule in rules:
            rule["ids:target"] = artifact
        
        response: dict = self.consumer.contractRequest(
            self.provider_url + "/api/ids/data", self.resource, artifact, False, rules
        )

        # make sure we've gotten a contract agreement and not an error message
        Contract.parse_raw(response.get('value', ''))

        # display(response)
        self.cache.cache_agreement(response, partition)

        return response

    def get_data_modality(self, partition=0) -> AccessModality:
        agreement = self._obtain_agreement(partition)

        agreement_content = Contract.parse_raw(agreement['value'])
        cacheable = is_artifact_cacheable(agreement_content)

        agreement_id = agreement["_links"]["self"]["href"]
        artifacts = self.consumerResources.get_artifacts_for_agreement(agreement_id)
        artifact_id = artifacts["_embedded"]["artifacts"][0]["_links"]["self"]["href"]

        return AccessModality(controller=self, cacheable=cacheable, artifact_id=artifact_id, partition=partition)

    def num_partitions(self):
        return len(self._get_artifacts())

class AccessModality:
    cacheable: bool
    can_filename: bool
    can_inmemory: bool

    _controller: ConnectorController
    _artifact_id: str
    _partition: int

    def __init__(self, controller, cacheable, artifact_id, partition) -> None:
        self.cacheable = cacheable
        self.can_filename = cacheable
        self.can_inmemory = not cacheable

        self._controller = controller
        self._partition = partition
        self._artifact_id = artifact_id

    def filename(self):
        if not self.cacheable:
            raise PermissionError('artifact is not cacheable')
        
        if (self._controller.cache.has_artifact(self._partition)):
            return self._controller.cache.get_artifact_filename(self._partition)

        print('streaming to cache')
        with self._controller.consumerResources.stream_data(self._artifact_id) as r:
            raise_for_connector_status(r)
            self._controller.cache.cache_artifact(r, self._partition)
        
        return self._controller.cache.get_artifact_filename(self._partition)

    def inmemory(self):
        print('bypassed cache')
        r = self._controller.consumerResources.get_data(self._artifact_id)
        raise_for_connector_status(r)
        return r.content
        
