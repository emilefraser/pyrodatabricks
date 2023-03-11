
class HashTable:
    def insert(self, key, value):
        """Insert a new key-value pair"""
        pass

    def find(self, key):
        """Find the value associated with a key"""
        pass

    def update(self, key, value):
        """Change the value associated with a key"""
        pass

    def list_all(self):
        """List all the keys"""
        pass


def get_index(data_list, a_string):
    # Variable to store the result (updated after each iteration)
    result = 0
    for a_character in a_string:
        # Convert the character to a number (using ord)
        # print(ord(a_character))
        a_number = ord(a_character)
        # Update result by adding the number
        result += a_number

    # Take the remainder of the result with the size of the data list
    print("final result, ", result)
    try:
        list_index = result % len(data_list)
    except ZeroDivisionError:
        list_index = 0
    print("index", list_index)
    return list_index


if __name__ == "__main__":
    phone_numbers = {
      'Rushikesh': '9489484949',
      'Hemanth': '9595949494',
      'Siddhant': '9231325312'
    }
    print(f"phone numbers, {phone_numbers}")
    print(f"Fetch data by key, {phone_numbers['Rushikesh']}")
    new_value = phone_numbers['Vishal'] = '8787878787'
    print("Adding a new value")
    print(f"Added new value, {new_value}")
    new_value = phone_numbers['Rushikesh'] = '8787878787'
    print(f"Updating value based on key, {new_value}")
    print(f"Printing all values, {phone_numbers}")
    for name in phone_numbers:
        print('Name:', name, ', Phone Number:', phone_numbers[name])

    MAX_HASH_TABLE_SIZE = 4096
    data_list_ = [None] * MAX_HASH_TABLE_SIZE
    print(get_index(data_list_, '') == 0)
    print("\nindex status for a string", get_index(data_list_, 'Aakash') == 585)
    print("\nindex status for a string", get_index(data_list_, 'Don O Leary') == 941)
    key, value = 'Aakash', '7878787878'
    idx = get_index(data_list_, key)
    print(f"\nindex, {idx}")
    data_list_[idx] = (key, value)
    print(f"\nKey Value added, ")
    data_list_[get_index(data_list_, 'Hemanth')] = ('Hemanth', '9595949494')

    # Find Index based on value
    idx = get_index(data_list_, 'Aakash')
    print(f"index is, {idx}")
    key, value = data_list_[idx]
    print(f"index value is, {value}")

    # List all pairs excepting None values
    pairs = [kv[0] for kv in data_list_ if kv is not None]
    print(f"Pair values, {pairs}")
