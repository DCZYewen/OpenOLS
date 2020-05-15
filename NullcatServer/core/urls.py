from core import handle
from .route import path

pattern = [
    path("^/(.+?)$", handle.StaticHandler)
]
