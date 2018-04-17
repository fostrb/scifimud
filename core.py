import os
from os import listdir
from os.path import isfile, join, isdir


class Location(object):
    def __init__(self, directory):
        self.directory = os.path.normpath(directory)
        self.name = os.path.basename(self.directory)

    def get_files(self):
        f_list = [f for f in listdir(self.directory) if isfile(join(self.directory, f))]
        return f_list

    def read_file(self, file):
        if file in self.get_files():
            f = open(os.path.normpath(self.directory + '/' + file))
            data = f.read()
            f.close()
            return data

    def write_file(self, filename, data):
        if filename in self.get_files():
            f = open(os.path.normpath(self.directory + '/' + filename), 'w')
            f.write(data)

    def is_locked(self, file):
        f = open(os.path.normpath(self.directory + '/' + file))
        line = f.readline()
        f.close()
        if "!!" in line:
            return line.split(':')
        else:
            return False

    def get_doors(self):
        d_list = [f for f in listdir(self.directory) if isdir(join(self.directory, f))]
        return d_list

    def attempt_move(self, door):
        if door in self.get_doors():
            door_dir = os.path.normpath(self.directory + '/' + door)
            new_loc = Location(door_dir)
            return new_loc
        else:
            return self

    def get_inspectables(self):
        i_list = []
        for file in self.get_files():
            i_list.append(file)
        for door in self.get_doors():
            i_list.append(door)
        return i_list

    def inspect(self, target=None):
        i_list = self.get_inspectables()

        if target:
            pass
        else:
            print("contents of location " + self.name + ':')
            for each in i_list:
                print('\t'+each)


class Environment(object):
    def __init__(self, location=None):
        self.location = location

    def get_files(self):
        f_list = self.location.get_files()
        return f_list

    def write_file(self, filename, data):
        self.location.write_file(filename, data)

    def read_file(self, file):
        data = self.location.read_file(file)
        return data

    def is_locked(self, file):
        locked = self.location.is_locked(file)
        return locked

    def attempt_move(self, target):
        self.location = self.location.attempt_move(target)
