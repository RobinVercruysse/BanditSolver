import getpass
import os
import socket
import sys
import traceback
from paramiko.py3compat import input

import paramiko
import socket
import sys
from paramiko.py3compat import u
import termios
import tty
import select

host = 'bandit.labs.overthewire.org'
port = 2220
username = 'bandit0'
password = 'bandit0'

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.WarningPolicy())

client.connect(host, port, username, password)

chan = client.invoke_shell()

oldtty = termios.tcgetattr(sys.stdin)
try:
    tty.setraw(sys.stdin.fileno())
    tty.setcbreak(sys.stdin.fileno())
    chan.settimeout(0.0)

    while True:
        recbuffer = ''
        r, w, e = select.select([chan, sys.stdin], [], [])
        if chan in r:
            try:
                x = u(chan.recv(1024))
                if len(x) == 0:
                    break
                for character in x:
                    recbuffer += character
                    if '~$ ' in recbuffer:
                        sys.stdout.write(recbuffer)
                        sys.stdout.flush()
                    if '\n' == character:
                        recbuffer = ''
            except socket.timeout:
                pass
        if sys.stdin in r:
            x = sys.stdin.read(1)
            if len(x) == 0:
                break
            chan.send(x)
finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

chan.close()
client.close()
