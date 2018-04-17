import threading
import time
import gi; gi.require_version('Gtk', '3.0'); gi.require_version('Vte', '2.91')
from gi.repository import Gtk, GObject, GLib, Vte
import signal
import sys

from telnetlib import Telnet

from mudclient.clientwindow import CommandWin, LogsWin


class MudClient(Gtk.Window):
    def __init__(self, title='galaxwin'):
        super(MudClient, self).__init__()
        self.connect('destroy', Gtk.main_quit)
        self.tn = Telnet("localhost", 1234)

        vbox = Gtk.VBox()
        #vbox.add(CommandWin('Commands'))
        #vbox.add(LogsWin('Logs'))

        commands_term = Vte.Terminal()
        logs_term = Vte.Terminal()
        vbox.add(logs_term)
        vbox.add(commands_term)
        command_entry = Gtk.Entry()
        command_entry.set_text("asdf")
        vbox.add(command_entry)

        self.add(vbox)

        self.show_all()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    GObject.threads_init()
    exit_status = MudClient()
    Gtk.main()
    sys.exit(0)
