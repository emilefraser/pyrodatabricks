# Composition to Model “Has A” Relationship

Composition models a has a relationship. With composition, a class Composite has an instance of class Component and can leverage its implementation. The Component class can be reused in other classes completely unrelated to the Composite.

In the composition example above, the Employee class has an Address object. Address implements all the functionality to handle addresses, and it can be reused by other classes.

Other classes like Customer or Vendor can reuse Address without being related to Employee. They can leverage the same implementation ensuring that addresses are handled consistently across the application.

A problem you may run into when using composition is that some of your classes may start growing by using multiple components. Your classes may require multiple parameters in the constructor just to pass in the components they are made of. This can make your classes hard to use.

A way to avoid the problem is by using the Factory Method to construct your objects. You did that with the composition example.

If you look at the implementation of the EmployeeDatabase class, you’ll notice that it uses ._create_employee() to construct an Employee object with the right parameters.

This design will work, but ideally, you should be able to construct an Employee object just by specifying an id, for example employee = Employee(1).

You are basically saying that there should only be one _AddressBook, one _PayrollSystem, and one _ProductivitySystem. Again, this design pattern is called the Singleton design pattern, which comes in handy for classes from which there should only be one, single instance.
https://en.wikipedia.org/wiki/Singleton_pattern
