#-----------__operators__-------------------#
# Adds the two numbers
1 + 2
#3

# Concatenates the two strings
'Real' + 'Python'
#'RealPython'


# Gives the product
3 * 2
#6

# Repeats the string
'Python' * 3
#'PythonPythonPython'

#-----------__functions__-------------------#

a = 'Real Python'
b = ['Real', 'Python']
len(a)
#11
a.__len__()
#11
b[0]
#'Real'
b.__getitem__(0)
#'Real'

dir(a)
# ['__add__',
#  '__class__',
#  '__contains__',
#  '__delattr__',
#  '__dir__',
#  ...,
#  '__iter__',
#  '__le__',
#  '__len__',
#  '__lt__',
#  ...,
#  'swapcase',
#  'title',
#  'translate',
#  'upper',
#  'zfill']


#-----------__overloading builtin functions__-------------------#

#change the behaviour of length by overriding

class Order:
    def __init__(self, cart, customer):
        self.cart = list(cart)
        self.customer = customer

    def __len__(self):
        return len(self.cart)

order = Order(['banana', 'apple', 'mango'], 'Real Python')
len(order)
#3

#if not present you'll get a type error
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: object of type 'Order' has no len()