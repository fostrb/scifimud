#!/usr/bin/python3
from telnetlib import Telnet, _TelnetSelector
import sys
import selectors
import os



tn = Telnet('localhost', 1234)

selector = _TelnetSelector()
selector.register(tn, selectors.EVENT_READ)
selector.register(sys.stdin, selectors.EVENT_READ)


def newrun():
    tn = Telnet('localhost', 1234)
    while True:
        try:
            text = tn.read_eager()
        except EOFError:
            print('*** Connection closed by remote host ***')
            sys.exit()
        if text:
            print(text.decode('ascii'))

        else:
            line = input(">").encode('ascii')
            strline = line.decode('ascii')
            line += b'\n'
            if not line:
                break
            if strline == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                tn.write(line)


def oldrun():
    while True:
        for key, events in selector.select():
            if key.fileobj is tn:
                try:
                    text = tn.read_eager()
                except EOFError:
                    print('*** Connection closed by remote host ***')
                    sys.exit()
                if text:
                    print(text.decode('ascii'), end='')
                    #sys.stdout.write(text.decode('ascii'))
                    #sys.stdout.flush()
            else:
                #line = sys.stdin.readline().encode('ascii')
                line = input().encode('ascii')
                line += b'\n'
                strline = line.decode('ascii').strip('\n')
                if not line:
                    break
                if strline == "clear":
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    tn.write(line)

if __name__ == '__main__':
    oldrun()