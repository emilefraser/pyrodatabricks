
# file1.py
print("File1 __name__ = %s" %__name__)


def tester():
    print("File1 : tester")
    
if __name__ == "__main__": 
    print("File1 is being run directly")
else: 
    print("File1 is being imported")