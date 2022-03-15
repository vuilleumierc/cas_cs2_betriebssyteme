#!/usr/bin/python3

import subprocess

try:
    proc = subprocess.Popen(["/usr/bin/tail", "-f", "/var/log/kern.log"])
    errcode = proc.wait()
except KeyboardInterrupt:
    proc.terminate()