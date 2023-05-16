# used nametuples which are sub class of tuple
from collections import namedtuple
TestResults = namedtuple('TestResults', ['failed', 'attempted'])
print(TestResults(0, 1))
