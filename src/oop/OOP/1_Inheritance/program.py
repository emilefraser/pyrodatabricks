# In program.py

import hr
import disgruntled

salary_employee = hr.SalaryEmployee(1, 'John Smith', 1500)
hourly_employee = hr.HourlyEmployee(2, 'Jane Doe', 40, 15)
commission_employee = hr.CommissionEmployee(3, 'Kevin Bacon', 1000, 250)
disgruntled_employee = disgruntled.DisgruntledEmployee(20000, 'Anonymous')
payroll_system = hr.PayrollSystem()
payroll_system.calculate_payroll([
    salary_employee,
    hourly_employee,
    commission_employee,
    #BAD! duck typed - doesn't inherit but looks like a duck so it quacks
    disgruntled_employee 
])

# Use inheritance to reuse an implementation: 
# Your derived classes should leverage most of their base class 
# implementation. They must also model an is a relationship. 
# A Customer class might also have an id and a name, but a Customer 
# is not an Employee, so you should not use inheritance.

# Implement an interface to be reused: When you want your class 
# to be reused by a specific part of your application, you implement 
# the required interface in your class, but you don’t need to 
# provide a base class, or inherit from another class.