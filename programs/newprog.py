import argparse

# TODO: probably just get rid of argparse deps. Maybe look at click. Or just beef up the MUDInterpreter.


class WrapperCmdLineArgParser:
    def __init__(self, parser):
        self.parser = parser
        self.help_msg = ""

    def __call__(self, f):
        if not self.parser:  # If no parser was passed to the decorator, get it from 'f'
            self.parser = f(None, None, None, True)

        def wrapped_f(args):
            line = args.split()
            try:
                parsed = self.parser.parse_args(line)
            except SystemExit:
                return
            return parsed
        return wrapped_f


class NewProg(object):
    def __init__(self):
        self.name = ''
        self.parser = argparse.ArgumentParser()
        self.aliases = []
        self.run_while_derezzed = True

    def parse_args(self, args):
        @WrapperCmdLineArgParser(parser=self.parser)
        def parse_args(parsed):
            return parsed
        parsed = parse_args(args)
        return parsed

    def attempt_run(self, player, args, mud):
        if player.is_derezzed and not self.run_while_derezzed:
            player.message("you can't run " + self.name + " while derezzed")
        else:
            return self.run(player, args, mud)

    def run(self, player, args, mud):
        pass

    @staticmethod
    def complete(*args):
        return []