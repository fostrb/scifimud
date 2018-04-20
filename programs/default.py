from programs.newprog import NewProg
import argparse
import time


__all__ = ['Look', 'Go', 'Progs', 'Talk', 'Whisper', 'Users', 'Slap', 'Inspect', 'Whoami', 'Attack', 'Stats', 'Derezz']

# TODO: classify commands by type so they can be listed usefully


class Look(NewProg):
    def __init__(self):
        super(Look, self).__init__()
        self.name = 'look'
        self.aliases = ['ls', 'l', 'll']

    def run(self, player, args, mud):
        output = ""
        loc = mud.map.get_location(player.location)
        players_in_loc = []
        for p in mud.players:
            if p.location == loc.name:
                players_in_loc.append(p)

        output += loc.get_display() + '\n'
        if len(players_in_loc) > 0:
            output += "Players here:\n"
            for p in players_in_loc:
                output += '\n'+ p.name + '\n'
        return output


class Go(NewProg):
    def __init__(self):
        super(Go, self).__init__()
        self.name = 'go'
        self.aliases = ['move', 'walk']

    def run(self, player, args, mud):
        output = ""
        loc = mud.map.get_location(player.location)
        if args in loc.exits.keys():
            player.location = loc.exits[args]
            output += "Moved via " + args + " to " + loc.exits[args] + '\n'
            for pl in mud.players:
                if pl != player:
                    if pl.location == player.location:
                        output += player.name + " entered " + pl.location + " via " + args + '\n'
        return output


class Progs(NewProg):
    def __init__(self):
        super(Progs, self).__init__()
        self.name = 'progs'

    def run(self, player, args, mud):
        output = ""
        output += "Programs loaded:\n"
        for prog in mud.interpreter.programs:
            output += "\t" + prog.name + '\n'
        return output


class Talk(NewProg):
    def __init__(self):
        super(Talk, self).__init__()
        self.name = 'talk'

    def run(self, player, args, mud):
        for otherplayer in mud.players:
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

        for target_player in mud.players:
            if target_player.name == target:
                target_player.message('[' + player.name + ']:' + message)


class Users(NewProg):
    def __init__(self):
        super(Users, self).__init__()
        self.name = 'users'

    def run(self, player, args, mud):
        output = ""
        output += "Users online:\n"
        for p in mud.players:
            output += p.name + '\n'
        return output


class Slap(NewProg):
    def __init__(self):
        super(Slap, self).__init__()
        self.name = 'slap'

    def run(self, player, args, mud):
        target = args
        for p in mud.players:
            if p.name == target and p.location == player.location:
                p.message("SLAP")
                for np in mud.players:
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
        output = ''
        try:
            parsed = self.parse_args(args)
            if parsed.target:
                # things in the location
                loc = mud.map.get_location(player.location)
                for pl in mud.players:
                    if pl.location == player.location:
                        if pl.name == parsed.target:
                            output += "Inspecting " + pl.name + "...\n"
                            break
                for exitname, e in loc.exits.items():
                    if exitname == parsed.target:
                        output += "Inspecting " + exitname + "...\n"
                        output += "leads to " + e + '\n'
            return output
        except Exception as e:
            mud.mud_server.log(e)


class Whoami(NewProg):
    def __init__(self):
        super(Whoami, self).__init__()
        self.name = 'whoami'

    def run(self, player, args, mud):
        return player.name


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
                for target in mud.players:
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
                for target in mud.players:
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
        output = ""
        output += player.name + '\n'
        if player.is_derezzed:
            output += "You are derezzed\n"
            output += "remaining:" + str(int(player.derezzed_remaining)) + '\n'
        else:
            output += "Health:" + str(player.health) + '\n'
