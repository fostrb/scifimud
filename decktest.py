import traceback
import readline
import operator as op

from python_parser import Parser, a, anyof, maybe, someof


import programs
from programs.newprog import NewProg


class InterpreterError(Exception):
    pass


class Interpreter(object):
    def __init__(self):
        self.un_ops = {
            '-': op.neg,
            '+': op.pos
        }
        self.bin_ops = {
            '*': op.mul,
            '/': op.truediv,
            '+': op.add,
            '-': op.sub
        }
        self.vars = {}

        self.programs = {
        }

        self.load_programs()

    def load_programs(self):
        for name, cls in programs.__dict__.items():
            if isinstance(cls, type):
                iprog = cls()
                if isinstance(iprog, NewProg):
                    self.programs[name] = iprog

        for name, program in self.programs.items():
            print(name)

if __name__ == '__main__':
    Interpreter()