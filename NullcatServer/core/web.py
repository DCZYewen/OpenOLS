import re
import base64
import asyncio
import jinja2
import struct
from time import time
from urllib.parse import unquote
from typing import Iterable
from .ext.const import *
from .helpers import timestamp_toCookie, File, ws_return_key, render, Bio
from .db import DBSession
try:
    from ujson import dumps
except ImportError:
    from json import dumps

database = DBSession()
ws_connection = {"default": []}  # WebSocket连接组储存


@asyncio.coroutine
def conn_drain(drain) -> bool:
    try:
        yield from drain()
    except ConnectionError:
        return True
    yield  # Fix "socket.send() raised exception." issue
    return False


class HTTPRequest:
    def __init__(self, origin, ip=None):
        self.body = b""
        self.remote = ip
        self.head = {}
        self.re_args = ()
        info, extra = origin.split(b"\r\n", 1)
        self.method, self.path, self.protocol = re.match(r"(\w{3,7}) (.*) HTTP/(\d\.\d)", info.decode()).groups()
        for kv in extra[:-4].decode().splitlines():
            k, v = kv.split(": ", 1)
            self.head[k.title()] = v
        self.body_length = int(self.head.get("Content-Length", "0"))

    @property
    def GET(self) -> dict:
        if self.path.find("?") == -1:
            return {}
        data = self.path.split("?", 1)[1]
        try:
            block = data.split("&")
        except IndexError:
            block = data
        result = {}
        try:
            for i in block:
                k, v = i.split("=", 1)
                result[k] = unquote(v)
            return result
        except ValueError:
            return {}

    @property
    def POST(self) -> dict:
        try:
            block = self.body.split(b"&")
        except IndexError:
            block = self.body
        result = {}
        try:
            for i in block:
                k, v = i.split(b"=", 1)
                result[k.decode()] = v
            return result
        except ValueError:
            return {}

    @property
    def Cookie(self) -> dict:
        cookie = self.head.get("Cookie")
        if not cookie:
            return {}
        buf = cookie.split("; ")
        kv = {}
        for i in buf:
            k, v = i.split("=", 1)
            kv[k] = v
        return kv

    def __repr__(self) -> str:
        return 'Request(method="{0}", path="{1}", protocol="{2}")'.format(self.method, self.path, self.protocol)


class Response(object):
    """
    警告：不要使用这个类发送过大的请求
    在慢速连接中可能会导致连接断开
    """
    def __init__(self, content=None, code=200, header=None, content_type="text/html"):
        if not header:
            header = {}
        self.code = code
        self.protocol = "HTTP/1.1"
        self.header = {"Content-Type": content_type, **header}
        if isinstance(content, str):
            self.content = content.encode()
        elif isinstance(content, (bytes, bytearray, File, Bio)):
            self.content = content
        elif not content:
            self.content = b""
        else:
            raise ValueError(f"Wrong type {type(content)}")
        self.length = len(self.content)

    def set_content(self, content: bytes):
        self.content = content
        return self

    def status(self, code: int, protocol="HTTP/1.1"):
        self.code = code
        self.protocol = protocol

    def add_header(self, header):
        self.header.update(header)

    def set_cookie(self, name, value, expire=3600, **kwargs):
        if value > 4095:
            raise RuntimeWarning()
        result = f"{name}={value}; expires={timestamp_toCookie(time() + expire)};"
        for k, v in kwargs.items():
            if k and v:
                result += f' {k.replace("_", "-")}={v};'
            elif k:
                result += f" {k};"
        self.header["Set-Cookie"] = result

    def getLen(self) -> int:
        return self.length

    def build(self) -> bytearray:
        header = bytearray()
        header += f"{self.protocol} {self.code} {code_message.get(self.code, 'OK')}\r\n".encode()
        for k, v in self.header.items():
            header += k.encode()
            header += b": "
            if isinstance(v, (bytes, bytearray)):
                header += v
            elif isinstance(v, (str, int, float)):
                header += str(v).encode()
            else:
                raise ValueError(f"Str, Bytes, int data only, but {type(v)} got")
            header += b"\r\n"
        header += b"\r\n"
        return header

    async def send(self, writer: asyncio.StreamWriter):
        data = self.build()
        writer.write(data)
        await conn_drain(writer.drain)
        if isinstance(self.content, File):
            writer.write(self.content.full_read())
        else:
            writer.write(self.content)
        await conn_drain(writer.drain)

    def __repr__(self):
        return f"<Response code={self.code} header={self.header}>"


