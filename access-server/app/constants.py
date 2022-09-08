from pathlib import Path
from datetime import timedelta

DATA_PATH = './access-server-data'
DB_FILE_PATH='./db.sqlite'
API_KEY_NAME = "access_token"
MAX_ID = 254
VALIDITY_DURATION = timedelta(minutes=30)
SSH_USERNAME_LEN = 8
SSH_PASS_LEN = 8

PLACEHOLDER_SUBNETID = 'PLACEHOLDER_SUBNETID'
PLACEHOLDER_SSH_PASS = 'PLACEHOLDER_SSH_PASS'
PLACEHOLDER_SSH_USER = 'PLACEHOLDER_SSH_USER'

def instance_path(id: int, token: str) -> Path:
    return Path(DATA_PATH) / str(id) / token