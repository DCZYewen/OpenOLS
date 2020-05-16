# Create on 2019/12/19
import os
import sys

def redirect_io(in_io, out_io):
    sys.stdout = out_io
    sys.stderr = out_io
    sys.stdin = in_io

def daemon(pidfile_path=None):
    if hasattr(os, "fork"):
        if os.fork():
            sys.exit(0)
        else:
            os.umask(0)
            os.setsid()
            redirect_io(open(os.devnull, "r"), open(os.devnull, "w"))
            if pidfile_path:
                import atexit
                with open(pidfile_path, "w") as f:
                    f.write(str(os.getpid()))
                atexit.register(os.remove, pidfile_path)
