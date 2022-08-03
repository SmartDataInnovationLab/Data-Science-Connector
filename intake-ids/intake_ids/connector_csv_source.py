from .connector_source import ConnectorSource
from intake.source import base
import pandas as pd
import io

class ConnectorCSVSource(ConnectorSource):
    container = 'dataframe'
    version = '0.0.1'
    partition_access = False
    name = 'connector_csv'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        self._get_schema()
        content = self.ids_data()

        return pd.read_csv(io.StringIO(content.decode('utf-8')), names=self._dtypes.keys())