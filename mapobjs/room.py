class InvalidExitError(Exception):
    pass


class RoomExit(object):
    def __init__(self, direction=None, name='door', dest=None):
        self.direction = direction.lower()
        self.dest = dest
        self.name = name
        self.description = ''


class Room(object):
    def __init__(self, name='unnamed_room'):
        self.name = name
        self.exits = []
        self.directions = []
        self.description = ''

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

