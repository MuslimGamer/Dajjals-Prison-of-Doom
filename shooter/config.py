import json
from shooter import file_watcher

# Global key/value pairs intended as global config. Reloads automatically.

__data = {}

def load(raw_json):
    # TODO: remove comments (JSON doesn't officially support comments)
    global __data
    __data = json.loads(raw_json)

def get(key):
    global __data
    if not key in __data:
        raise(Exception("There's no key called '{0}'. Keys: {1}".format(key, __data.items())))
    else:
        return __data[key]

file_watcher.watch('data/config.json', lambda raw_json: load(raw_json))
