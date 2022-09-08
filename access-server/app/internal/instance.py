import os
from datetime import datetime
from app.model.instance import Instance
from app.constants import *

import zipfile
from random import choice
from string import ascii_lowercase, digits

IDS_DIR = os.path.join(os.path.dirname(__file__), 'ids-dir.zip')

def username():
    return ''.join(choice(ascii_lowercase) for i in range(SSH_USERNAME_LEN))
def password():
    return ''.join(choice(digits + ascii_lowercase) for i in range(SSH_PASS_LEN))

def create_instance(id: int, start_date: datetime, user_token: str) -> Instance:
    path = instance_path(id ,user_token)
    end_date = start_date + VALIDITY_DURATION
    ssh_user = username()
    ssh_pass = password()

    instance = Instance(id=id, path=str(path), start_date=start_date, end_date=end_date, user_token=user_token, ssh_user=ssh_user, ssh_pass=ssh_pass)

    with zipfile.ZipFile(IDS_DIR, 'r') as zip_ref:
        zip_ref.extractall(instance.path)

    code = os.system('/usr/bin/bash -c "cd ' + str(path)
        + ' && sed -i \'s/PLACEHOLDER_SUBNETID/' + str(id)
        + '/g; s/PLACEHOLDER_SSH_PASS/' + ssh_pass
        + '/g; s/PLACEHOLDER_SSH_USER/' + ssh_user
        + '/g\' docker-compose.yml'
        + ' && docker-compose up -d"')

    if code != 0:
        raise Exception('unknown error in the application (error code 36731609)')

    return instance

def stop_instance(instance: Instance):
    code = os.system('/usr/bin/bash -c "cd ' + str(instance.path)
        + ' && docker-compose down --remove-orphans"')

    if code != 0:
        raise Exception('unknown error in the application (error code 49721610)')