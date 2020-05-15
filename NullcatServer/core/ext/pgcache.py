from .cache import LRUCached

_cache = dict()
debug = False
max_size = 50


class SimpleCached:
    @staticmethod
    def cache(func):
        async def inner(self):
            path = self.request.path
            # 随机选取幸运数据移除
            if len(_cache) >= max_size:
                if debug:
                    print(_cache.popitem()[0], "Remove")
                else:
                    _cache.popitem()
            # 缓存获取
            if path in _cache:
                if debug:
                    print("Cache", path, "hit")
                return _cache.get(path)
            else:
                result = await func(self)
                if result:
                    _cache[path] = result
                    if debug:
                        print("Request", path, "stored")
                    return result
        return inner

    @staticmethod
    def flush():
        # 刷新缓存
        _cache.clear()
        if debug:
            print("Cache flush")


class PriorityCached(LRUCached):
    def cache(self, func):
        async def inner(req):
            path = req.request.path
            if path in self.mapper:
                return self.get(path)
            else:
                result = await func(req)
                if result:
                    self.set(path, result)
                    return result
        return inner

    def flush(self):
        self.mapper.clear()
        self.priority.clear()


PGCached = PriorityCached(max_size)
