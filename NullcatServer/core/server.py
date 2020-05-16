import sys
import time
import socket
import asyncio
from .logger import main_logger
from .web import HTTPRequest, http404, HttpServerError
from .config import conf
from .route import url_match
from .rewrite import Redirect_Handler

try:
    import uvloop
except ImportError:
    uvloop = None


def get_local_ip(default=""):
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        return default


def get_best_loop(debug=False):
    if sys.platform == 'win32':
        loop = asyncio.ProactorEventLoop()  # Windows IOCP loop
    elif sys.platform == 'linux':
        if uvloop:
            loop = uvloop.new_event_loop()  # Linux uvloop (thirty part loop)
        else:
            loop = asyncio.new_event_loop()  # Linux asyncio default loop
    else:
        loop = asyncio.new_event_loop()  # Default loop
    if debug:
        loop.set_debug(debug)
        print(loop)
    return loop


def get_ssl_context(alpn: list, cert_path, key_path):
    import ssl
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1)
    support_ciphers = conf.get("https", "support_ciphers")
    context.set_ciphers(support_ciphers)
    context.set_alpn_protocols([*alpn])
    context.load_cert_chain(cert_path, key_path)
    return context


class FullAsyncServer(object):
    log = main_logger.get_logger()

    def __init__(self, handler, block=True, loop=None):
        if not loop:
            loop = get_best_loop(conf.get("server", "loop_debug"))
        self.block = block
        self.handler = handler
        self.timeout = conf.get("server", "request_timeout")
        if conf.get("https", "is_enable"):
            self.ssl = get_ssl_context(["http/1.1"],
                                       conf.get("https", "cert_path"),
                                       conf.get("https", "key_path"))
        else:
            self.ssl = None
        self.loop = loop

    def millis(self):
        return int(time.time() * 1000)

    async def http1_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, data: tuple) -> bool:
        ip, header = data
        if header:
            start_time = self.millis()
            try:
                req = HTTPRequest(header, ip)
            except (ValueError, AttributeError):
                self.log.warning("Request Unpack Error(from %s)" % ip)
                self.log.warning(("Origin data: ", header))
                return False
            pattern = self.handler.get(req.head.get("Host", "*"), self.handler.get("*", []))
            if isinstance(pattern, str):
                req.head["X-Local"] = pattern
                sender = await Redirect_Handler(req, reader, writer).run()
                sender.add_header({"Connection": "close"})
                await sender.send(writer)
                self.log.info(f"{req.method} {req.head.get('Host')}:{req.path} Redirect")
                return False
            match = url_match(req.path, pattern)
            obj = None
            if match:
                req.re_args = match[1].groups()
                try:
                    obj = match[0](req, reader, writer)
                    res = await obj.run()
                except Exception:
                    self.log.exception("Handler Error:")
                    res = HttpServerError()
            else:
                res = http404()
            if res.code != 101:
                res.add_header({"Content-Length": res.getLen(),
                                "Connection": req.head.get("Connection", "close").lower(),
                                "Server": "Apache/2.2.23 (Unix)",
                                "X-Powered-By": "PHP/5.3.12"})
            await res.send(writer)
            if obj:
                await obj.loop()
                req.head["Connection"] = "close"
            self.log.info(f"{req.method} {req.path}:{res.code} {req.head.get('Host')} {ip}"
                          f"({self.millis()-start_time}ms)")
            if req.head.get("Connection", "close") == "close":
                return False
            return True

    async def server(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        ip, port = writer.get_extra_info("peername")[0:2]
        while True:
            try:
                header = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), self.timeout)
            except (ConnectionError, asyncio.TimeoutError, asyncio.IncompleteReadError):
                break
            except OSError as e:
                print(e)
                break
            if not await self.http1_handler(reader, writer, (ip, header)):
                break
        writer.close()
        self.log.debug(f"[{ip}:{port}]: connect lost")

    def signal_handler(self, sig):
        self.log.warning(f"Got signal {sig}, stopping...")
        self.loop.stop()
        
    def run(self):
        if sys.platform != "win32":
            from signal import SIGTERM, SIGINT
            for sig in (SIGTERM, SIGINT):
                self.loop.add_signal_handler(sig, self.signal_handler, sig)
        if conf.get("http", "is_enable"):
            if conf.get("http", "rewrite_only") and self.ssl:
                from .rewrite import server
            else:
                server = self.server
            http = asyncio.start_server(server,
                                        conf.get("http", "host"),
                                        conf.get("http", "port"))
            self.loop.run_until_complete(http)
            self.log.info(f"HTTP is running at {conf.get('http', 'host')}:{conf.get('http', 'port')}")
        if self.ssl:
            https = asyncio.start_server(self.server,
                                         conf.get("https", "host"),
                                         conf.get("https", "port"),
                                         ssl=self.ssl)
            self.loop.run_until_complete(https)
            self.log.info(f"HTTPS is running at {conf.get('https', 'host')}:{conf.get('https', 'port')}")
        if self.block:
            self.log.info("Press Ctrl+C to stop server")
            try:
                self.loop.run_forever()
            except KeyboardInterrupt:
                self.loop.stop()
            self.log.warning("Server closed")