class StreamResponse(Response):
    def setLen(self, length: int):
        self.length = length

    def getLen(self) -> int:
        if isinstance(self.content, File) and not self.length:
            return self.content.getSize()
        return self.length

    async def send(self, writer: asyncio.StreamWriter):
        data: Iterable = self.content
        writer.write(self.build())
        for i in data:
            if await conn_drain(writer.drain):
                break
            writer.write(i)


class JsonResponse(Response):
    def __init__(self, content, header=None):
        Response.__init__(self, content=dumps(content), header=header, content_type="application/json")


class FileResponse(Response):
    def __init__(self, path, header=None, content_type="application/octet-stream"):
        Response.__init__(self, header=header, content_type=content_type)
        try:
            self.content = File(os.path.join(work_directory, path))
        except FileNotFoundError:
            self.content = b"404 Not found"

    def getLen(self) -> int:
        return len(self.content)


class HtmlResponse(Response):
    def __init__(self, template_name, header=None, **kwargs):
        try:
            content = render(template_name, **kwargs)
        except jinja2.exceptions.TemplateNotFound:
            content = "<h3>404: Template Not Found</h3>"
        Response.__init__(self, content, header=header, content_type="text/html; charset=utf-8")


class BaseHandler:
    def __init__(self, request: HTTPRequest, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.request = request
        self.writer = writer
        self.reader = reader

    async def run(self):
        pass

    async def loop(self):
        pass


class WebHandler(BaseHandler):
    async def run(self) -> Response:
        if self.request.method == "GET":
            res = await self.get()
        elif self.request.method == "POST":
            res = await self.post()
        else:
            res = http405()
        if not res:
            raise ValueError("Function no result")
        return res

    async def get(self):
        return http405()

    async def post(self):
        return http405()


class BasicAuthHandler(WebHandler):
    user = b""
    password = b""
    realm = "Server"

    async def run(self) -> Response:
        if "Authorization" not in self.request.head:
            res = Response("401 Unauthorized", code=401)
            res.add_header({"WWW-Authenticate": f'Basic realm="{self.realm}"'})
        else:
            raw = self.request.head.get("Authorization", "")
            typ, content = raw.split(" ", 1)
            if typ != "Basic":
                return Response(f"Unknown auth method {typ}", code=400)
            user, password = base64.b64decode(content).split(b":", 1)
            if user != self.user or password != self.password:
                res = Response("401 Unauthorized", code=401)
                res.add_header({"WWW-Authenticate": f'Basic realm="{self.realm}"'})
            else:
                res = await WebHandler.run(self)
        return res


class APIHandler(WebHandler):
    code = 200
    header = {}

    def _get_new_data(self):
        origin = dir(BaseHandler)
        now = dir(self)
        attr_list = list(set(now) - set(origin))
        result = dict()
        for n in attr_list:
            result[n] = getattr(self, n)
        return result

    async def run(self) -> Response:
        res = await WebHandler.run(self)
        if isinstance(res, Response):
            return res
        assert isinstance(res, (dict, list, tuple, str, int, bytearray, bytes)), "Unknown type: %s" % type(res)
        if not Response:
            return Response(header=self.header, code=204)
        if isinstance(res, (dict, list, tuple)):
            return Response(content=dumps(res), header=self.header, code=self.code, content_type="text/json")
        elif isinstance(res, (str, int)):
            return Response(content=str(res), header=self.header, code=self.code, content_type="text/plain")
        elif isinstance(res, (bytes, bytearray)):
            return Response(content=res, header=self.header, code=self.code, content_type="text/plain")


class WsHandler(BaseHandler):
    keep_alive = True

    async def run(self) -> Response:
        if self.request.head.get("Upgrade") != "websocket":
            return http405()
        key = self.request.head.get("Sec-Websocket-Key", "")
        if len(key) != 24:  # 24 bytes fixed
            return http400()
        res = Response(code=101)
        res.add_header({"Connection": "Upgrade",
                        "Upgrade": "websocket",
                        "Sec-WebSocket-Accept": ws_return_key(key)})
        return res

    async def read(self, timeout=-1) -> tuple:
        try:
            if timeout == -1:
                b1, b2 = await self.reader.read(2)
            else:
                b1, b2 = await asyncio.wait_for(self.reader.read(2), timeout)
        except asyncio.TimeoutError:
            return None, None
        except (ValueError, ConnectionError):
            return None, OPCODE_CLOSE_CONN
        # fin = b1 & FIN
        opcode = b1 & OPCODE
        masked = b2 & MASKED
        payload_length = b2 & PAYLOAD_LEN
        if opcode == OPCODE_CLOSE_CONN:
            self.close_connection()
            return None, opcode
        if not masked:
            print("must masked")
            return None, OPCODE_CLOSE_CONN
        if payload_length == 126:
            payload_length = struct.unpack(">H", await self.reader.read(2))[0]
        elif payload_length == 127:
            payload_length = struct.unpack(">Q", await self.reader.read(8))[0]
        ms = await self.reader.read(4)
        message_bytes = bytearray()
        i = 0
        d = await self.reader.read(payload_length)
        while i != payload_length:
            message_bytes.append(d[i] ^ ms[i % 4])
            i += 1
        return message_bytes, opcode

    def send(self, message, opcode=OPCODE_TEXT):
        """
        Important: Fragmented(=continuation) messages are not supported since
        their usage cases are limited - when we don't know the payload length.
        """

        header = bytearray()
        if not isinstance(message, (bytes, bytearray)):
            payload = message.encode()
        else:
            payload = message
        payload_length = len(payload)

        # Normal payload
        if payload_length <= 125:
            header.append(FIN | opcode)
            header.append(payload_length)

        # Extended payload
        elif 126 <= payload_length <= 65535:
            header.append(FIN | opcode)
            header.append(PAYLOAD_LEN_EXT16)
            header.extend(struct.pack(">H", payload_length))

        # Huge extended payload
        elif payload_length < 18446744073709551616:
            header.append(FIN | opcode)
            header.append(PAYLOAD_LEN_EXT64)
            header.extend(struct.pack(">Q", payload_length))

        else:
            raise Exception("Message is too big. Consider breaking it into chunks.")

        self.writer.write(header + payload)

    def close_connection(self, message="Connection close"):
        self.send(message, opcode=OPCODE_CLOSE_CONN)
        self.keep_alive = False

    async def write(self, data):
        self.send(data)
        await self.writer.drain()

    def write_nowait(self, data):
        self.send(data)

    async def loop(self):
        try:
            await self.onInit()
            while self.keep_alive:
                data, opcode = await self.read(10)
                if opcode == OPCODE_TEXT:
                    await self.onReceive(data)
                elif opcode == OPCODE_PING:
                    await self.onPing()
                elif opcode == OPCODE_PONG:
                    pass
                elif opcode == OPCODE_CLOSE_CONN:
                    await self.onClose()
                else:
                    if not opcode:
                        self.send("", opcode=OPCODE_PING)
                        continue
                    print("Unknown opcode:", opcode)
                    self.close_connection()
        except ConnectionError as e:
            print(e)
            self.close_connection()

    async def onInit(self):
        pass

    async def onReceive(self, data):
        pass

    async def onPing(self):
        self.send("", OPCODE_PONG)

    async def onClose(self):
        self.close_connection()


class WsGroupHandler(WsHandler):
    group = "default"

    @staticmethod
    def _init_new_group(name: str):
        ws_connection[name] = []

    @staticmethod
    def group_list() -> list:
        return list(ws_connection.keys())

    @staticmethod
    def broadcast(data):
        for group in ws_connection.values():
            for send_text in group:
                send_text(data)

    def change_group(self, target_group: str):
        self.remove_conn()
        self.add_conn(target_group)
        self.group = target_group

    def add_conn(self, group=None):
        if not group:
            group = self.group
        if group not in ws_connection:
            self._init_new_group(group)
        if group not in ws_connection[group]:
            ws_connection[group].append(self.send)

    def remove_conn(self):
        if self.send in ws_connection[self.group]:
            ws_connection[self.group].remove(self.send)
            if not ws_connection[self.group] and self.group != "default":
                ws_connection.pop(self.group)

    def emit(self, data):
        if self.group not in ws_connection:
            raise AttributeError("Group %s not found" % self.group)
        for send_text in ws_connection.get(self.group):
            send_text(data)

    async def onClose(self):
        self.remove_conn()
        self.close_connection()


def http204():
    return Response(code=204)


def http404(message=PAGE_404):
    return Response(message, 404)


def http400(message=PAGE_400):
    return Response(message, 400)


def http301(url):
    res = Response(code=301)
    res.add_header({"Location": url})
    return res


def http304():
    return Response(code=304)


def http403(message=PAGE_403):
    return Response(message, 403)


def http405(message=PAGE_405):
    return Response(message, 405)


def HttpServerError(message=PAGE_500):
    return Response(message, 500)
