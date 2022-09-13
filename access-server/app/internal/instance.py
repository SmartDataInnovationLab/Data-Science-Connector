import os
import zipfile
from time import sleep
from datetime import datetime
from random import choice
from string import ascii_lowercase, digits
from app.model.instance import Instance
from app.constants import *

from .resourceapi import ResourceApi

IDS_DIR = os.path.join(os.path.dirname(__file__), 'ids-dir.zip')
CSV_WEATHER = os.path.join(os.path.dirname(__file__), 'csv_weather')

def username():
    return ''.join(choice(ascii_lowercase) for i in range(SSH_USERNAME_LEN))
def password():
    return ''.join(choice(digits + ascii_lowercase) for i in range(SSH_PASS_LEN))

# https://stackoverflow.com/a/30463972/3873452
def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)

def create_instance(id: int, start_date: datetime, user_token: str) -> Instance:
    path = instance_path(id ,user_token)
    end_date = start_date + VALIDITY_DURATION
    ssh_user = username()
    ssh_pass = password()
    ssh_port = id + SSH_PORT_START

    instance = Instance(id=id, path=str(path), start_date=start_date, end_date=end_date, user_token=user_token, ssh_user=ssh_user, ssh_pass=ssh_pass, ssh_port=ssh_port)

    with zipfile.ZipFile(IDS_DIR, 'r') as zip_ref:
        zip_ref.extractall(instance.path)
    
    # make ssh workaround executable in docker 
    make_executable(ssh_workaround_path(path))

    try:
        code = os.system('/usr/bin/bash -c "cd ' + str(path)
            + ' && sed -i \'s/PLACEHOLDER_SUBNETID/' + str(id)
            + '/g; s/PLACEHOLDER_SSH_PASS/' + ssh_pass
            + '/g; s/PLACEHOLDER_SSH_USER/' + ssh_user
            + '/g; s/PLACEHOLDER_SSH_PORT/' + str(ssh_port)
            + '/g\' docker-compose.yml'
            + ' && docker-compose up -d"')

        if code != 0:
            raise Exception('unknown error in the application (error code 36731609)')

        # poke connector until it's ready
        cont = True
        retry = 1
        while cont:
            sleep(2.5)
            try:
                upload_sample_to_provider(provider_url=provider_url(id=instance.id))
                cont = False
            except Exception as e:
                if retry == 8:
                    raise e
                cont = True


        return instance
    except Exception as e:
        stop_instance(instance=instance)
        print('maybe time')
        raise e

def stop_instance(instance: Instance):
    print('stopping' + str(instance.id) + " " + instance.user_token)
    code = os.system('/usr/bin/bash -c "cd ' + str(instance.path)
        + ' && docker-compose down --remove-orphans"')

    if code != 0:
        raise Exception('unknown error in the application (error code 49721610)')

def upload_sample_to_provider(provider_url: str):
    print(provider_url)
    provider = ResourceApi(provider_url)
    catalog = provider.create_catalog()
    offers = provider.create_offered_resource(data={
    "title": "Daten der Wetterstation auf der Heinrich-Hübsch-Schule 2017",
    "description": "Daten der Wetterstation auf der Heinrich-Hübsch-Schule 2017",
    "keywords": [
        "wetter",
        "weather"
    ],
    "publisher": "https://transparenz.karlsruhe.de/",
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    })
    # https://transparenz.karlsruhe.de/dataset/daten-der-wetterstation-auf-der-heinrich-hubsch-schule
    representation = provider.create_representation(data={
        "title": "Daten der Wetterstation auf der Heinrich-Hübsch-Schule 2017",
        "description": "Daten der Wetterstation auf der Heinrich-Hübsch-Schule 2017",
        "mediaType": "text/csv"
    })
    contract = provider.create_contract(data={
    "title": "Contract for Weather Data",
    "description": "Contract for Weather Data",
    "start": "2022-09-01T05:40:27.740Z",
    "end": "2022-12-01T05:40:27.740Z"
    })
    use_rule = provider.create_rule(data={"value": """{
        "@context" : {
            "ids" : "https://w3id.org/idsa/core/",
            "idsc" : "https://w3id.org/idsa/code/"
        },
        "@type": "ids:Permission",
        "@id": "https://w3id.org/idsa/autogen/permission/cf1cb758-b96d-4486-b0a7-f3ac0e289588",
        "ids:action": [
            {
            "@id": "idsc:USE"
            }
        ],
        "ids:description": [
            {
            "@value": "Provide Access Usage Policy for Weather Data",
            "@type": "http://www.w3.org/2001/XMLSchema#string"
            }
        ],
        "ids:title": [
            {
            "@value": "Usage Policy for Weather Data",
            "@type": "http://www.w3.org/2001/XMLSchema#string"
            }
        ]
    }"""})

    artifacts = []
    for root, dirs, files in os.walk(CSV_WEATHER, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            with open(path, 'r', encoding="utf8") as f:
                text = f.read()
                artifacts.append(provider.create_artifact(data={"value": text}))


    ## Link resources
    provider.add_resource_to_catalog(catalog, offers)
    provider.add_representation_to_resource(offers, representation)
    for artifact in artifacts:
        provider.add_artifact_to_representation(representation, artifact)
    provider.add_contract_to_resource(offers, contract)
    provider.add_rule_to_contract(contract, use_rule)