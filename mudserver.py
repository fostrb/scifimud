import socket
import select
import time
import datetime
from gameobjs import ClientPlayer


class MudServer(object):
    _EVENT_NEW_PLAYER = 0
    _EVENT_PLAYER_LEFT = 1
    _EVENT_COMMAND = 2

    _READ_STATE_NORMAL = 0
    _READ_STATE_COMMAND = 1
    _READ_STATE_SUBNEG = 2

    _TN_INTERPRET_AS_COMMAND = 255
    _TN_ARE_YOU_THERE = 246
    _TN_WILL = 251
    _TN_WONT = 252
    _TN_DO = 253
    _TN_DONT = 254
    _TN_SUBNEGOTIATION_START = 250
    _TN_SUBNEGOTIATION_END = 240

    def __init__(self):
        self._players = []
        self._events = []
        self._new_events = []

        self._listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._listen_socket.bind(("0.0.0.0", 1234))
        self._listen_socket.setblocking(False)
        self._listen_socket.listen(1)

    def update(self):
        self._check_for_new_connections()
        self._check_for_disconnected()
        self._check_for_messages()

        self._events = self._new_events
        self._new_events = []

    def log(self, msg):
        # will replace with actual log functionality at some point
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print('[' + st + ']:' + msg)

    def get_new_players(self):
        new_players = []
        for ev in self._events:
            if ev[0] == self._EVENT_NEW_PLAYER:
                new_players.append(ev[1])
        return new_players

    def get_commands(self):
        commands = []
        for event in self._events:
            if event[0] == self._EVENT_COMMAND:
                commands.append((event[1], event[2]))
        return commands

    def get_disconnected_players(self):
        rage_quits = []
        for event in self._events:
            if event[0] == self._EVENT_PLAYER_LEFT:
                rage_quits.append(event[1])
        return rage_quits

    def _check_for_new_connections(self):
        rlist, wlist, xlist = select.select([self._listen_socket], [], [], 0)
        if self._listen_socket not in rlist:
            return

        joined_socket, addr = self._listen_socket.accept()
        joined_socket.setblocking(False)
        newplayer= ClientPlayer(joined_socket, addr[0], "", time.time())
        self._players.append(newplayer)
        self._new_events.append((self._EVENT_NEW_PLAYER, newplayer))

    def _check_for_disconnected(self):
        for player in self._players:
            if time.time() - player.last_check < 1.0:
                continue

            if not player.msg_literal("\x00"):
                self._handle_disconnect(player)

    def _check_for_messages(self):
        for player in self._players:
            rlist, wlist, xlist = select.select([player.socket], [], [], 0)
            if player.socket not in rlist:
                continue
            try:
                data = player.socket.recv(4096).decode("ascii")
                message = self._parse_client_data(player, data)
                self._new_events.append((self._EVENT_COMMAND, player, message.lower()))
            except socket.error:
                self._handle_disconnect(player)
            except Exception:
                self._handle_disconnect(player)

    def _parse_client_data(self, player, data):
        message = None
        state = self._READ_STATE_NORMAL

        for c in data:
            if state == self._READ_STATE_NORMAL:
                if ord(c) == self._TN_INTERPRET_AS_COMMAND:
                    state = self._READ_STATE_COMMAND

                elif c == "\n":
                    message = player.buffer
                    player.buffer = ""

                elif c == "\x08":
                    player.buffer = player.buffer[:-1]

                else:
                    player.buffer += c

            elif state == self._READ_STATE_COMMAND:
                if ord(c) == self._TN_SUBNEGOTIATION_START:
                    state = self._READ_STATE_SUBNEG

                elif ord(c) in (self._TN_WILL, self._TN_WONT, self._TN_DO,
                                self._TN_DONT):
                    state = self._READ_STATE_COMMAND

                else:
                    state = self._READ_STATE_NORMAL

            elif state == self._READ_STATE_SUBNEG:
                if ord(c) == self._TN_SUBNEGOTIATION_END:
                    state = self._READ_STATE_NORMAL
        return message

    def _handle_disconnect(self, player):
        self._new_events.append((self._EVENT_PLAYER_LEFT, player))
        self._players.remove(player)
