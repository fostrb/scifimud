import argparse


class WrapperCmdLineArgParser:
    def __init__(self, parser):
        """Init decorator with an argparse parser to be used in parsing cmd-line options"""
        self.parser = parser
        self.help_msg = ""

    def __call__(self, f):
        """Decorate 'f' to parse 'line' and pass options to decorated function"""
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


class DeckProgram(object):
    def __init__(self):
        self.name = ''
        self.aliases = []
        self.parser = argparse.ArgumentParser()

    def parse_args(self, args):
        @WrapperCmdLineArgParser(parser=self.parser)
        def parse_args(parsed):
            return parsed
        parsed = parse_args(args)
        return parsed

    def run(self, args, env):
        pass

    @staticmethod
    def complete(*args):
        return []
