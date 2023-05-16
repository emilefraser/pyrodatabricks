# You first import the relevant functions and classes from other modules. 
# The _EmployeeDatabase is made internal, and at the bottom, you create a 
# single instance. This instance is public and part of the interface 
# because you will want to use it in the application.

# You changed the _EmployeeDatabase._employees attribute to be a 
# dictionary where the key is the employee id and the value is the 
# employee information. You also exposed a .get_employee_info() method 
# to return the information for the specified employee employee_id.

# The _EmployeeDatabase.employees property now sorts the keys to 
# return the employees sorted by their id. You replaced the method 
# that constructed the Employee objects with calls to the Employee 
# initializer directly.

# The Employee class now is initialized with the id and uses the public 
# functions exposed in the other modules to initialize its attributes.

from productivity import get_role
from hr import get_policy
from contacts import get_employee_address
from representations import AsDictionaryMixin

class _EmployeeDatabase:
    def __init__(self):
        self._employees = {
            1: {
                'name': 'Mary Poppins',
                'role': 'manager'
            },
            2: {
                'name': 'John Smith',
                'role': 'secretary'
            },
            3: {
                'name': 'Kevin Bacon',
                'role': 'sales'
            },
            4: {
                'name': 'Jane Doe',
                'role': 'factory'
            },
            5: {
                'name': 'Robin Williams',
                'role': 'secretary'
            }
        }


    @property
    def employees(self):
        return [Employee(id_) for id_ in sorted(self._employees)]

    def get_employee_info(self, employee_id):
        info = self._employees.get(employee_id)
        if not info:
            raise ValueError(employee_id)
        return info



class Employee(AsDictionaryMixin):
    def __init__(self, id):
        self.id = id
        info = employee_database.get_employee_info(self.id)
        self.name = info.get('name')
        self.address = get_employee_address(self.id)
        self._role = get_role(info.get('role'))
        self._payroll = get_policy(self.id)

    def work(self, hours):
        duties = self._role.perform_duties(hours)
        print(f'Employee {self.id} - {self.name}:')
        print(f'- {duties}')
        print('')
        self._payroll.track_work(hours)

    def calculate_payroll(self):
        return self._payroll.calculate_payroll()

employee_database = _EmployeeDatabase()