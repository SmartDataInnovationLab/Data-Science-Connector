from .connector_controller import ConnectorController
from intake.source import base
from io import StringIO

class ConnectorCSVSource(base.DataSource):
    container = 'dataframe'
    version = '0.0.1'
    partition_access = True
    name = 'connector_csv'

    def __init__(self, ids_kwargs=None, csv_kwargs=None, metadata=None):
        self.ids = ConnectorController(**ids_kwargs)

        super(ConnectorCSVSource, self).__init__(metadata=metadata)

    def _get_schema(self):
        return base.Schema(
            datashape=None,
            dtype=None,
            shape=None,
            npartitions=self.ids.num_partitions(),
            extra_metadata={}
        )

    def _get_partition(self, i):
        import pandas as pd
        modal = self.ids.get_data_modality(i)
        if modal.can_filename:
            return pd.read_csv(modal.filename())
        elif modal.can_inmemory:
            return pd.read_csv(StringIO(modal.inmemory().decode('utf-8')))
        else:
            raise ValueError('Can\'t access partition')
