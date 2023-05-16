class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * self.length + 2 * self.width

class Square(Rectangle):
    def __init__(self, length):
        super(Square, self).__init__(length, length)

# In Python 3, the super(Square, self) call is equivalent to the 
# parameterless super() call. The first parameter refers to the 
# subclass Square, while the second parameter refers to a Square 
# object which, in this case, is self. 
# You can call super() with other classes as well:

class Cube(Square):
    def surface_area(self):
        face_area = super(Square, self).area()
        return face_area * 6

    def volume(self):
        #supering to the grand daddy!
        face_area = super(Square, self).area()
        return face_area * self.length