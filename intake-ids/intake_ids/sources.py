def _mimetype(repr):
    return repr.get('ids:mediaType', {}).get('ids:filenameExtension')

def get_source_for_representation(repr):
    if test_csv(repr):
        return "connector_csv", {}
    
    return None

def test_csv(repr):
    return _mimetype(repr) == 'text/csv'