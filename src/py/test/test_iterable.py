from collections.abc import Iterable
iterable_item = [3,6,4,2,1]

assert isinstance(iterable_item, Iterable) # Success Example

assert isinstance(3, Iterable) # Fail Example