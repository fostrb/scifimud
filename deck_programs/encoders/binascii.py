from deck_programs.deckprogram import *
import argparse
import binascii


class BinAscii(DeckProgram):
    def __init__(self):
        super(BinAscii, self).__init__()
        self.name = 'binascii'
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-d', '--decode', action='store')
        self.parser.add_argument('-e', '--encode', nargs='+', action='store')

    @staticmethod
    def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))

    def text_from_bits(self, bits, encoding='utf-8', errors='surrogatepass'):
        n = int(bits, 2)
        return self.int2bytes(n).decode(encoding, errors)

    @staticmethod
    def int2bytes(i):
        hex_string = '%x' % i
        n = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

    def run(self, args, env):
        a = self.parse_args(args)
        try:
            if a.encode:
                e = " ".join(a.encode)
                print(self.text_to_bits(e))
            elif a.decode:
                d = self.text_from_bits(a.decode)
                print(d)
        except:
            pass