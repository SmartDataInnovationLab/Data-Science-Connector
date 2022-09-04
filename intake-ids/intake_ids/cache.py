import hashlib
import json
import os
from pathlib import Path
from pydantic import ValidationError
from .ids_information_model.contract import Contract
from .usage_control.contract import is_contract_valid

CACHE_DIR = os.environ.get('CACHE_DIR') if os.environ.get('CACHE_DIR') is not None else '.intake-ids-cache'
AGREEMENT = 'agreement.json'
ARTIFACT = 'artifact.dat'

def hash(string: str):
    return hashlib.sha1(string.encode(encoding = 'UTF-8', errors = 'strict')).hexdigest()

class Cache():
    def __init__(self, consumer_url, provider_url, resource_url, representation_url) -> None:
        self.con_h = hash(consumer_url)
        self.pro_h = hash(provider_url)
        self.res_h = hash(resource_url)
        self.rep_h = hash(representation_url)

        self.path: Path = Path(CACHE_DIR) / self.con_h / self.pro_h / self.res_h / self.rep_h

    def _partition(self, partition: int) -> Path:
        return self.path / str(partition)
    def _agreement(self, partition: int) -> Path:
        return self._partition(partition) / AGREEMENT
    def _artifact(self, partition: int) -> Path:
        return self._partition(partition) / ARTIFACT

    def is_cached(self, partition: int) -> bool:
        if self.path.is_dir() is False:
            return False

        if self._check_validity(partition) is False:
            self.clear(partition)
            return False

        return True

    def _check_validity(self, partition: int) -> bool:
        try:
            agreement = self._get_agreement(partition)
            if agreement is None:
                return False

            contract = Contract.parse_raw(agreement.get('value', ''))
            return is_contract_valid(contract)
        except (ValidationError, OSError) as e:
            return False

    def _get_agreement(self, partition: int) -> dict | None:
        if not self._agreement(partition).is_file():
            return None

        with open(self._agreement(partition), 'r', encoding="utf8") as f:
            return json.load(f)

    def clear(self, partition: int) -> None:
        import shutil
        if self._partition(partition).exists() and self._partition(partition).is_dir():
            shutil.rmtree(self._partition(partition))

    def setup(self, partition: int) -> None:
        self._partition(partition).mkdir(parents=True, exist_ok=True)

    def get_agreement(self, partition: int) -> dict | None:
        if (not self.is_cached(partition)):
            return None
        
        return self._get_agreement(partition)
    
    def cache_agreement(self, agreement, partition):
        self.clear(partition)
        self.setup(partition)
        with open(self._agreement(partition), 'w') as f:
            json.dump(agreement, f, ensure_ascii=False, indent=4)

    def get_artifact_filename(self, partition: int) -> str:
        if not self.is_cached(partition):
            raise LookupError('Resource is not cached or agreement for the cached resource is no longer valid')
        return str(self._artifact(partition))

    def has_artifact(self, partition: int) -> bool:
        if not self.is_cached(partition):
            return False
        return self._artifact(partition).is_file()

    def cache_artifact(self, artifact_stream, partition: int):
        with open(self._artifact(partition), 'wb') as f:
            for chunk in artifact_stream.iter_content(chunk_size=16 * 1024): 
                f.write(chunk)
