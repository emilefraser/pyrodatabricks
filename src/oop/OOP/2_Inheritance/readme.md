# Inheritance to Model “Is A” Relationship

Inheritance should only be used to model an is a relationship. Liskov’s substitution principle says that an object of type Derived, which inherits from Base, can replace an object of type Base without altering the desirable properties of a program.

Liskov’s substitution principle is the most important guideline to determine if inheritance is the appropriate design solution. Still, the answer might not be straightforward in all situations. Fortunately, there is a simple test you can use to determine if your design follows Liskov’s substitution principle.

Let’s say you have a class A that provides an implementation and interface you want to reuse in another class B. Your initial thought is that you can derive B from A and inherit both the interface and implementation. To be sure this is the right design, you follow theses steps:

Evaluate B is an A: Think about this relationship and justify it. Does it make sense?

Evaluate A is a B: Reverse the relationship and justify it. Does it also make sense?

If you can justify both relationships, then you should never inherit those classes from one another. Let’s look at a more concrete example.

You have a class Rectangle which exposes an .area property. You need a class Square, which also has an .area. It seems that a Square is a special type of Rectangle, so maybe you can derive from it and leverage both the interface and implementation.

Before you jump into the implementation, you use Liskov’s substitution principle to evaluate the relationship.

A Square is a Rectangle because its area is calculated from the product of its height times its length. The constraint is that Square.height and Square.length must be equal.

It makes sense. You can justify the relationship and explain why a Square is a Rectangle. Let’s reverse the relationship to see if it makes sense.

A Rectangle is a Square because its area is calculated from the product of its height times its length. The difference is that Rectangle.height and Rectangle.width can change independently.

It also makes sense. You can justify the relationship and describe the special constraints for each class. This is a good sign that these two classes should never derive from each other.

You might have seen other examples that derive Square from Rectangle to explain inheritance. You might be skeptical with the little test you just did.