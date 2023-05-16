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

class Triangle:
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

class RightPyramid(Triangle, Square):
    def __init__(self, base, slant_height):
        self.base = base
        self.slant_height = slant_height

    def area(self):
        base_area = super().area()
        perimeter = super().perimeter()
        return 0.5 * perimeter * self.slant_height + base_area

#both subclasses have area. It will call triangle and error because
#of resolution order.
# Every class has an .__mro__ 
# attribute that allows us to inspect the order, so let’s do that:

# >>> RightPyramid.__mro__
# (<class '__main__.RightPyramid'>, <class '__main__.Triangle'>, 
#  <class '__main__.Square'>, <class '__main__.Rectangle'>, 
#  <class 'object'>)


# The problem here is that the interpreter is searching for .area() 
# in Triangle before Square and Rectangle, and upon finding .area() 
# in Triangle, Python calls it instead of the one you want. 
# Because Triangle.area() expects there to be a .height and a .base 
# attribute, Python throws an AttributeError.

# Luckily, you have some control over how the MRO is constructed. 
# Just by changing the signature of the RightPyramid class, 
# you can search in the order you want, and the methods will resolve 
# correctly: