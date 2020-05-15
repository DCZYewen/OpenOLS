import re
import importlib
from .config import conf


def path(p_url: str, target: object) -> tuple:
    com = re.compile(p_url)
    return com, target


def get_handler() -> dict:
    result = {}
    for k, v in conf.get("server", "handler").items():
        if isinstance(v, str):
            urls = v
        else:
            urls = []
            for module_path in v:
                urls.extend(
                    importlib.import_module(module_path).pattern
                )
        result[k] = urls
    return result


def url_match(url: str, kv: list) -> (list, None):
    if not kv:
        return None
    realurl = url.split("?")[0]
    for i in kv:
        result = i[0].search(realurl)
        if result:
            return [i[1], result]
    return None
