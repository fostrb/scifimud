#from mapobjs.room import Room
#from room import Room

# build functions operations:
#   Area.build is passed coordinates and attempts to build in those coordinates.
#   Directional references: passed source coordinates and a direction, return coordinates (or object) in that place.
#


class Area(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.grid = [[None] * width for _ in range(height)]


    def get_cell(self, x, y):
        return self.grid[y][x]

    def set_cell(self, x, y, val):
        self.grid[y][x] = val

    def print_self(self):
        print('   ', end='')
        # ------------------------------------
        for x in range(self.width):
            print(' ' + str(x), end=' ')
        print()
        # ------------------------------------
        for row in range(len(self.grid)):
            # ---------------------
            print(row, end='  ')
            # ---------------------
            r = self.grid[row]
            for cell in r:
                if cell is not None:
                    print('[' + str(cell.name) + ']', end="")
                else:
                    print('   ', end='')
            print()

    def get_north(self, x, y):
        y_north = y - 1
        return self.get_cell(x, y_north)

    def get_south(self, x, y):
        y_south = y + 1
        return self.get_cell(x, y_south)

    def get_east(self, x, y):
        x_east = x + 1
        return self.get_cell(x_east, y)

    def get_west(self, x, y):
        x_west = x - 1
        return self.get_cell(x_west, y)

    def get_neighbors(self, x, y):
        neighbors = {}
        neighbors['n'] = self.get_north(x, y)
        neighbors['s'] = self.get_south(x, y)
        neighbors['e'] = self.get_east(x, y)
        neighbors['w'] = self.get_west(x, y)
        return neighbors

    def get_coords(self, room):
        for i in range(self.height):
            row = self.grid[i]
            for j in range(self.width):
                cur_room = row[j]
                if cur_room == room:
                    return j, i

    def build_north(self, x, y, room, connection=None):
        return self.build_room(x, y-1, room, connection=connection)

    def build_south(self, x, y, room):
        return self.build_room(x, y+1, room)

    def build_east(self, x, y, room):
        return self.build_room(x+1, y, room)

    def build_west(self, x, y, room):
        return self.build_room(x-1, y, room)

    def build(self, _x, _y, direction, room, connection=None):
        x = _x
        y = _y
        if direction == 'n':
            y = y - 1
        elif direction == 's':
            y = y + 1
        elif direction == 'e':
            x = x + 1
        elif direction == 'w':
            x = x - 1
        self.set_cell(x, y, room)
        return x, y

    def build_room(self, x, y, rname=None, connection=None):
        # check the incoming data
        # check the build location
        if connection is not None:
            pass

        if self.get_cell(x, y) is not None:
            return None

        r = RCell(rname, self.neighbors_cb, self.coordinates_cb, self.connections_cb, self.build_north_cb,
                  self.build_south_cb, self.build_east_cb, self.build_west_cb)
        self.set_cell(x, y, r)
        return r

    # These are callbacks for room-level access to relational data and functions possessed by the Area
    def neighbors_cb(self, room):
        x, y = self.get_coords(room)
        n = self.get_neighbors(x, y)
        return n

    def coordinates_cb(self, room):
        x, y = self.get_coords(room)
        return x, y

    def connections_cb(self, room):
        pass

    def build_north_cb(self, room, name):
        x, y = self.get_coords(room)
        room = self.build_north(x, y, name)
        return room

    def build_south_cb(self, room, name):
        x, y = self.get_coords(room)
        room = self.build_south(x, y, name)
        return room

    def build_east_cb(self, room, name):
        x, y = self.get_coords(room)
        room = self.build_east(x, y, name)
        return room

    def build_west_cb(self, room, name):
        x, y = self.get_coords(room)
        room = self.build_west(x, y, name)
        return room


class RCell(object):
    def __init__(self, name=None, neighbors_cb=None, coordinates_cb=None, connections_cb=None, build_n_cb=None, build_s_cb=None, build_e_cb=None, build_w_cb=None):
        self.name = name

        self.neighbors_cb = neighbors_cb
        self.coordinates_cb = coordinates_cb
        self.connections_cb = connections_cb

        self.build_north_cb = build_n_cb
        self.build_south_cb = build_s_cb
        self.build_east_cb = build_e_cb
        self.build_west_cb = build_w_cb

    def get_neighbors(self):
        n = self.neighbors_cb(self)
        return n

    def get_connections(self):
        self.connections_cb(self)

    def get_coordinates(self):
        x, y = self.coordinates_cb(self)
        return y, x

    def build_north(self, name):
        room = self.build_north_cb(self, name)
        return room

    def build_south(self, name):
        room = self.build_south_cb(self, name)
        return room

    def build_east(self, name):
        room = self.build_east_cb(self, name)
        return room

    def build_west(self, name):
        room = self.build_west_cb(self, name)
        return room


class Connection(object):
    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    a = Area(10, 10)
    startroom = a.build_room(5, 5, '0')
    northroom = startroom.build_north("a")
    z = northroom.build_west("z")
    v = z.build_north("x")
    p = v.build_east('p')
    startroom.build_south('d')

    print(p.name + '\'s neighbors:')
    for key, val in p.get_neighbors().items():
        if val is not None:
            print(key, val.name)

    a.print_self()


