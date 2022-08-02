import io
import json
from intake.source import base
from abc import ABCMeta, abstractmethod
import pandas as pd

from .idsapi import IdsApi
from .resourceapi import ResourceApi

class ConnectorSource(base.DataSource):
    container = 'dataframe'
    # how to deal with multiple dataframes / set of series?
    version = '0.0.1'
    partition_access = False
    name = 'connector'

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

    def _get_schema(self):
        # schema will depend on offer metadata
        self._dtypes = self.ids_metadata()
        
        return base.Schema(
            datashape=None,
            dtype=self._dtypes,
            shape=(None, len(self._dtypes)),
            npartitions=1,  # This data is not partitioned, so there is only one partition
            extra_metadata={}
        )

    def _get_partition(self, _):
        content = self.ids_data()

        return pd.read_csv(io.StringIO(content.decode('utf-8')), names=self._dtypes.keys())
        
    def _close(self):
        pass