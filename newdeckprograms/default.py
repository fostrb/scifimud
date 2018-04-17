from newdeckprograms.newprog import NewProg
import argparse
import time


__all__ = ['Look', 'Go', 'Progs', 'Talk', 'Whisper', 'Users', 'Slap', 'Inspect', 'Whoami', 'Attack', 'Stats', 'Derezz']


class Look(NewProg):
    def __init__(self):
        super(Look, self).__init__()
        self.name = 'look'
        self.aliases = ['ls', 'l', 'll']

    def run(self, player, args, mud):
        loc = mud.map.get_location(player.location)
        players_in_loc = []
        for player_id, p in mud.players.items():
            if p.location == loc.name:
                players_in_loc.append(p)

        player.message(loc.get_display())
        if len(players_in_loc) > 0:
            player.message("Players here:")
            for p in players_in_loc:
                player.message('\t' + p.name)


class Go(NewProg):
    def __init__(self):
        super(Go, self).__init__()
        self.name = 'go'
        self.aliases = ['move', 'walk']

    def run(self, player, args, mud):
        loc = mud.map.get_location(player.location)
        if args in loc.exits.keys():
            player.location = loc.exits[args]
            player.message("Moved via " + args + " to " + loc.exits[args])
            for pid, pl in mud.players.items():
                if pl != player:
                    if pl.location == player.location:
                        pl.message(player.name + " entered " + pl.location + " via " + args)


class Progs(NewProg):
    def __init__(self):
        super(Progs, self).__init__()
        self.name = 'progs'

    def run(self, player, args, mud):
        player.message("Programs loaded:")
        for prog in player.programs:
            player.message("\t" + prog.name)


class Talk(NewProg):
    def __init__(self):
        super(Talk, self).__init__()
        self.name = 'talk'

    def run(self, player, args, mud):
        for pid, otherplayer in mud.players.items():
            if otherplayer.location == player.location:
                otherplayer.message(player.name + ':' + args)


class Whisper(NewProg):
    def __init__(self):
        super(Whisper, self).__init__()
        self.name = 'whisper'

    def run(self, player, args, mud):
        message = ''
        target = args.split()[0]
        for each in range(1, len(args.split())):
            message += args.split()[each] + ' '

        for pid, target_player in mud.players.items():
            if target_player.name == target:
                target_player.message('[' + player.name + ']:' + message)


class Users(NewProg):
    def __init__(self):
        super(Users, self).__init__()
        self.name = 'users'

    def run(self, player, args, mud):
        player.message("Users online:")
        for pid, p, in mud.players.items():
            player.message(p.name)


class Slap(NewProg):
    def __init__(self):
        super(Slap, self).__init__()
        self.name = 'slap'

    def run(self, player, args, mud):
        target = args
        for pid, p in mud.players.items():
            if p.name == target and p.location == player.location:
                p.message("SLAP")
                for nid, np in mud.players.items():
                    if np.location == p.location:
                        np.message(player.name + " SLAPPED " + target)
                break


class Inspect(NewProg):
    def __init__(self):
        super(Inspect, self).__init__()
        self.name = 'inspect'
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('target')

    def run(self, player, args, mud):
        try:
            parsed = self.parse_args(args)
            if parsed.target:
                # things in the location
                loc = mud.map.get_location(player.location)
                for pid, pl in mud.players.items():
                    if pl.location == player.location:
                        if pl.name == parsed.target:
                            player.message("Inspecting " + pl.name + "...")
                            player.message("Health:" + str(pl.health))
                            player.message("Atk:" + str(pl.atk))
                            break
                for exitname, e in loc.exits.items():
                    if exitname == parsed.target:
                        player.message("Inspecting " + exitname + "...")
                        player.message("Leads to " + e)
        except:
            pass


class Whoami(NewProg):
    def __init__(self):
        super(Whoami, self).__init__()
        self.name = 'whoami'

    def run(self, player, args, mud):
        player.message(player.name)


class Load(NewProg):
    def __init__(self):
        super(Load, self).__init__()
        self.name = 'load'

    def run(self, player, args, mud):
        pass


class Attack(NewProg):
    def __init__(self):
        super(Attack, self).__init__()
        self.name = 'attack'
        self.aliases = ['atk']
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('target')

    def run(self, player, args, mud):
        try:
            parsed = self.parse_args(args)
            if parsed.target:
                for pid, target in mud.players.items():
                    if target.location == player.location:
                        if target.name == parsed.target:
                            result = player.attack_target(target)
                            if result:
                                target.message(player.name + " attacked you!")
                                target.message(str(player.atk) + "dmg. " + str(target.health) + " health remaining.")
                            else:
                                target.message(player.name + " took a swing at you!")
                            break

        except Exception as e:
            player.message(str(e))


class Derezz(NewProg):
    def __init__(self):
        super(Derezz, self).__init__()
        self.name = 'derezz'
        self.aliases = ['kill', 'dr']
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('target')
        self.run_while_derezzed = False

    def run(self, player, args, mud):
        try:
            parsed = self.parse_args(args)
            if parsed.target:
                for pid, target in mud.players.items():
                    if target.location == player.location:
                        if target.name == parsed.target:
                            target.derezz(10, str(player.name + " derezzed you."))
        except Exception as e:
            player.message(str(e))


class Stats(NewProg):
    def __init__(self):
        super(Stats, self).__init__()
        self.name = 'stats'

    def run(self, player, args, mud):
        player.message(player.name)
        if player.is_derezzed:
            player.message("You are derezzed")
            player.message("remaining:" + str(int(player.derezzed_remaining)))
        else:
            player.message("Health:" + str(player.health))