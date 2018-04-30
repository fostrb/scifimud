from mapobjs.area import Area
from mapobjs.room import Room, NewRoomConnection


class NewArea(object):
    def __init__(self, rooms):
        # ---------------------------------------------------------------------
        rooms = []
        startroom = Room('Galaxnet Dome')
        startroom.description = "Welcome to gnet. You are in a dome. This is the spawnpoint."
        rooms.append(startroom)

        r1 = Room('The Foyer')
        door1 = NewRoomConnection(name='door')
        r1.new_connect(door1, startroom, 'north')
        r1.description = "You are in the foyer outside the gnet spawn. It's shitty."
        rooms.append(r1)

        r2 = Room('The Garden')
        door2 = NewRoomConnection(name='garden_door')
        r2.new_connect(door2, startroom, 'west')
        door3 = NewRoomConnection(name='other_door')
        r2.new_connect(door3, r1, 'north')
        r2.description = "You're in the gnet garden."
        rooms.append(r2)
        #---------------------------------------------------------------------
        self.rooms = rooms
        self.buildme()

    def get_starting_room(self):
        for room in self.rooms:
            if room.name == 'Galaxnet Dome':
                return room

    def printme(self):
        for room in self.rooms:
            print(room.name)
            print("connections:")
            for direction, door_dict in room.connection_dict.items():
                    for door, dest in door_dict.items():
                        print("\t" + door.name + " : " + direction + " -> " + dest.name)

    def buildme(self):
        for room in self.rooms:
            for conn in room._desired_connections:
                room.new_connect(conn)

    # get_location
    def get_room_by_name(self, name):
        for room in self.rooms:
            if room.name.lower() == name.lower():
                return room

    def get_room_by_id(self, rid):
        for room in self.rooms:
            if room.id == rid:
                return room


class NewMap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[' '] * width for _ in range(height)]

        self.set_cell(4, 5, 'S')
        self.set_cell(4, 6, 'F')
        self.set_cell(5, 5, 'G')
        self.print_self()
        self.get_cell(7, 2)

    def get_cell(self, x, y):
        return self.grid[y][x]

    def set_cell(self, x, y, val):
        self.grid[y][x] = val

    def print_self(self):
        for row in self.grid:
            for cell in row:
                if cell != ' ':
                    print('[' + str(cell) + ']', end="")
                else:
                    print('   ', end='')
            print()


if __name__ == '__main__':
    rooms = []
    startroom = Room('Galaxnet Dome')
    startroom.description = "Welcome to gnet. You are in a dome. This is the spawnpoint."
    rooms.append(startroom)

    r1 = Room('The Foyer')
    #r1connect = RoomConnection(name='door', direction='North', dest=startroom)
    door1 = NewRoomConnection(name='door')
    #r1connect.description = "It's a doooooooor!"
    #r1.connect_to(r1connect)
    r1.new_connect(door1, startroom, 'north')
    r1.description = "You are in the foyer outside the gnet spawn. It's shitty."
    rooms.append(r1)

    r2 = Room('The Garden')
    #r2.connect_to(startroom)
    r2.description = "You're in the gnet garden."
    rooms.append(r2)

    NewArea(None)
