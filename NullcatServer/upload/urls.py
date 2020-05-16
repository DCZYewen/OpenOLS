# -*- coding: utf-8 -*-
# generate by new_app on 2020/05/12 09:38

from core.route import path
from . import handle

pattern = [
    path(r"^/testget$", handle.BB),
    path(r"^/ajax/getInfo$", handle.FileList)
]
