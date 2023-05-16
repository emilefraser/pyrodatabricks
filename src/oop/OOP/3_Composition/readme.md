# Composition in Python
Composition is an object oriented design concept that models a has a relationship. In composition, a class known as composite contains an object of another class known to as component. In other words, a composite class has a component of another class.

Composition allows composite classes to reuse the implementation of the components it contains. The composite class doesn’t inherit the component class interface, but it can leverage its implementation.

The composition relation between two classes is considered loosely coupled. That means that changes to the component class rarely affect the composite class, and changes to the composite class never affect the component class.

This provides better adaptability to change and allows applications to introduce new requirements without affecting existing code.

When looking at two competing software designs, one based on inheritance and another based on composition, the composition solution usually is the most flexible. You can now look at how composition works.

You’ve already used composition in our examples. If you look at the Employee class, you’ll see that it contains two attributes:

id to identify an employee.
name to contain the name of the employee.
These two attributes are objects that the Employee class has. Therefore, you can say that an Employee has an id and has a name.

# Flexible Designs With Composition

Composition is more flexible than inheritance because it models a loosely coupled relationship. Changes to a component class have minimal or no effects on the composite class. Designs based on composition are more suitable to change.

You change behavior by providing new components that implement those behaviors instead of adding new classes to your hierarchy.

Take a look at the multiple inheritance example above. Imagine how new payroll policies will affect the design. Try to picture what the class hierarchy will look like if new roles are needed. As you saw before, relying too heavily on inheritance can lead to class explosion.

The biggest problem is not so much the number of classes in your design, but how tightly coupled the relationships between those classes are. Tightly coupled classes affect each other when changes are introduced.

In this section, you are going to use composition to implement a better design that still fits the requirements of the PayrollSystem and the ProductivitySystem.

