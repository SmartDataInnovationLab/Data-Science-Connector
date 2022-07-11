from intake.source import base
import pandas as pd

class ConnectorSource(base.DataSource):
    container = 'dataframe'
    version = '0.0.1'
    partition_access = False
    name = 'connector'

    def __init__(self, metadata=None):
        super(ConnectorSource, self).__init__(metadata=metadata)

    def _get_schema(self):
        # schema will depend on offer metadata
        self._dtypes = {
            'number': 'int', 
            'title': 'str'
        }
        
        return base.Schema(
            datashape=None,
            dtype=self._dtypes,
            shape=(None, len(self._dtypes)),
            npartitions=1,  # This data is not partitioned, so there is only one partition
            extra_metadata={}
        )

    def _get_partition(self, _):
        data = {
            'number': [1, 2, 3],
            'title': ['A', 'B', 'C']
        }

        return pd.DataFrame(data)
        
    def _close(self):
        pass