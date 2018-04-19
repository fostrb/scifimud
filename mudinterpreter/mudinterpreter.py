import programs
from programs.newprog import *
import string

IDENTCHARS = string.ascii_letters + string.digits + '_'


class MUDInterpreter(object):
    def __init__(self):
        self.identchars = IDENTCHARS
        self.programs = []
        self.load_programs()
        self.program_names = self.get_program_names()

    def load_programs(self):
        for name, cls in programs.__dict__.items():
            if isinstance(cls, type):
                iprog = cls()
                if isinstance(iprog, NewProg):
                    self.programs.append(iprog)

    def pipe(self, player, args, mud):

        buffer = None
        for arg in args:
            s = arg
            if buffer:
                s += ' ' + buffer
            buffer = self.run_cmd(player, s, mud)
        return buffer

    def attempt_run(self, player, line, mud):
        output = self.run_cmd(player, line, mud)
        return output

    def run_cmd(self, player, line, mud):
        cmd, args, line = self.pre_parseline(line)
        if not line:
            return self.emptyline(player, mud)

        player._lastcmd = line
        if line == 'EOF':
            player._lastcmd = ''
        elif cmd == '':
            return self.default(line)
        elif cmd == 'pipe':
            out = self.pipe(player, args, mud)
            return out
        else:
            try:
                for program in self.programs: # type: NewProg
                    if cmd == program.name or cmd in program.aliases:
                        return program.attempt_run(player, args, mud)
            except Exception as e:
                print(e)

    def default(self, line):
        return str('*** Unknown syntax: ' + line)

    def emptyline(self, player, mud):
        if player._lastcmd:
            return self.run_cmd(player, player._lastcmd, mud)

    def pre_parseline(self, line):
        if '|' in line:
            return 'pipe', line.split('|'), line
        return self.parseline(line)

    def parseline(self, line):
        line = line.strip()
        if not line:
            return None, None, line
        elif line[0] == '?':
            line = 'help ' + line[1:]
        i, n = 0, len(line)
        while i < n and line[i] in self.identchars: i = i+1
        cmd, arg = line[:i], line[i:].strip()
        return cmd, arg, line

    def get_program_names(self):
        rlist = []
        for prog in self.programs:
            rlist.append(prog.name)
            for alias in prog.aliases:
                rlist.append(alias)
        return rlist