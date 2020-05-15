#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import time
import re

header = """# -*- coding: utf-8 -*-
# generate by new_app on %s
""" % time.strftime("%Y/%m/%d %H:%M")

urls_template = header+"""
from core.route import path
from . import handle

pattern = [
    
]
"""

handle_template = header+""""""

file_list = {
    "__init__.py": "",
    "urls.py": urls_template,
    "handle.py": handle_template
}

def generate_struct(path):
    os.mkdir(path)
    for name, content in file_list.items():
        with open(path+"/"+name, "w") as uf:
            uf.write(content)
            print(name, "create")


if __name__ == '__main__':
    name = ""
    for offset, arg in enumerate(sys.argv):
        if arg == "new_app.py":
            name = sys.argv[offset+1]
    if name:
        if re.search(r"[/\\><|]", name):  # 过滤
            print("名称中不能含有 / \ | < > 等字符")
            exit(0)
        if os.path.isdir(name):
            print("name '%s' was exist" % name)
            exit(0)
        print("app name:", name)
        generate_struct(name)
    else:
        print("Usage: new_app.py [name]")
    print("Done")
