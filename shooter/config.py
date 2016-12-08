import json

class Config:
    instance = None
    
    def __init__(self):
        # Global configuration flags. Derived from config.json
        self._data = {}
        Config.instance = self    

    def load(self, raw_json):
        # TODO: remove comments (JSON doesn't officially support comments)    
        self._data = json.loads(raw_json)

    def get(self, key):
        if not key in self._data:
            raise(Exception("There's no config key called '{0}'. Keys: {1}".format(key, self._data.items())))
        else:
            return self._data[key]

# Create first (singleton) instance
Config()