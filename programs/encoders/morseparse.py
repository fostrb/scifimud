from programs.mprog import *

# TODO: get this to read whitespace and unmappable chars


class MorseParse(MProg):
    def __init__(self):
        super(MorseParse, self).__init__()
        self.name = 'morse'

        self.morse = {
            'A': '.-',      'B': '-...',    'C': '-.-.',
            'D': '-..',     'E': '.',       'F': '..-.',
            'G': '--.',     'H': '....',    'I': '..',
            'J': '.---',    'K': '-.-',     'L': '.-..',
            'M': '--',      'N': '-.',      'O': '---',
            'P': '.--.',    'Q': '--.-',    'R': '.-.',
            'S': '...',     'T': '-',       'U': '..-',
            'V': '...-',    'W': '.--',     'X': '-..-',
            'Y': '-.--',    'Z': '--..',

            '0': '-----',   '1': '.----',   '2': '..---',
            '3': '...--',   '4': '....-',   '5': '.....',
            '6': '-....',   '7': '--...',   '8': '---..',
            '9': '----.',

            '.': '.-.-.-',  ',': '--..--',  ':': '---...',
            '?': '..--..',  '\'': '.----.', '-': '-....-',
            '/': '-..-.',   '@': '.--.-.',  '=': '-...-'
        }

    def encode(self, text):
        encoded = ""
        t = "".join(text)
        for c in t:
            if c.upper() in self.morse.keys():
                encoded += (self.morse[c.upper()]) + " "
            else:
                encoded += c
        return encoded

    def decode(self, text):
        decoded = ""
        for symbol in text:
            for key, val in self.morse.items():
                if symbol == val:
                    decoded += key
        return decoded

    def auto_detect_and_operate(self, args):
        alpha = 0
        morse = 0
        for character in args:
            if character == '.' or character == '-':
                morse += 1
            else:
                if character.upper() in self.morse.keys():
                    alpha += 1

        if morse > alpha:
            arguments = "".join(args).split()
            morselist = []
            converted = ""
            for arg in arguments:
                for key, symbol in self.morse.items():
                    if arg == symbol:
                        morselist.append(arg)
                        converted += key
            return converted

        else:
            converted = ""
            for character in args:
                if character.upper() in self.morse.keys():
                    converted += self.morse[character.upper()] + " "
                else:
                    converted += character
            return converted

    def run(self, player, args, mud):
        output = ''
        output += self.auto_detect_and_operate(args)
        return output
