import socket
import newdeckprograms
from newdeckprograms.newprog import NewProg
import random
import time


class Client(object):
    def __init__(self, socket=None, address="", buffer="", last_check=0):
        self.socket = socket
        self.address = address
        self.buffer = buffer
        self.last_check = last_check


class Player(object):
    def __init__(self, name=None, player_id=None, location=None, client=None):
        self.name = name
        self.player_id = player_id
        self.location = location
        self._client = client
        self.programs = []
        self.program_dict = {}

        self.max_health = 10

        self.is_derezzed = False
        self.derezzed_at = None
        self.derezzed_total_time = 0

        self.health = self.max_health
        self.atk = 2
        self.defense = 20

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

    def update(self):
        self.check_rezzed()

    def load_programs(self):
        for name, cls in newdeckprograms.__dict__.items():
            if isinstance(cls, type):
                iprog = cls()
                if isinstance(iprog, NewProg):
                    self.programs.append(iprog)
                    self.program_dict[iprog.name] = iprog

    def attempt_run_program(self, cmd, args, mud):
        for program in self.programs: # type: NewProg
            if cmd == program.name or cmd in program.aliases:
                program.attempt_run(self, args, mud)
                break

    def message(self, message):
        try:
            self._client.socket.sendall(bytearray(message+"\n\r", "ascii"))
        except KeyError:
            pass
        except socket.error:
            pass