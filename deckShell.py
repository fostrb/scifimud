import readline
import string
import sys
import deck_programs
from deck_programs.deckprogram import DeckProgram


IDENTCHARS = string.ascii_letters + string.digits + '_'

class DeckShell(object):
    identchars = IDENTCHARS
    completekey = 'tab'
    stdout = sys.stdout
    stdin = sys.stdin
    use_rawinput = 1
    lastcmd = ''

    def __init__(self, env, user='user'):
        self.cmdqueue = []
        self.programs = []
        self.program_dict = {}
        self.import_programs()
        self.env = env
        self.user = user
        self.prompt = self.user + '@' + env.location.name + '>'

    def import_programs(self):
        for name, cls in deck_programs.__dict__.items():
            if isinstance(cls, type):
                iprog = cls()
                if isinstance(iprog, DeckProgram):
                    self.programs.append(cls())
                    self.program_dict[iprog.name] = iprog

    def cmdloop(self, intro=None):
        self.preloop()
        self.old_completer = readline.get_completer()
        readline.set_completer(self.complete)
        readline.parse_and_bind(self.completekey+": complete")

        try:
            if intro is not None:
                self.stdout.write(str(intro)+"\n")
            stop = None
            while not stop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    if self.use_rawinput:
                        try:
                            line = input(self.prompt)
                        except EOFError:
                            line = 'EOF'
                    else:
                        self.stdout.write(self.prompt)
                        self.stdout.flush()
                        line = self.stdin.readline()
                        if not len(line):
                            line = 'EOF'
                        else:
                            line = line.rstrip('\r\n')
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
            self.postloop()
        finally:
            try:
                readline.set_completer(self.old_completer)
            except ImportError:
                    pass

    def default(self, line):
        self.stdout.write('*** Unknown syntax: %s\n' % line)

    def emptyline(self):
        if self.lastcmd:
            return self.onecmd(self.lastcmd)

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.

        """
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if cmd == '':
            return self.default(line)
        else:
            try:
                for prog in self.programs:
                    if prog.name == cmd or cmd in prog.aliases:
                        return prog.run(arg, self.env)
                if cmd in ['help', 'h']:
                    self.print_help()
                    return
                return self.default(line)
            except Exception as e:
                print("caught exception")
                print(e)
                return self.default(line)

    def precmd(self, line):
        """Hook method executed just before the command line is
        interpreted, but after the input prompt is generated and issued.
        """
        return line

    def postcmd(self, stop, line):
        """Hook method executed just after a command dispatch is finished."""
        return stop

    def preloop(self):
        # Do login here
        pass

    def postloop(self):
        """Hook method executed once when the cmdloop() method is about to
        return.

        """
        pass

    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.
        """
        if state == 0:
            import readline
            origline = readline.get_line_buffer()
            line = origline.lstrip()
            stripped = len(origline) - len(line)
            begidx = readline.get_begidx() - stripped
            endidx = readline.get_endidx() - stripped
            if begidx > 0:
                cmd, args, foo = self.parseline(line)
                if cmd == '':
                    complete_function = self.completedefault
                else:
                    try:
                        if cmd in self.program_dict.keys():
                            complete_function = self.program_dict[cmd].complete
                        else:
                            complete_function = self.completedefault()
                    except AttributeError:
                        complete_function = self.completedefault
            else:
                complete_function = self.completenames

            self.completion_matches = complete_function(text, line, begidx, endidx)
        try:
            return self.completion_matches[state]
        except IndexError:
            return None

    def parseline(self, line):
        """Parse the line into a command name and a string containing
        the arguments.  Returns a tuple containing (command, args, line).
        'command' and 'args' may be None if the line couldn't be parsed.
        """
        line = line.strip()
        if not line:
            return None, None, line
        elif line[0] == '?':
            line = 'help ' + line[1:]
        i, n = 0, len(line)
        while i < n and line[i] in self.identchars: i = i+1
        cmd, arg = line[:i], line[i:].strip()
        return cmd, arg, line

    def completenames(self, text, *ignored):
        rlist = []
        for a in self.get_prog_names():
            if a.startswith(text):
                rlist.append(a)
        return rlist

    def get_prog_names(self):
        rlist = []
        for prog in self.programs:
            rlist.append(prog.name)
        return rlist

    def completedefault(self, *ignored):
        """Method called to complete an input line when no command-specific
        complete_*() method is available.

        By default, it returns an empty list.

        """
        return []

    def print_help(self):
        print("Loaded Programs:")
        for prog in self.programs:
            print('\t' + prog.name)
        print()
