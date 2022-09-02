import hashlib
import os

CACHE_DIR = os.environ.get('CACHE_DIR') if os.environ.get('CACHE_DIR') is not None else '.intake-ids-cache'

def get_keys(consumer_url, provider_url, resource_url, representation_url):
    return hashlib.sha1(consumer_url), hashlib.sha1(provider_url), hashlib.sha1(resource_url), hashlib.sha1(representation_url)

def get_path(consumer_url, provider_url, resource_url, representation_url):
    return os.path.join(get_keys(consumer_url, provider_url, resource_url, representation_url))

def get_repr_folder(consumer_url, provider_url, resource_url, representation_url):
    path = get_path(consumer_url, provider_url, resource_url, representation_url)
    if os.path.isdir(path):
        return path
    else:
        return None