from programs.newprog import *


# TODO: Fix this up. It's unreliable at best


class Shift(NewProg):
    def __init__(self):
        super(Shift, self).__init__()
        self.name = 'shift'
        self.aliases = 'caesar'
        self.alpha = 'abcdefghijklmnopqrstuvwxyz'

    def run(self, player, args, mud):
        output = ""
        text_in = args.split()
        shift = int(text_in[0])
        text_in.remove(str(shift))
        message = ' '.join(text_in)

        encoded = ""
        for i in range(len(message)):
            if message[i] in self.alpha:
                oldchar = self.alpha.index(message[i])
                newchar = self.alpha[(oldchar+shift) % len(self.alpha)]
                encoded += newchar
            else:
                encoded += message[i]
        output += encoded
        return output
