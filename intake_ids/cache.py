from .debug import *
import hashlib
import json
import os
from pathlib import Path
from pydantic import ValidationError
from appdirs import user_cache_dir
from .ids_information_model.contract import Contract
from .ids_information_model.artifact import Artifact
from .usage_control.contract import is_contract_valid_for_artifact

DEFAULT_CACHE_DIR = user_cache_dir('intake-ids', 'omeryagmurlu')
CACHE_DIR = os.environ.get('INTAKE_IDS_CACHE_DIR') if os.environ.get('INTAKE_IDS_CACHE_DIR') is not None else DEFAULT_CACHE_DIR
AGREEMENT = 'agreement.json'
ARTIFACT = 'artifact.dat'
ARTIFACT_META = 'artifact.json'

def hash(string: str):
    return hashlib.sha1(string.encode(encoding = 'UTF-8', errors = 'strict')).hexdigest()

def get_jsonfile(path: Path) -> dict | None:
    if not path.is_file():
        return None

    with open(path, 'r', encoding="utf8") as f:
        return json.load(f)

def save_jsonfile(path: Path, obj: dict):
    with open(path, 'w') as f:
            json.dump(obj, f, ensure_ascii=False, indent=4)

class Cache():
    def __init__(self,
        consumer_url:str = None, provider_url:str = None, resource_url:str = None, representation_url:str = None,
        consumer_hash:str = None, provider_hash:str = None, resource_hash:str = None, representation_hash:str = None,
        cache_dir=CACHE_DIR
    ) -> None:
        self.con_h = consumer_hash if consumer_hash is not None else hash(consumer_url)
        self.pro_h = provider_hash if provider_hash is not None else hash(provider_url)
        self.res_h = resource_hash if resource_hash is not None else hash(resource_url)
        self.rep_h = representation_hash if representation_hash is not None else hash(representation_url)

        self.path: Path = Path(cache_dir) / self.con_h / self.pro_h / self.res_h / self.rep_h

    def _partition(self, partition: int) -> Path:
        return self.path / str(partition)
    def _agreement(self, partition: int) -> Path:
        return self._partition(partition) / AGREEMENT
    def _artifact(self, partition: int) -> Path:
        return self._partition(partition) / ARTIFACT
    def _artifact_metadata(self, partition: int) -> Path:
        return self._partition(partition) / ARTIFACT_META
    def _get_agreement(self, partition: int):
        return Contract.parse_obj(get_jsonfile(self._agreement(partition)))
    def _get_artifact_metadata(self, partition: int):
        return Artifact.parse_obj(get_jsonfile(self._artifact_metadata(partition)))

    def is_cached(self) -> bool:
        return self.path.is_dir()

    def check_validity(self, partition: int) -> bool:
        try:
            contract = self._get_agreement(partition)
            artifact = self._get_artifact_metadata(partition)

            retval = is_contract_valid_for_artifact(contract, artifact)
        except (ValidationError, OSError) as e:
            # print("validation failed")
            # print(e)
            self.clear(partition)
            retval = False
        finally:
            if retval == False:
                self.clear(partition)
            return retval


    def clear(self, partition: int) -> None:
        display('Clearing')
        import shutil
        if self._partition(partition).exists() and self._partition(partition).is_dir():
            shutil.rmtree(self._partition(partition))

    def setup(self, partition: int) -> None:
        self._partition(partition).mkdir(parents=True, exist_ok=True)

    # Agreements
    def get_agreement(self, partition: int) -> tuple[Contract, Artifact] | None:
        if (not self.is_cached() or not self.check_validity(partition)):
            return None
        
        return self._get_agreement(partition), self._get_artifact_metadata(partition)
    
    def cache_agreement(self, agreement, artifact_metadata, partition):
        self.clear(partition)
        self.setup(partition)
        save_jsonfile(self._agreement(partition), agreement)
        save_jsonfile(self._artifact_metadata(partition), artifact_metadata)

    # Artifacts
    def get_artifact_filename(self, partition: int) -> str:
        if not self.is_cached() or not self.check_validity(partition):
            raise LookupError('Resource is not cached or agreement for the cached resource is no longer valid')
        return str(self._artifact(partition))

    def has_artifact(self, partition: int) -> bool:
        if not self.is_cached() or not self.check_validity(partition):
            return False
        return self._artifact(partition).is_file()

    def cache_artifact(self, artifact_stream, partition: int):
        with open(self._artifact(partition), 'wb') as f:
            for chunk in artifact_stream.iter_content(chunk_size=16 * 1024): 
                f.write(chunk)
