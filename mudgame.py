from MUDServer import MudServer
from gameobjs import *
import time
from galaxmap import GalaxMap


class MudGame(object):
    def __init__(self, name='MUD_TEST'):
        self.name = name
        self.saved_players = {}
        self.players = {}
        self.mud_server = MudServer()
        self.map = GalaxMap()

    def handle_new_connections(self):
        for player_id in self.mud_server.get_new_players():
            client = self.mud_server._clients[player_id]
            self.players[player_id] = Player(client=client)
            self.mud_server.log('new connection: ' + client.address)
            self.mud_server.send_message(player_id, "Name:")

    def handle_disconnect(self):
        for dc_id in self.mud_server.get_disconnected_players():

            if dc_id not in self.players.keys():
                continue

            dc_player = self.players[dc_id]
            self.saved_players[dc_player.name] = dc_player

            dc_name = str(dc_player.name)
            self.mud_server.log(dc_name)
            for plid, player in self.players.items():
                self.mud_server.log(dc_name + " disconnected")
                player.message(dc_name + " disconnected")
            self.mud_server.log(dc_name + " disconnected")
            del (self.players[dc_id])

    def handle_commands(self):
        for player_id, cmd, params in self.mud_server.get_commands():
            if player_id not in self.players.keys():
                continue

            player = self.players[player_id]

            if player.name is None:
                player.name = cmd
                player.player_id = player_id
                player.location = "CyberBar"

                if player.name in self.saved_players.keys():
                    savedplayer = self.saved_players[player.name]
                    player.message("Welcome back!")
                    player.location = savedplayer.location

                for pid, pl in self.players.items():
                    self.mud_server.send_message(pid, player.name + " entered.")

                self.mud_server.log(player.name + " entered.")
                player.load_programs()

            else:
                player.attempt_run_program(cmd, params, self)

    def check_players(self):
        for pid, player in self.players.items():
            player.update()

    def run(self):
        while True:
            time.sleep(0.2)
            self.mud_server.update()
            self.handle_new_connections()
            self.handle_disconnect()
            self.handle_commands()
            self.check_players()


if __name__ == '__main__':
    instance = MudGame()
    instance.run()
