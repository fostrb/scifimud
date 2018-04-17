from deck_programs.deckprogram import *
import random


class Duel(DeckProgram):
    def __init__(self):
        super(Duel, self).__init__()
        self.name = 'duel'

        self.words = [
            'word',
            'other',
            'something',
            'asdf'
        ]

    def run(self, args, env):
        cmd = ''
        score = 0
        while True:
            curcmd = random.choice(self.words)
            print(score, curcmd)
            cmd = input(':')
            if cmd == curcmd:
                score += 1
            if score == 3:
                print("demo_end")
                return
