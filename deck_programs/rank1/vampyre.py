from deck_programs.deckprogram import *
import core
import random
from os.path import isfile, join
import os
from time import sleep
import argparse


class Vampyre(DeckProgram):
    def __init__(self, name='vampyre'):
        super(Vampyre, self).__init__()
        self.name = name
        self.parser = argparse.ArgumentParser(prog=self.name)
        self.parser.add_argument('-s', '--sweep', action='store_true',
                            help="Search files for vulnerabilities. "
                                 "Files able to be unlocked will display as 'vulnerable")
        self.parser.add_argument('-l', '--lock', action='store', nargs=2,
                            help="Lock a file, specifying complexity of lock. vampyre -l 5 <file>")
        self.parser.add_argument('-u', '--unlock', action='store')

    def lock_waiting(self, complexity):
        for i in range(1, complexity*10):
            print(".", end='', flush=True)
            sleep(.5)
        print(".")

    def print_vamPYre(self, clear=False):
        vampyre = """
               ____________________
     ___      /     _________
        \    / AMP\/RE
         \  /     / cyber lockpicking utility
          \/    \/
        """
        if clear:
            os.system('cls' if os.name == 'nt' else 'clear')
        for each in vampyre:
            print(each, end='', flush=True)
            sleep(.005)
        print()

    @staticmethod
    def loading_bar():
        for i in range(1,10):
            print(".", end='', flush=True)
            sleep(.1)

    def unlock(self, file, size, env):
        self.size = size
        self.solution = []
        self.possibles = []
        self.roll_solution()
        self.guessed = ["-"]*self.size
        self.print_current()
        solved = self.guessing()
        if solved:
            #data = env.read
            data = env.read_file(file)

            newdata = ""
            for line in data.split('\n'):
                if "!!" not in line:
                    print(line, end='')
                    newdata += line
            env.write_file(file, newdata)
            print()
            print(file, "UNLOCKED")

    def roll_solution(self):
        for i in range(0, self.size):
            character = self.rolling()
            while character in self.solution:
                character = self.rolling()
            self.solution.append(character)

        self.possibles = self.solution.copy()
        for i in range(0, self.size):
            character = self.rolling()
            while character in self.possibles:
                character = self.rolling()
            self.possibles.append(character)
        self.possibles.sort()

    def print_current(self):
        print(self.possibles)
        for each in self.guessed:
            print(" ___", end='')
        print()
        for each in self.guessed:
            print("|", each, end=' ')
        print("|")
        for each in self.guessed:
            print(" ```", end='')
        print()

    def guessing(self):
        guess = ''
        while list(guess) != self.solution:
            guess = input(">")[:self.size].upper()
            if '!' in guess:
                print("Leaving vampyre")
                return
            for each in guess:
                print(each, end=":")
                if each in self.solution:
                    if guess.index(each) == self.solution.index(each):
                        print("LOCKED".rjust(20))
                        self.guessed[guess.index(each)] = each
                    else:
                        print("Exists".rjust(20))
                else:
                    print("--------------------")
                    if each.upper() in self.possibles:
                        self.possibles.remove(each.upper())
            print('--------------------------------------------------------------------')
            self.print_current()
        return True

    def rolling(self):
        return chr(random.randint(65, 90))

    def complete(self, text, line, begidx, endidx):
        pass

    def run(self, args, env):
        self.print_vamPYre()
        a = self.parse_args(args)
        try:
            if a.sweep:
                print("sweeping...")
                for file in env.get_files():
                    print('\t', file.ljust(40), end='', flush=True)
                    self.loading_bar()
                    lock = env.is_locked(file)
                    if lock:
                        if lock[1] == "vampyre":
                            print("---VULNERABLE---")
                        else:
                            print("LOCKED")
                    else:
                        print("UNLOCKED")
                return
            elif a.lock:
                complexity = int(a.lock[0])
                if 14 > complexity > 1:
                    if a.lock[1] in env.get_files():
                            if env.is_locked(a.lock[1]):
                                print(a.lock[1], "is already locked.")
                                return
                            else:
                                inputString = "Locking" + str(a.lock[1]) + " with vampyre at complexity " + str(complexity) +": continue? (y/n)"
                                if input(inputString).upper() not in ["N", "NO"]:
                                    self.lock_waiting(complexity)
                                    data = env.read_file(a.lock[1])
                                    env.write_file(a.lock[1], "!!:vampyre:"+str(complexity)+"\n"+data)
            elif a.unlock:
                lock = env.is_locked(a.unlock)
                if lock:
                    if lock[1] == "vampyre":
                        num = lock[2]
                        if num:
                            self.unlock(a.unlock, int(num), env)
                    else:
                        print(a.unlock, "is not locked with vampyre.")
                else:
                    print(a.unlock, "is unlocked.")
        except:
            pass
