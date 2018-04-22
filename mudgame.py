from mudserver import MudServer
#from gameobjs import * # uncomment import later for type hinting
import time
#from galaxmap import GalaxMap
from mudinterpreter.mudinterpreter import MUDInterpreter

from mapobjs.room import GNETMap
from roomtest import GalaxMap


class MudGame(object):
    def __init__(self, name='MUD_TEST'):
        self.name = name
        self.players = []
        self.saved_players = {}
        self.mud_server = MudServer()
        self.interpreter = MUDInterpreter()
        self.map = GalaxMap()

    def handle_new_connections(self):
        for player in self.mud_server.get_new_players():
            self.players.append(player)
            self.mud_server.log('new connection: ' + player.address)
            player.message("Name:")

    def handle_disconnect(self):
        for dc_player in self.mud_server.get_disconnected_players():
            if dc_player not in self.players:
                continue
            self.saved_players[dc_player.name] = dc_player
            name = str(dc_player.name)
            for player in self.players:
                player.message(name + " disconnected")
            self.mud_server.log(name + " disconnected.")
            self.players.remove(dc_player)

    def handle_commands(self):
        for player, line in self.mud_server.get_commands():
            if player not in self.players:
                continue

            #  replace with login at some point
            if player.name is None:
                player.name = line
                player.location = 'Galaxnet Dome'

                if player.name in self.saved_players.keys():
                    savedplayer = self.saved_players[player.name]
                    player.message("Welcome back " + player.name)
                    player.location = savedplayer.location
                for p in self.players:
                    p.message(player.name + " entered.")
                self.mud_server.log(player.name + " entered ")
            else:
                # normal command parsing
                try:
                    output = self.interpreter.attempt_run(player, line, self)
                    if output:
                        player.message(output)
                except:
                    pass

    def check_players(self):
        for player in self.players:
            player.update()

    def run(self):
        while True:
            #time.sleep(0.2)
            self.mud_server.update()
            self.handle_new_connections()
            self.handle_disconnect()
            self.handle_commands()
            self.check_players()


if __name__ == '__main__':
    instance = MudGame()
    instance.run()
