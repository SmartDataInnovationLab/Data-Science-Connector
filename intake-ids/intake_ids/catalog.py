from intake.catalog import Catalog
from intake.catalog.local import LocalCatalogEntry
from .connector_controller import driver_args
from .sources import get_source_for_representation

from .vendor.idsapi import IdsApi

class ConnectorCatalog(Catalog):
    # if only one catalog in ids, use it. otherwise load all
    def __init__(self, provider_url, consumer_url, name, auth=("admin", "password"), catalog_id=None, metadata=None, **kwargs):
        self.provider_url = provider_url
        self.consumer_url = consumer_url
        self.catalog_id = catalog_id

        self.consumer = IdsApi(consumer_url, auth)
        self.recipient_url = self.provider_url + "/api/ids/data"

        self._offers = {}

        super().__init__(name=name, metadata=metadata, **kwargs)

    def _load(self):
        if self.catalog_id is not None:
            self._load_catalog(self.catalog_id)
        else:
            connector = self.consumer.descriptionRequest(self.recipient_url)
            for cat in connector.get('ids:resourceCatalog', []):
                self._load_catalog(cat['@id'])

    def _load_catalog(self, catalog_id):
        catalog = self.consumer.descriptionRequest(self.recipient_url, catalog_id)
        for res in catalog.get('ids:offeredResource', []):
            self._load_resource(resource_id = res['@id'])
    
    def _load_resource(self, resource_id=None, resource=None):
        if resource_id is not None: 
            resource = self.consumer.descriptionRequest(self.recipient_url, resource_id)
        
        for rep in resource.get('ids:representation', []):
            self._load_repr(resource = resource, repr_id=rep['@id'])

    def _load_repr(self, resource, repr_id=None, repr=None):
        if repr_id is not None:
            repr = self.consumer.descriptionRequest(self.recipient_url, repr_id)
        
        if repr and is_processable_representation(repr):
            self._entries[repr['@id']] = ConnectorEntry(
                representation = repr,
                resource = resource,
                provider_url = self.provider_url,
                consumer_url = self.consumer_url
            )
        
def is_processable_representation(repr):
    return get_source_for_representation(repr) is not None

class ConnectorEntry(LocalCatalogEntry):
    def __init__(self, representation, resource, provider_url, consumer_url):
        driver, args = get_source_for_representation(representation)
        connector_args = driver_args(representation, resource, provider_url, consumer_url)
        name = representation['@id']
        description = f"""{resource['ids:title'][0]['@value']}
{resource['ids:description'][0]['@value']}"""
        super().__init__(name, description, driver, True, args={ **args, 'ids_kwargs': connector_args })
