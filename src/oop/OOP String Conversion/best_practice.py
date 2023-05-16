#always put a repr in place to explicitly differentiate str from repr

class Car:
    def __init__(self, color, mileage):
        self.color = color
        self.mileage = mileage

    def __repr__(self):
        return '{self.__class__.__name__}({self.color}, {self.mileage})'.format(self=self)

    def __str__(self):
        return 'a {self.color} car'.format(self=self)