from uuid import uuid4 as uuid


class InvalidExitError(Exception):
    pass


class RoomExit(object):
    def __init__(self, direction=None, name='door', dest=None):
        self.direction = direction.lower()
        self.dest = dest
        self.name = name
        self.description = ''


class NewRoomConnection(object):
    def __init__(self, name):
        self.name = name


class RoomConnection(object):
    def __init__(self, direction, name='door', dest=None):
        self.direction = direction.lower()
        self.name = name
        self.dest = dest
        self.description = ''
        self.id = uuid()


class Room(object):
    def __init__(self, name='unnamed_room'):
        self.name = name
        self.exits = []
        self.directions = []
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

    def get_connection_names(self, name):
        for direction, doorlist in self.connection_dict.items():
            rlist = []
            for door in doorlist:
                rlist.append(door.name)
            return rlist

    def get_connection_by_name(self, name):
        if name in self.connection_dict:
            return self.connection_dict[name]

    def get_exit_by_name(self, ename):
        ename = ename.strip()
        for rexit in self.exits:
            if ename == rexit.name:
                return rexit
        return None

    def get_exit_names(self):
        rlist = []
        for rexit in self.exits:
            rlist.append(rexit.name)
        return rlist

    def can_accept_exit(self, roomexit):
        if roomexit.direction.lower() == 'north':
            if 'south' not in self.directions:
                return True
        if roomexit.direction.lower() == 'south':
            if 'north' not in self.directions:
                return True
        if roomexit.direction.lower() == 'east':
            if 'west' not in self.directions:
                return True
        if roomexit.direction.lower() == 'west':
            if 'east' not in self.directions:
                return True
        return False


class GNETMap(object):
    def __init__(self, rooms):
        self.rooms = rooms
        self.build_area()

    def opposite_directions(self, e1):
        if e1.lower() == 'north':
            return 'south'
        if e1.lower() == 'south':
            return 'north'
        if e1.lower() == 'east':
            return 'east'
        if e1.lower() == 'west':
            return 'west'
        if e1.lower() == 'up':
            return 'down'
        if e1.lower() == 'down':
            return 'up'
        else:
            return False

    def build_area(self):
        second_pass_rooms = []

        for room in self.rooms:
            name = room.name
            print('building ...' + name)
            exits = room.exits

            if not len(exits) == 0:
                for roomexit in room.exits:
                    found = False
                    for built_room in self.rooms:
                        if built_room.name == roomexit.dest:
                            found = True
                            if built_room.can_accept_exit(roomexit):
                                newdirection = self.opposite_directions(roomexit.direction)
                                newexit = RoomExit(direction=newdirection, name=roomexit.name, dest=room.name)
                                built_room.exits.append(newexit)
                            else:
                                raise InvalidExitError()
                    if not found:
                        second_pass_rooms.append(room)
