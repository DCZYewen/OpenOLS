class LRUCached:
    def __init__(self, max_size=500):
        self.max_size = max_size
        self.mapper = dict()
        self.priority = list()

    def pop(self, index=-1):
        return self.mapper.pop(
            self.priority.pop(index)
        )

    def release(self, count):
        if count > self.max_size:
            raise ValueError("remove count cannot bigger than max_length")
        for _ in range(count):
            self.pop()

    def set(self, key, value):
        if len(self.priority) >= self.max_size:
            self.pop()
        self.priority.insert(0, key)
        self.mapper[key] = value

    def get(self, key):
        if key in self.mapper:
            self.priority.remove(key)
            self.priority.insert(0, key)
            return self.mapper[key]
        return None

    def __len__(self) -> int:
        return len(self.mapper)

    def __contains__(self, item):
        return item in self.mapper

    def __repr__(self):
        return f"<LRUCached max_size={self.max_size} current_size={len(self.mapper)}>"
