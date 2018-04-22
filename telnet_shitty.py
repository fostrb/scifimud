import readline
from telnetlib import Telnet, _TelnetSelector
import sys
import selectors
import os
import string
#import atexit
import threading

#tn = Telnet('localhost', 1234)

#selector = _TelnetSelector()
#selector.register(tn, selectors.EVENT_READ)
#selector.register(sys.stdin, selectors.EVENT_READ)


class TelnetReader(threading.Thread):
    def __init__(self, tn):
        super(TelnetReader, self).__init__()
        self.tn = tn
        self.selector = _TelnetSelector()
        self.selector.register(self.tn, selectors.EVENT_READ)
        #self.selector.register(sys.stdin, selectors.EVENT_READ)
        #threading.Thread.__init__(self)

    def run(self):
        while True:
            for key, events in self.selector.select():
                if key.fileobj is self.tn:
                    try:
                        text = self.tn.read_eager()
                    except EOFError:
                        print('*** Connection closed by remote host ***')
                        return
                        #sys.exit()
                    if text:
                        print(text.decode('utf8'), end='')


class TelnetClient(object):
    IDENTCHARS = string.ascii_letters + string.digits + '_'
    stdout = sys.stdout
    stdin = sys.stdin
    use_rawinput = 1

    def __init__(self):
        self.tn = Telnet('localhost', 1234)
        self.reader = TelnetReader(self.tn).start()

    def run(self):
        while True:
            try:
                line = input()
                line = line.encode('utf8')
                line += b'\n'
            except EOFError:
                line = 'EOF'.encode('utf8')
            strline = line.decode('utf8').strip('\n')
            if not line:
                break
            if strline == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
            elif strline == "quit":
                sys.exit()
            else:
                self.tn.write(line)


if __name__ == '__main__':
    a = TelnetClient()
    a.run()
