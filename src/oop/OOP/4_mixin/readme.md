# Mixing Features With Mixin Classes
One of the uses of multiple inheritance in Python is to extend a class features through mixins. A mixin is a class that provides methods to other classes but are not considered a base class.

A mixin allows other classes to reuse its interface and implementation without becoming a super class. They implement a unique behavior that can be aggregated to other unrelated classes. They are similar to composition but they create a stronger relationship.

Let’s say you want to convert objects of certain types in your application to a dictionary representation of the object. You could provide a .to_dict() method in every class that you want to support this feature, but the implementation of .to_dict() seems to be very similar.

This could be a good candidate for a mixin.