#!/usr/bin/python3
from deckShell import DeckShell
from core import *


class NewDeck(object):
    def __init__(self, environment):
        self.env = environment
        self.shell = DeckShell(self.env)
        self.shell.cmdloop()


if __name__ == '__main__':
    loc = Location(directory="/home/fostrb/PycharmProjects/decker/FILESDIR")
    env = Environment(loc)
    d = NewDeck(env)
