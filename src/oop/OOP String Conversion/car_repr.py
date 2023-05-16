class Car:
    def __init__(self, color, mileage):
        self.color = color
        self.mileage = mileage

    def __repr__(self):
        return '__repr__ for car'

    def __str__(self):
        return '__str__ for car'

#in the repl
my_car = Car('red', 37281)
print(my_car)
#__str__ for car
str(my_car)
#'__str__ for car'
'{}'.format(my_car)
#'__str__ for car'


my_car
#__repr__ for car
repr(my_car)
#__repr__ for car
