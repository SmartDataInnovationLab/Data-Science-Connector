from __future__ import annotations
from .debug import *
import json
from pydantic import ValidationError

from .vendor.idsapi import IdsApi
from .cache import Cache
from .ids_information_model.contract import Contract
from .ids_information_model.artifact import Artifact
from .usage_control.contract import is_artifact_cacheable, select_valid_contract_by_preferable_rules, is_contract_valid_for_artifact
from .exceptions import ConnectorError, raise_for_connector_status


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
        self.cache = Cache(consumer_url, provider_url, resource_url, representation_url)

    def _get_artifacts(self):
        rep = self.consumer.descriptionRequest(self.provider_url + "/api/ids/data", self.representation)
        if not "ids:instance" in rep or len(rep["ids:instance"]) <= 0:
            raise ValueError('Representation doesn\'t contain any artifacts')

        return rep["ids:instance"]

    def _obtain_agreement(self, partition):
        if (self.cache.get_agreement(partition) is not None):
            display('Using cache for agreement')
            return self.cache.get_agreement(partition)

        # select artifact based on partition
        artifacts = self._get_artifacts()
        artifact_meta_dict = artifacts[partition]
        artifact_meta = Artifact.parse_obj(artifact_meta_dict)

        res = self.consumer.descriptionRequest(self.provider_url + "/api/ids/data", self.resource)
        offer_dict = select_valid_contract_by_preferable_rules(res["ids:contractOffer"], artifact_meta)

        if offer_dict is None:
            raise ConnectorError("No valid contracts available for this resource")

        display('New agreement')
        # negotiate contract
        rules = offer_dict.get("ids:permission", []) + offer_dict.get("ids:prohibition", [])
        for rule in rules:
            rule["ids:target"] = artifact_meta.id

        response: dict = self.consumer.contractRequest(
            self.provider_url + "/api/ids/data", self.resource, artifact_meta.id, False, rules
        )

        # make sure we've gotten a contract agreement and not an error message
        try:
            Contract.parse_raw(response.get('value', ''))
        except ValidationError as e:
            print(response)
            raise e

        agreement_dict = json.loads(response['value'])
        agreement = Contract.parse_obj(agreement_dict)

        self.cache.cache_agreement(agreement_dict, artifact_meta_dict, partition)
        return agreement, artifact_meta

    def get_data_modality(self, partition=0) -> AccessModality:
        agreement, artifact = self._obtain_agreement(partition)

        return AccessModality(controller=self, cacheable=is_artifact_cacheable(agreement), artifact_id=artifact.id, partition=partition)

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
        
        display('We are a cacheable artifact')
        if self._controller.cache.has_artifact(self._partition):
            display('Using cache for ARTIFACT')
            return self._controller.cache.get_artifact_filename(self._partition)

        # if contract is not valid (or not valid for artifact), there is nothing we can do, error 
        if not self._controller.cache.check_validity(self._partition):
            raise ConnectorError('Agreement for the resource is not valid')

        display('Trying to write new artifact to cache')
        with self._controller.consumer.stream_data(self._artifact_id) as r:
            raise_for_connector_status(r)
            display('streaming to cache')
            self._controller.cache.cache_artifact(r, self._partition)
        
        return self._controller.cache.get_artifact_filename(self._partition)

    def inmemory(self):
        display('We are NOT a cacheable artifact')
        r = self._controller.consumer.get_data(self._artifact_id)
        raise_for_connector_status(r)
        print('bypassed cache')
        return r.content
        
