# policy design
# https://en.wikipedia.org/wiki/Modern_C%2B%2B_Design#Policy-based_design
# The general advice is to use the relationship that creates fewer dependencies between two classes. 
# This relation is composition. Still, there will be times where inheritance will make more sense.
# Inheritance to Model “Is A” Relationship
# Liskov’s substitution principle says that an object of type Derived, which inherits from Base, 
# can replace an object of type Base without altering the desirable properties of a program.


# Let’s say you have a class A that provides an implementation 
# and interface you want to reuse in another class B. 
# Your initial thought is that you can derive B from A and inherit both the interface 
# and implementation. To be sure this is the right design, you follow theses steps:

# Evaluate B is an A: Think about this relationship and justify it. Does it make sense?

# Evaluate A is a B: Reverse the relationship and justify it. Does it also make sense?

# If you can justify both relationships, then you should never inherit those classes from one another. 
# Let’s look at a more concrete example.

from hr import PayrollSystem
from productivity import ProductivitySystem
from employees import EmployeeDatabase

productivity_system = ProductivitySystem()
payroll_system = PayrollSystem()
employee_database = EmployeeDatabase()
employees = employee_database.employees
productivity_system.track(employees, 40)
payroll_system.calculate_payroll(employees)