#!/usr/bin/env python3


from resourceapi import ResourceApi
from idsapi import IdsApi
import pprint
import sys

provider_url = "https://provider:8080"
consumer_url = "https://consumer:8080"

print("Starting script")
# Provider
provider = ResourceApi(provider_url)

## Create resources
dataValue = "5,aaa\n6,bbb\n7,ccc\n"
catalog = provider.create_catalog()
offers = provider.create_offered_resource()
representation = provider.create_representation(data={"dtypes": """{
    "number": "int",
    "title": "str"
}"""})
artifact = provider.create_artifact(data={"value": dataValue})
contract = provider.create_contract()
use_rule = provider.create_rule()

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

# # Consumer
# consumer = IdsApi(consumer_url)

# # IDS
# # Call description to get all offers
# all_offers = consumer.descriptionRequest(provider_url + "/api/ids/data")
# print("All Offers")
# pprint.pprint(all_offers)
# # Call description for a spec offer, I use the one created above, but you may retrieve it from all_offers
# offer = consumer.descriptionRequest(provider_url + "/api/ids/data", offers)
# print("Offer", offers)
# pprint.pprint(offer)

# # Negotiate contract
# obj = offer["ids:contractOffer"][0]["ids:permission"][0]
# # You will agree to the provided contract offer by using it for the contract request without content changes.
# # You just have to add the artifact id as ids:target to the rule.
# obj["ids:target"] = artifact
# print("Obj")
# pprint.pprint(obj)
# print("Offer", offers)
# pprint.pprint(offer)
# response = consumer.contractRequest(
#     provider_url + "/api/ids/data", offers, artifact, False, obj
# )

# print("Response")
# pprint.pprint(response)

# # Pull data
# agreement = response["_links"]["self"]["href"]

# consumerResources = ResourceApi(consumer_url)
# artifacts = consumerResources.get_artifacts_for_agreement(agreement)
# print("Artifacts")
# pprint.pprint(artifacts)

# first_artifact = artifacts["_embedded"]["artifacts"][0]["_links"]["self"]["href"]
# pprint.pprint(first_artifact)

# data = consumerResources.get_data(first_artifact).text
# pprint.pprint(data)

# if data != dataValue:
#     exit(1)

# exit(0)
