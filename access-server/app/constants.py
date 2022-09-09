from pathlib import Path
from datetime import timedelta

DATA_PATH = './access-server-data'
DB_FILE_PATH='./db.sqlite'
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
    'SSH_HOST': 'httpssomething'
}
