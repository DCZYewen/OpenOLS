import os
from .ext.mimetype import get_type
from .web import http404, StreamResponse, http304, http400, WebHandler
from .helpers import File, timestamp_toCookie, parse_range, make_etag
from .ext.const import work_directory


static_path = os.path.join(work_directory, "static/")


class StaticHandler(WebHandler):
    async def get(self):
        request = self.request
        if request.re_args[0].find("..") != -1:
            return http400()
        path = os.path.join(static_path, request.re_args[0])
        if os.path.exists(path):
            f = File(path)
            mtime = timestamp_toCookie(f.mtime())
            if request.head.get("If-Modified-Since") == mtime:
                return http304()
            else:
                res = StreamResponse(f, content_type=get_type(path))
                content_range = request.head.get("Range")
                if content_range:  # Todo Add: Etag verity
                    offset, byte, total = parse_range(content_range, f.size-1)
                    f.set_range(offset, total)
                    res.add_header({"Content-Range": f"bytes {offset}-{byte}/{f.size}"})
                    if_unmodified_since = request.head.get("If-Unmodified-Since")
                    if if_unmodified_since == mtime:
                        res.code = 200
                    else:
                        res.code = 206
                    res.setLen(total)
                else:
                    res.add_header({"Accept-Ranges": "bytes",
                                    "Cache-Control": "cache-control: max-age=300, immutable",
                                    "Last-Modified": mtime,
                                    "Etag": make_etag(f.mtime(), f.size)})
            return res
        return http404()
