class Test(object):
    def __init__(self, first_name, last_name ):
        self.first_name = first_name
        self.last_name = last_name

    def test_all_class_arguments(self):
        print('Testing both of the class variables to see whether they are both strings!')

        for _ in [self.first_name, self.last_name]:
            assert(type(_) is str)
        print('------')
        print('Passed all of the tests')

yay = Test('James' , 'Phoenix') # Success Example
yay.test_all_class_arguments()

# Testing both of the class variables to see whether they are both strings!
#------
#Passed all of the tests


yay = Test(5 , 'Phoenix') # Fail Example
yay.test_all_class_arguments()

#Testing both of the class variables to see whether they are both strings!
#------
#AssertionError 