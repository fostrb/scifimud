from mapobjs.area import Area
from mapobjs.room import GNETMap, Room, RoomExit


class GalaxMap(object):
    def __init__(self):
        rooms = []
        startroom = Room('Galaxnet Dome')
        startroom.description = "Welcome to gnet. You are in a dome. This is the spawnpoint."
        rooms.append(startroom)

        r1 = Room('The Foyer')
        r1.exits.append(RoomExit(direction='North', dest='Galaxnet Dome', name='door'))
        r1.description = "You are in the foyer outside the gnet spawn. It's shitty."
        rooms.append(r1)

        r2 = Room('The Garden')
        r2.exits.append(RoomExit(direction='West', dest='Galaxnet Dome', name='garden door'))
        r2.description = "You're in the gnet garden."
        rooms.append(r2)

        wb = GNETMap(rooms)


        self.rooms = wb.rooms

    def get_location(self, name):
        for room in rooms:
            if room.name == name:
                return room


if __name__ == '__main__':
    #area = Area(4, 5)
    rooms = []
    startroom = Room('Galaxnet Dome')
    startroom.description = "Welcome to gnet. You are in a dome. This is the spawnpoint."
    rooms.append(startroom)

    r1 = Room('The Foyer')
    r1.exits.append(RoomExit(direction='North', dest='Galaxnet Dome', name='door'))
    r1.description = "You are in the foyer outside the gnet spawn. It's shitty."
    rooms.append(r1)

    r2 = Room('The Garden')
    r2.exits.append(RoomExit(direction='West', dest='Galaxnet Dome', name='garden door'))
    r2.description = "You're in the gnet garden."
    rooms.append(r2)

    wb = GNETMap(rooms)

    for room in wb.rooms:
        print(room.name)
        if len(room.exits) != 0:
            print("\tExits:")
            for e in room.exits:
                print("\t\tName:" + e.name)
                print("\t\tDirection:" + e.direction)
                print("\t\tDest:" + e.dest)
