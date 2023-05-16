import math
#static method had no dependency / impact
#on the class or object

class Pizza:
    def __init__(self, radius, ingredients):
        self.ingredients = ingredients
        self.radius = radius

    def __repr__(self):
        return f'Pizza({self.ingredients})'

    def area(self):
        return self._circle_area(self.radius)

    @staticmethod
    def _circle_area(r):
        return r ** 2 * math.pi

    @classmethod
    def margherita(cls, radius):
        return cls(radius, ['cheese','tomatoes'])

    @classmethod
    def prosciutto(cls, radius):
        return cls(radius, ['cheese','tomatoes'])

p = Pizza.margherita(10)
p = Pizza.prosciutto(10)