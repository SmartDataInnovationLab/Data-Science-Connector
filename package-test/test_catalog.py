from intake_ids import ConnectorCatalog

# provider_url = "https://provider:8080"
# consumer_url = "https://consumer:8080"
provider_url = "https://connectorb:8081"
consumer_url = "https://connectora:8080"

catalog = ConnectorCatalog(provider_url=provider_url, consumer_url=consumer_url, name="testcat", auth=("admin", "password"))

print(len(list(catalog)))

last_entry = None
for entry_id, entry in catalog.items():
    last_entry = entry

for chunk in last_entry.read_chunked(): print(chunk)