from intake_ids.debug import * 
import argparse
import sys
import os
from intake_ids.cache import DEFAULT_CACHE_DIR, CACHE_DIR, Cache

count = 0

def handle_cache(cache: Cache):
    global count

    display(cache.path)
    for partition in level_name(cache.path):
        if not cache.check_validity(int(partition)):
            count = count + 1

def level_name(current: str):
    with os.scandir(current) as level:
        for entry in level:
            if entry.is_dir():
                yield entry.name

def periodic_cleanup(cachedir: str):
    for consumer_hash in level_name(cachedir):
        p1 = os.path.join(cachedir, consumer_hash)
        for provider_hash in level_name(p1):
            p2 = os.path.join(p1, provider_hash)
            for resource_hash in level_name(p2):
                p3 = os.path.join(p2, resource_hash)
                for representation_hash in level_name(p3):
                    cache = Cache(consumer_hash=consumer_hash, provider_hash=provider_hash, resource_hash=resource_hash, representation_hash=representation_hash, cache_dir=cachedir)
                    handle_cache(cache)
    
    print("Cleared %d agreements/artifacts from the cache" % count)

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cachedir', help="Cache location to manage. Default value is the environment variable \"INTAKE_IDS_CACHE_DIR\" or if it does not exist, " + DEFAULT_CACHE_DIR, default=CACHE_DIR)
    args = parser.parse_args()
    return periodic_cleanup(args.cachedir)

if __name__ == "__main__":
    sys.exit(main())