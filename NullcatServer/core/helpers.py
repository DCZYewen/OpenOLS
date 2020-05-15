import os
import re
import time
import asyncio
from functools import partial
from hashlib import sha1
from base64 import b64encode
from typing import Optional, Tuple

from jinja2 import Environment, FileSystemLoader, FileSystemBytecodeCache
from .errors import UnknownTypeError, TooBigEntityError
from .config import conf
from .ext.const import work_directory, ws_magic_string

template_path = conf.get("template", "template_path")
cache_path = conf.get("template", "cache_path")

loader = FileSystemLoader(template_path)

if conf.get("template", "use_fs_cache"):
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)
    bc_cache = FileSystemBytecodeCache(os.path.join(work_directory, cache_path), "%s.cache")
else:
    bc_cache = None
env = Environment(loader=loader, bytecode_cache=bc_cache, enable_async=False, autoescape=True)


# "--" + self.bound + "\r\n" + http_like_data + "\r\n"
class PostDataManager:
    def __init__(self, request, reader: asyncio.StreamReader, buf_size=16384, limit=10485760):  # 10M
        if request.body_length > limit:
            raise TooBigEntityError(
                "Max size is %d, but %d got" % (limit, request.body_length)
            )
        self.reader = reader
        self.request = request
        self.buf_size = buf_size
        self.max_size = limit
        self.bound = b""

    async def _read(self):
        return await self.reader.read(min(self.buf_size, self.request.body_length))

    async def multipart(self):
        buf = bytearray()
        while True:
            if not buf:
                buf = await self._read()
                if not buf:
                    return
                self.request.body_length -= len(buf)
                continue
            cursor = buf.find(self.bound) + len(self.bound)
            if cursor >= len(self.bound):
                if buf[cursor: cursor + 2] == b"--":
                    yield buf[:buf.find(self.bound)]  # data body
                    buf = bytearray()
                elif buf[cursor: cursor + 2] == b"\r\n":
                    head, buf = buf[cursor + 2:].split(b"\r\n\r\n", 1)
                    result = {}
                    for l in head.split(b"\r\n"):
                        if not l:
                            break
                        k, v = l.decode().split(": ", 1)
                        result[k] = v
                    yield result
                else:
                    buf = buf[buf.find(self.bound):]
                    yield buf[:buf.find(self.bound)]  # data body
            else:
                yield buf
                buf = bytearray()

    async def urlencode(self):
        buf = bytearray()
        result = {}
        while True:
            if self.request.body_length:
                buf += await self._read()
            else:
                break
        for l in buf.split(b"&"):
            try:
                k, v = l.split(b"=")
            except ValueError:
                continue
            result[k] = v
        return result

    def handle(self):
        content_type = self.request.head.get("Content-Type", "").split("; ")
        if content_type[0] == "multipart/form-data":
            for seg in content_type[1:]:
                k, v = seg.split("=")
                if k == "boundary":
                    self.bound = b"--" + v.encode()
            return self.multipart()
        elif content_type[1] == "application/x-www-form-urlencoded":
            return self.urlencode()
        else:
            raise UnknownTypeError(content_type)


class Bio:
    def __init__(self, data: bytes, buf=32768):
        self.data = bytearray(data)
        self.buf = buf

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        count = 0
        while True:
            if len(self.data) > count * self.buf:
                yield self.data[count * self.buf:(count + 1) * self.buf]
            elif len(self.data) < count * self.buf:
                return self.data[count * self.buf:]
            count += 1


class File(object):
    def __init__(self, path, buf_size=65535):
        self.path = path
        self.offset = 0
        self.buf_size = buf_size
        self.chunk_size = None
        if os.path.exists(path):
            self._file = open(path, "rb")
            self.size = os.path.getsize(path)
        else:
            raise FileNotFoundError

    def read(self, size):
        return self._file.read(size)

    def full_read(self):
        return self._file.read()

    def getSize(self):
        return self.size

    def seek(self, offset):
        self._file.seek(offset)

    def mtime(self):
        return os.stat(self.path).st_mtime

    def set_range(self, offset, size):
        if offset < 0:
            raise ValueError
        elif offset + size >= self.size:
            size = self.size - offset
        self.offset = offset
        self.chunk_size = size

    def __iter__(self):
        self.seek(self.offset)
        if self.chunk_size:
            while True:
                if self.chunk_size - self.buf_size > 0:
                    yield self.read(self.buf_size)
                else:
                    yield self.read(self.chunk_size)
                    break
                self.chunk_size -= self.buf_size
        else:
            while True:
                data = self.read(self.buf_size)
                if data:
                    yield data
                else:
                    break

    async def __aiter__(self):
        loop = asyncio.get_event_loop()
        self.seek(self.offset)
        buf = bytearray(self.buf_size)
        if self.chunk_size:
            while True:
                if self.chunk_size <= 0:
                    break
                read = await loop.run_in_executor(None, self._file.readinto, buf)
                if not read:
                    break  # EOF
                yield buf
                self.chunk_size -= self.buf_size
        else:
            while True:
                read = await loop.run_in_executor(None, self._file.readinto, buf)
                if not read:
                    break  # EOF
                yield buf

    def __len__(self) -> int:
        return self.size


def cookie_toTimestamp(cookieTime) -> int:
    return int(time.mktime(time.strptime(cookieTime, "%a, %d %b %Y %H:%M:%S GMT")))


def timestamp_toCookie(Time=time.time()) -> str:
    return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(Time))


def parse_range(origin, max_value=0) -> Optional[Tuple[int, int, int]]:
    result = re.match(r"bytes=(\d*)-(\d*)", origin)
    if result:
        if result.groups()[1]:
            offset, byte = (int(i) for i in result.groups())
        else:
            offset, byte = (int(result.groups()[0]), max_value)  # 4M
        total = byte - offset + 1
        if byte > max_value:
            return offset, max_value, max_value - offset + 1
        return offset, byte, total
    else:
        return None


def render(template, **kwargs):
    template = env.get_template(template)
    return template.render(**kwargs)


def ws_return_key(key) -> bytes:
    if isinstance(key, str):
        return b64encode(sha1(key.encode() + ws_magic_string).digest())
    return b64encode(sha1(key + ws_magic_string).digest())


def make_etag(mtime, file_length):
    return f'"{int(mtime)}-{str(file_length)[-3:]}"'


def run_with_wrapper(func, *args, **kwargs):
    exe = func(*args, **kwargs)
    if asyncio.iscoroutine(exe):
        asyncio.ensure_future(exe)


def interval(delay, func, *args, **kwargs):
    run_with_wrapper(func, *args, **kwargs)
    asyncio.get_event_loop().call_later(delay, partial(interval, delay, func, *args, **kwargs))


def call_later(delay, callback, *args, **kwargs):
    return asyncio.get_event_loop().call_later(delay, partial(run_with_wrapper, callback, *args, **kwargs))
