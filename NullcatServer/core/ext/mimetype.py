type_dict = {
    "htm":   "text/html",
    "html":  "text/html",
    "txt":   "text/plain",
    "py":    "text/plain",
    "md":    "text/plain; charset=utf-8",
    "json":  "text/json; charset=utf-8",
    "css":   "text/css",
    "js":    "text/javascript",
    "mp3":   "audio/mpeg",
    "mid":   "audio/midi",
    "ogg":   "audio/ogg",
    "wav":   "audio/wav",
    "flac":  "audio/x-flac",
    "mp4":   "video/mp4",
    "avi":   "video/avi",
    "ts":    "video/mp2t",
    "webm":  "video/webm",
    "jpg":   "image/jpeg",
    "png":   "image/png",
    "gif":   "image/gif",
    "bmp":   "image/bmp",
    "xml":   "application/xml",
    "m3u8":  "application/x-mpegURL",
    "exe":   "application/octet-stream",
    "jar":   "application/octet-stream",
    "bin":   "application/octet-stream",
    "zip":   "application/x-zip-compressed",
    "gz":    "application/x-gzip"
}

def get_type(path, default="text/plain"):
    result = type_dict.get(path.split(".")[-1])
    if not result:
        return default
    return result
