def main():
    data = read_data_from_web()
    modified_data = process_data(data)
    write_data_to_database(modified_data)

if __name__ == "__main__":
    main()


    python3 best_practices.py

    >>> import best_practices as bp
This is my file to demonstrate best practices.
>>> data = "Data from a file"
>>> modified_data = bp.process_data(data)
Beginning data processing...
Data processing finished.
>>> bp.write_data_to_database(modified_data)
Writing processed data to a database
Data from a file that has been modified

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()

print("Guru99")



# File2.py 
    
import File1 
    
print("File2 __name__ = %s" %__name__)
    
if __name__ == "__main__":
    print("File2 is being run directly")
else: 
    print("File2 is being imported")