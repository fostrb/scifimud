from mapobjs.room import Room


class Area(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.grid = []
        for row in range(width):
            self.grid.append([])
            for column in range(height):
                self.grid[row].append(0)
