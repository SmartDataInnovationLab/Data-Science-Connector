from scripts.resourceapi import ResourceApi
from scripts.idsapi import IdsApi

def create_dummy_data(repr_kwargs, data_value, provider, catalog, rule_value = None):
    offers = provider.create_offered_resource()
    representation = provider.create_representation(**repr_kwargs)
    artifact = provider.create_artifact(data={"value": data_value})
    contract = provider.create_contract()
    use_rule = provider.create_rule() if rule_value == None else provider.create_rule(data={"value": rule_value})

    ## Link resources
    provider.add_resource_to_catalog(catalog, offers)
    provider.add_representation_to_resource(offers, representation)
    provider.add_artifact_to_representation(representation, artifact)
    provider.add_contract_to_resource(offers, contract)
    provider.add_rule_to_contract(contract, use_rule)

    print("Created provider resources")
    print("resource", offers)
    print("repr", representation)
    print("artifact", artifact)