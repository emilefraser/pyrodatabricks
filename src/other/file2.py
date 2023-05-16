# File2.py 
    
import file1 
from file1 import tester
    
print("File2 __name__ = %s" %__name__)
print(tester)

    
if __name__ == "__main__":
    print("File2 is being run directly")
else: 
    print("File2 is being imported")