import os
import json

conf_path = "config.json"
base_config = {
    "server": {
        "request_timeout": 10,
        "daemon": True,
        "loop_debug": False,
        "handler": {"*": ["core.urls"]}
     },
    "http": {
        "host": "",
        "port": 80,
        "is_enable": True,
        "rewrite_only": False
    },
    "https": {
        "host": "",
        "port": 443,
        "is_enable": False,
        "support_ciphers": "ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128",
        "cert_path": "",
        "key_path": ""
    },
    "database": {
        "database_url": "sqlite:///database.db",
        "use_memcached": False,
        "memcached_url": "",
        "debug": False
    },
    "logger": {
        "level": 20,
        "formatter": "$(asctime)s [$(levelname)s]:$(message)s",
        "time_format": "$Y/$m/$d $H:$M:$S",
        "save_log": True,
        "save_path": "log/"
    },
    "template": {
        "template_path": "template/",
        "use_fs_cache": True,
        "cache_path": "__pycache__/"
    }
}


class JsonConfigParser:
    def __init__(self, config: dict):
        self.config = config

    def _dict_sync(self, source: dict, target: dict):
        for k, v in source.items():
            if isinstance(v, dict):
                self._dict_sync(v, target[k])
            else:
                target[k] = v

    def update(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError
        with open(path, "r") as raw:
            data = raw.read()
        try:
            self._dict_sync(
                json.loads(data),
                base_config
            )
        except json.decoder.JSONDecodeError as e:
            print("Error: ConfigFile is not load")
            print("reason:", e)
            exit(0)

    def get(self, segment: str, block=None):
        if segment in self.config:
            result = self.config[segment]
            if not block:
                return result
            elif block in result:
                return result[block]
            raise KeyError(f"block {block} is not exist")
        raise KeyError(f"segment {segment} is not exist")

    def sets(self, segment: str, data: dict):
        if segment not in self.config:
            raise KeyError(f"segment {segment} is not exist")
        for k, v in data.items():
            self.config[segment][k] = v

    def set(self, segment: str, block, data):
        if segment in self.config:
            self.config[segment][block] = data
        else:
            raise KeyError(f"block {block} is not exist")

    def save(self, path=conf_path):
        with open(path, "w") as f:
            f.write(
                json.dumps(self.config, indent=2)
            )


conf = JsonConfigParser(base_config)
if not os.path.exists(conf_path):
    print(f"Warning: {conf_path} not found, regenerating...")
    conf.save()
else:
    conf.update(conf_path)
