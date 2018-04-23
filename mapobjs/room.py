from uuid import uuid4 as uuid


class NewRoomConnection(object):
    def __init__(self, name):
        self.name = name


class Room(object):
    def __init__(self, name='unnamed_room'):
        self.name = name
        self.description = ''
        self.id = uuid()

        self._desired_connections = []

        # direction: {door:dest, door2:dest2}
        self.connection_dict = {
            'north': {},
            'south': {},
            'east': {},
            'west': {}
        }

    def get_description(self):
        rval = self.name + '\n'
        rval += self.description+'\n'
        rval += "Doors:\n"
        print("HERE")
        for direction, door_dict in self.connection_dict.items():
            for door, dest in door_dict.items():
                print(direction, door.name, dest.name)
                rval += "\t" + direction.upper() + " : " + door.name + " -> " + dest.name
        return rval

    # connect SELF via DOOR to DEST from DEST's DIRECTION
    def new_connect(self, door, dest, direction):
        if direction not in self.connection_dict:
            self.connection_dict[direction] = {}
        if isinstance(dest, Room):
            if isinstance(door, NewRoomConnection):
                direction_inverse = dest.accept_new_connect(door, self, direction)
                if direction_inverse:
                    if dest not in self.connection_dict[direction_inverse]:
                        if door not in self.connection_dict[direction_inverse]:
                            self.connection_dict[direction_inverse][door] = dest

    def accept_new_connect(self, door, dest, direction):
        # attempting to accept a connection to DEST
        # leading DIRECTION
        # via DOOR
        if isinstance(dest, Room) and isinstance(door, NewRoomConnection):
            if direction not in self.connection_dict:
                self.connection_dict[direction] = {}
            inverse = self.invert_direction(direction)
            if inverse:
                if door not in self.connection_dict[direction]:
                    self.connection_dict[direction][door] = dest
                    return inverse
        return False

    def invert_direction(self, direction):
        if direction == 'north':
            return 'south'
        elif direction == 'south':
            return 'north'
        elif direction == 'east':
            return 'west'
        elif direction == 'west':
            return 'east'
        else:
            return False

    def get_connection_by_name_new(self, name):
        for direction, doorlist in self.connection_dict.items():
            for door in doorlist:
                if door.name.lower() == name.lower():
                    return door

    def get_connection_names(self):
        for direction, doorlist in self.connection_dict.items():
            rlist = []
            for door in doorlist:
                rlist.append(door.name)
            return rlist

    def get_connection_by_name(self, name):
        if name in self.connection_dict:
            return self.connection_dict[name]
        return None
