from pathlib import Path
from datetime import timedelta
import appdirs

dir = Path(appdirs.user_data_dir('access-server-for-intake-ids-user-study'))
dir.mkdir(parents=True, exist_ok=True)

DATA_PATH = dir / 'access-server-data'
DB_FILE_PATH = dir / 'db.sqlite'
API_KEY_NAME = "access_token"
MAX_ID = 254
VALIDITY_DURATION = timedelta(minutes=30)
SSH_USERNAME_LEN = 8
SSH_PASS_LEN = 8
SSH_PORT_START = 43400

def instance_path(id: int, token: str) -> Path:
    return Path(DATA_PATH) / str(id) / token

def ssh_workaround_path(path: Path) -> Path:
    return path / 'ssh-workaround' / '88-enable_forwarding'

def provider_url(id: int):
    return 'https://172.23.' + str(id) + '.10:8080'

CONFIG = {
    'SSH_HOST': 'ds-connector.sdil.de',
    'IDS_PROVIDER_PREFIX': 'https://provider',
    'IDS_PROVIDER_POSTFIX': ':8080',
    'IDS_CONSUMER_PREFIX': 'https://consumer',
    'IDS_CONSUMER_POSTFIX': ':8080',
}
