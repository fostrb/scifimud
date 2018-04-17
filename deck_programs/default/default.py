from deck_programs.deckprogram import *
import os

__all__ = ['LS', 'Clear', 'PWD', 'Cat', 'Move', 'Inspect']


class LS(DeckProgram):
    def __init__(self, name='ls'):
        super(LS, self).__init__()
        self.name = name

    def run(self, args, env):
        for file in env.get_files():
            print(file)


class PWD(DeckProgram):
    def __init__(self):
        super(PWD, self).__init__()
        self.name = 'pwd'

    def run(self, args, env):
        print(env.location)


class Clear(DeckProgram):
    def __init__(self, name='clear'):
        super(Clear, self).__init__()
        self.name = name

    def run(self, *args):
        os.system('cls' if os.name == 'nt' else 'clear')


class Cat(DeckProgram):
    def __init__(self):
        super(Cat, self).__init__()
        self.name = 'cat'
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('file')

    def run(self, args, env):
        parsed = self.parse_args(args)
        if parsed.file:
            data = env.read_file(parsed.file)
            print(data)


class Move(DeckProgram):
    def __init__(self):
        super(Move, self).__init__()
        self.name = 'cd'
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('target')

    def run(self, args, env):
        parsed = self.parse_args(args)
        if parsed.target:
            env.attempt_move(parsed.target)


class Inspect(DeckProgram):
    def __init__(self):
        super(Inspect, self).__init__()
        self.name = 'inspect'
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('target', action='store')

    def run(self, args, env):
        inspection_target = env.location
        if len(args) == 0:
            inspection_target.inspect()
        else:
            parsed = self.parse_args(args)
            if parsed.target:
                pass
