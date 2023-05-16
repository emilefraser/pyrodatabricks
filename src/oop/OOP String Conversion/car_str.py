class Car:
    def __init__(self, color, mileage):
        self.color = color
        self.mileage = mileage

    def __str__(self):
        return 'a {self.color} car'.format(self=self)

#in the repl
my_car = Car('red', 37281)
print(my_car)
#a red car
my_car
#<__console__.Car object at 0x10e984b00>
str(my_car)
#'a red car'
'{}'.format(my_car)
#'a red car'
