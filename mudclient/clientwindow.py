from gi.repository import Gtk, Vte, GLib
import os


class CommandWin(Gtk.Frame):
    def __init__(self, title=None):
        super(CommandWin, self).__init__()
        self.set_label(title)
        self.terminal = Vte.Terminal() # type:Vte.Terminal

        self.add(self.terminal)
        self.show_all()


class LogsWin(Gtk.Frame):
    def __init__(self, title=None):
        super(LogsWin, self).__init__()
        self.set_label(title)
        self.terminal = Vte.Terminal()  # type:Vte.Terminal
        '''self.terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["/home/fostrb/PycharmProjects/decker/telnettest.py"],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
        )'''

        self.add(self.terminal)
        self.show_all()