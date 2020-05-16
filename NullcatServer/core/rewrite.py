import asyncio
from .config import conf
from .logger import main_logger
from .web import HTTPRequest, http301, WebHandler

log = main_logger.get_logger()
target_port = conf.get("https", "port")

class Redirect_Handler(WebHandler):
    async def get(self):
        if self.request.head.get("X-Local"):
            return http301(self.request.head.get("X-Local"))
        host = self.request.head.get("Host")
        if not host:
            log.warning(f"GET {self.request.path}: Host not found(from {self.request.remote})")
            host = "127.0.0.1"
        return http301(f"https://{host.split(':')[0]}:{target_port}{self.request.path}")

    async def post(self):
        return await self.get()


async def rewrite_handler(reader, writer, data):
    ip, header = data
    if header:
        try:
            req = HTTPRequest(header, ip)
        except (ValueError, AttributeError):
            log.warning("Request Unpack Error(from %s)" % ip)
            log.warning(("Origin data: ", header))
            return
        if req.path[0] != "/":  # Filter proxy scanner
            return
        sender = await Redirect_Handler(req, reader, writer).run()
        sender.add_header({"Connection": "close"})
        await sender.send(writer)


async def server(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    ip, port = writer.get_extra_info("peername")[0:2]
    try:
        header = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), conf.get("server", "request_timeout"))
        await rewrite_handler(reader, writer, (ip, header))
    except (ConnectionError, asyncio.TimeoutError, asyncio.IncompleteReadError):
        pass
    except OSError as e:
        print(e)
        pass
    writer.close()
