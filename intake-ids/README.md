# intake-ids

This is an [intake](https://intake.readthedocs.io/en/latest) plugin that provides drivers and a catalog for [local artifacts](https://international-data-spaces-association.github.io/DataspaceConnector/CommunicationGuide/v6/Provider#step-2-add-data) in an [International Data Spaces](https://internationaldataspaces.org/) [connector](https://github.com/International-Data-Spaces-Association/DataspaceConnector). It automates contract negotiation, deprecation and re-negotiation processes needed for data access from connectors. 

A catalog provides a list of processable Resources in an IDS Connector. A Resource is only included (processable) in the catalog if it has at least one Representation with a supported mimetype. These are currently:

- text/csv

Future formats could include Parquet and JSON.

## Installation

`intake-ids` is published on [PyPI](https://pypi.org/project/intake-ids/).
You can install it by running the following in your terminal:
```bash
pip install intake-ids
```

You can test the functionality by opening the example notebook in the `examples/` directory.

## Usage

The package can be imported using
```python
from intake_ids import ConnectorCatalog
```

### Loading a catalog

You can load from a remote IDS Connector `provider` by providing the URLs for both the local connector and the remote connector `provider` and the authentication tuple for the local connector:
```python
provider_url = "https://provider:8080"
consumer_url = "https://consumer:8080"

catalog = ConnectorCatalog(provider_url=provider_url, consumer_url=consumer_url, name="testcat", auth=("admin", "password"))
len(list(catalog))
```

By default, ConnectorCatalog will combine all "IDS Catalog"s in the connector into one catalog. You can select the "IDS Catalog" using `catalog_id`.
```python
catalog_id   = "https://provider:8080/api/catalogs/eda0cda2-10f2-4b39-b462-5d4f2b1bb758"

catalog = ConnectorCatalog(provider_url=provider_url, consumer_url=consumer_url, catalog_id=catalog_id, name="testcat", auth=("admin", "password"))
```

You can display the resources (items) in the catalog
```python
for entry_id, entry in catalog.items():
    display(entry)
```

If the catalog has too many entries to comfortably print all at once,
you can narrow it by searching for a term (e.g. 'motion'):
```python
for entry_id, entry in catalog.search('motion').items():
  display(entry)
```

### Loading an artifact
Once you have identified a resource/representation you want to use, you can load it into a dataframe using `read()` or `read_chunked()`:

```python
df = pd.concat(entry.read_chunked())
```

or

```python
df = entry.read()
```

This will automatically load that dataset into the specified container for the driver for the entry.

## Command line tools
The plugin provides the `intake-ids-periodic-cleanup` script for periodic validation and cleanup of the cache. You can use the following crontab to run this script every 5 minutes.

```
*/5 * * * * $HOME/.local/bin/intake-ids-periodic-cleanup
```

## Details

Processable (Resource, Representation)-pair entries are then included in the catalog and matched to an available driver specialized for it's type. 
Alongside the entries themselves are also metadata from the Representation and cursory information about the usage policy (Rules) and access rights (ContractOffer) of the Resource.

### Drivers and Agreement caching

Drivers for entries allow for reading Artifacts by sorting through all the ContractOffers available for the Resource and negotiating an Agreement using one of them. If no valid ContractOffer exists for the Resource, an error is thrown. If otherwise multiple valid ContractOffers exist for the Resource, a preferable (artifact-cacheable) offer is selected. ContractAgreements are cached on the system and reused the next time the Resource is read/requested by the user if they are still valid without negotiating a new Agreement. If the cached Agreement is not valid (eg. expired) at any point, it (and all other associated items, including it's artifacts, see the next section) is removed from the cache and the process for agreement negotiation takes place again.

Currently following drivers exist:

driver | mimetypes | container
------ | --------- | ---------
ConnectorCSV | text/csv | pandas.dataframe

### Artifact caching

Depending on the determined usage control pattern (found out by inspecting Rules in the Agreement) for the Resource they are part of, some Artifacts can be cached by the driver in the local filesystem and used directly the next time they are requested. Before each read from the cache, the driver checks the continued validity of the Agreement and evalutes the usage control restrictions, clearing the agreement/artifact from the cache if the results come negative.

#### Cache support for usage patterns

Following the specifications of the [IDSA Position Paper about Usage Control](https://internationaldataspaces.org/wp-content/uploads/dlm_uploads/IDSA-Position-Paper-Usage-Control-in-the-IDS-V3..pdf), the IDS defines 21 policy classes.
The IDS Dataspace Connector [currently implements 9](https://international-data-spaces-association.github.io/DataspaceConnector/Documentation/v6/UsageControl#policy-patterns) of these.
Of the remaining 9 usage patterns, intake-ids offers artifact- and agreement-caching (full caching) support for 4 patterns, remaining 5 are agreement-cached only.

No. | Title                                          | artifact caching | agreement caching | support by IDS Dataspace Connector | description
--- | ---------------------------------------------- | ---------------- | ----------------- | ---------------------------------- | -----------
1   | Allow the Usage of the Data                    | x                | x                 | x                                  | provides data usage without any restrictions
2   | Connector-restricted Data Usage                |                  | x                 | x                                  | allows data usage for a specific connector
3   | Application-restricted Data Usage              |                  |                   |                                    |	 
4   | Interval-restricted Data Usage                 | x                | x                 | x                                  | provides data usage within a specified time interval
5   | Duration-restricted Data Usage                 | x                | x                 | x                                  | allows data usage for a specified time period
6   | Location Restricted Policy                     |                  |                   |                                    |	 
7   | Perpetual Data Sale (Payment once)             |                  |                   |                                    |	 
8   | Data Rental (Payment frequently)               |                  |                   |                                    |	 
9   | Role-restricted Data Usage                     |                  |                   |                                    |	 
10  | Purpose-restricted Data Usage Policy           |                  |                   |                                    |	 
11  | Event-restricted Usage Policy                  |                  |                   |                                    |	 
12  | Restricted Number of Usages                    |                  | x                 | x                                  | allows data usage for n times
13  | Security Level Restricted Policy               |                  | x                 | x                                  | allows data access only for connectors with a specified security level
14  | Use Data and Delete it After                   | x                | x                 | x                                  | allows data usage within a specified time interval with the restriction to delete it at a specified time stamp
15  | Modify Data (in Transit)                       |                  |                   |                                    |	 
16  | Modify Data (in Rest)                          |                  |                   |                                    |	 
17  | Local Logging                                  |                  | x                 | x                                  | allows data usage and sends logs to a specified Clearing House
18  | Remote Notifications                           |                  | x                 | x                                  | allows data usage and sends notification message
19  | Attach Policy when Distribute to a Third-party |                  |                   |                                    |	 
20  | Distribute only if Encrypted                   |                  |                   |                                    |	 
21  | State Restricted Policy                        |                  |                   |                                    |

### Periodic policy validation

The plugin includes a console script `intake-ids-periodic-cleanup` that evaluates all stored Agreements and usage control restrictions and removes invalid ones from the cache. It is provided as a command line tool and installed to your `$PATH` if the plugin was downloaded via pip/installed with setuptools. You can use this tool in a cronjob to make sure that usage policies are upheld even when the plugin is not in use.

## Requirements
```
install_requires =
    intake>=0.6.5
    pandas>=1.4.3
    requests>=2.28.1
    pydantic>=1.10.1
    isodate>=0.6.1
    appdirs>=1.4.4
python_requires = >=3.10
```