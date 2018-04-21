import socket
import programs
from programs.mprog import MProg
import random
import time


# TODO: add 'inspect' properties to every game object. (Including the map. Also fix the map.)


class ClientPlayer(object):
    def __init__(self, sock=None, address="", buffer="", last_check=0):
        self.socket = sock
        self.address = address
        self.buffer = buffer
        self.last_check = last_check

        self.name = None
        self.location = None
        self.programs = []

        # this shit's just for testing purposes
        self.max_health = 10
        self.health = self.max_health
        self.defense = 10
        self.atk = 2
        # -------------------------------------

        self.is_derezzed = False
        self.derezzed_at = None
        self.derezzed_total_time = 0

        self._lastcmd = ''

    def msg_literal(self, msg):
        try:
            self.socket.sendall(bytearray(msg, "ascii"))
            return True
        except socket.error:
            return False

    def message(self, message):
        try:
            self.socket.sendall(bytearray(message+'\n\r', "ascii"))
            return True
        except socket.error:
            return False

    def derezz(self, derezzed_time=60, drmessage=None):
        self.is_derezzed = True
        self.derezzed_total_time = derezzed_time
        self.derezzed_at = time.time()
        if drmessage:
            self.message("DEREZZED MESSAGE:")
            self.message(drmessage)
        self.message(str(self.derezzed_total_time))

    def rezz(self, rezmessage=None):
        self.health = self.max_health
        self.is_derezzed = False
        self.derezzed_total_time = 0
        self.derezzed_at = 0
        if rezmessage:
            self.message("Rezzed Message:")
            self.message(rezmessage)
        else:
            self.message("You are rezzed naturally")

    def check_rezzed(self):
        if self.health <= 0 and not self.is_derezzed:
            self.derezz()
        elif self.is_derezzed:
            self.derezzed_remaining = self.derezzed_total_time - (time.time() - self.derezzed_at)
            if self.derezzed_remaining <= 0:
                self.rezz()

    # This would be a program in the future
    # Also it'd be not this. This is dumb as hell.
    def attack_target(self, target_player):
        roll = random.randint(1, 100)
        self.message("Rolled " + str(roll) + "+" + str(self.atk) + "=" + str(roll + self.atk))
        if roll + self.atk > target_player.defense:
            self.message("HIT")
            target_player.health -= self.atk
            return True
        else:
            self.message("MISS")
            return False

    def update(self):
        self.check_rezzed()


class Client(object):
    def __init__(self, socket=None, address="", buffer="", last_check=0):
        self.socket = socket
        self.address = address
        self.buffer = buffer
        self.last_check = last_check

    def msg(self, msg):
        try:
            self.socket.sendall(bytearray(msg+"\n\r", "ascii"))
        except socket.error:
            return False