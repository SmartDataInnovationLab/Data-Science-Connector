#!/usr/bin/env python3


import pprint
import sys

from idsapi import IdsApi
from resourceapi import ResourceApi

provider_url = "http://provider-dataspace-connector"
consumer_url = "http://consumer-dataspace-connector"


def main(argv):
    if len(argv) == 2:
        provider_url = argv[0]
        consumer_url = argv[1]
        print("Setting provider alias as:", provider_url)
        print("Setting consumer alias as:", consumer_url)


if __name__ == "__main__":
    main(sys.argv[1:])

print("Starting script")

# Provider
provider = ResourceApi(provider_url)

## Create resources
dataValue = "SOME LONG VALUE"
catalog = provider.create_catalog()
offers = provider.create_offered_resource()
representation = provider.create_representation()
artifact = provider.create_artifact(data={"value": dataValue})
contract = provider.create_contract()
use_rule = provider.create_rule(
    data={
        "value": """{
  "@context" : {
    "ids" : "https://w3id.org/idsa/core/",
    "idsc" : "https://w3id.org/idsa/code/"
  },
  "@type" : "ids:Permission",
  "@id" : "https://w3id.org/idsa/autogen/permission/d504b82f-79dd-4c93-969d-937ab6a1d676",
  "ids:description" : [ {
    "@value" : "connector-restriction",
    "@type" : "http://www.w3.org/2001/XMLSchema#string"
  } ],
  "ids:title" : [ {
    "@value" : "Example Usage Policy",
    "@type" : "http://www.w3.org/2001/XMLSchema#string"
  } ],
  "ids:action" : [ {
    "@id" : "idsc:USE"
  } ],
  "ids:constraint" : [ {
    "@type" : "ids:Constraint",
    "@id" : "https://w3id.org/idsa/autogen/constraint/572c96ec-dd86-4b20-a849-a0ce8c255eee",
    "ids:rightOperand" : {
      "@value" : "https://w3id.org/idsa/autogen/baseConnector/7b934432-a85e-41c5-9f65-669219dde4ea",
      "@type" : "http://www.w3.org/2001/XMLSchema#anyURI"
    },
    "ids:leftOperand" : {
      "@id" : "idsc:SYSTEM"
    },
    "ids:operator" : {
      "@id" : "idsc:SAME_AS"
    }
  } ]
}"""
    }
)

## Link resources
provider.add_resource_to_catalog(catalog, offers)
provider.add_representation_to_resource(offers, representation)
provider.add_artifact_to_representation(representation, artifact)
provider.add_contract_to_resource(offers, contract)
provider.add_rule_to_contract(contract, use_rule)

print("Created provider resources")

# Consumer
consumer = IdsApi(consumer_url)

# IDS
# Call description
offer = consumer.descriptionRequest(provider_url + "/api/ids/data", offers)
pprint.pprint(offer)

# Negotiate contract
obj = offer["ids:contractOffer"][0]["ids:permission"][0]
obj["ids:target"] = artifact
response = consumer.contractRequest(
    provider_url + "/api/ids/data", offers, artifact, False, obj
)
pprint.pprint(response)

# Pull data
agreement = response["_links"]["self"]["href"]

consumerResources = ResourceApi(consumer_url)
artifacts = consumerResources.get_artifacts_for_agreement(agreement)
pprint.pprint(artifacts)

first_artifact = artifacts["_embedded"]["artifacts"][0]["_links"]["self"]["href"]
pprint.pprint(first_artifact)

data = consumerResources.get_data(first_artifact).text
pprint.pprint(data)

if data != dataValue:
    exit(1)

exit(0)
