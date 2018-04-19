# TODO: Scrap and rewrite.


class Location(object):
    def __init__(self, name='', description='', exits={}):
        self.name = name
        self.description = description
        self.exits = exits

    def get_display(self):
        output = self.name + ":\n"
        output += '\t' + self.description + '\n'
        output += "Exits:"
        for ename, eloc in self.exits.items():
            output += '\n\t' + ename
        return output

    def print_self(self):
        print(self.name + ": " + self.description)
        print("exits:")
        for e in self.exits:
            print('\t'+e)


class GalaxMap(object):
    def __init__(self):
        self.locations = []
        self.rooms = {
            "CyberBar": {
                "description": "You're in the CyberBar",
                "exits": {"door": "Outside", "portal": "Void"}
            },
            "Outside": {
                "description": "You're outside",
                "exits": {"door": "CyberBar"}
            },
            "Void": {
                "description": "You're in the void.",
                "exits": {"outside": "Outside"}
            }
        }
        self.make_map()

    def get_location(self, name):
        for location in self.locations:
            if location.name == name:
                return location

    def make_map(self):
        for room in self.rooms:
            description = self.rooms[room]["description"]
            exits = {}
            for ename, newloc in self.rooms[room]["exits"].items():
                exits[ename] = newloc
            self.locations.append(Location(name=room, description=description, exits=exits))


if __name__ == '__main__':
    GalaxMap()
