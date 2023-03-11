from binary_search_trees_traversals_balancing.assignment.dictionary_and_hash_tables import get_index


class BasicHashTable:
    def __init__(self, max_size=0):
        # 1. Create a list of size `max_size` with all values None
        self.data_list = [None] * max_size

    def insert(self, key, value):
        # 1. Find the index for the key using get_index
        idx = get_valid_index(self.data_list, key)
        print(idx)
        # 2. Store the key-value pair at the right index
        self.data_list[idx] = (key, value)

    def find(self, key):
        # 1. Find the index for the key using get_index
        idx = get_valid_index(self.data_list, key)

        # 2. Retrieve the data stored at the index
        kv = self.data_list[idx]

        # 3. Return the value if found, else return None
        return None if kv is None else kv[1]

    def update(self, key, value):
        # 1. Find the index for the key using get_index
        idx = get_valid_index(self.data_list, key)

        # 2. Store the new key-value pair at the right index
        self.data_list[idx] = (key, value)

    def list_all(self):
        # 1. Extract the key from each key-value pair
        return [kv[0] for kv in self.data_list if kv is not None]


def get_valid_index(data_list, key):
    # Start with the index returned by get_index
    idx = get_index(data_list, key)

    while True:
        # Get the key-value pair stored at idx
        try:
            kv = data_list[idx]
        except IndexError:
            kv = None

        # If it is None, return the index
        if kv is None:
            return idx

        # If the stored key matches the given key, return the index
        k, v = kv
        if k == key[0]:
            return idx

        # Move to the next index
        idx += 1

        # Go back to the start if you have reached the end of the array
        if idx == len(data_list):
            idx = 0


if __name__ == "__main__":
    basic_table = BasicHashTable(max_size=1024)
    print("\nchecking is hash table max length is same as data list variable, ", len(basic_table.data_list) == 1024)
    # Insert some values
    basic_table.insert('Aakash', '9999999999')
    basic_table.insert('Hemanth', '8888888888')

    # Find a value
    print("\nFind a value based on given key, ", basic_table.find('Hemanth') == '8888888888')

    # Update a value
    print("\nUpdate a value")
    basic_table.update('Aakash', '7777777777')

    # Check the updated value
    print("\nchecking for a updated value, ", basic_table.find('Aakash') == '7777777777')

    # Get the list of keys
    print("\nAll values in list", basic_table.list_all() == ['Aakash', 'Hemanth'])

    # Handling collisions with linear Probing
    basic_table.insert('listen', 99)

    basic_table.insert('silent', 200)
    print("\nFinding inserted value, ", basic_table.find('listen'))

    # Create an empty hash table
    data_list2 = [None] * 4096

    # New key 'listen' should return expected index
    print("\nchecking for a expected value, ", get_valid_index(data_list2, 'listen') == 655)

    # Insert a key-value pair for the key 'listen'
    data_list2[get_index(data_list2, 'listen')] = ('listen', 99)

    # Colliding key 'silent' should return next index
    print("\nColliding key index matching status, ", get_valid_index(data_list2, 'silent') == 656)

    # We modified hash table with linear probing
    probing_table = BasicHashTable(4096)

    # Insert a value
    probing_table.insert('listen', 99)

    # Check the value
    print("\nChecking value for listen string, ", probing_table.find('listen') == 99)

    # Insert a colliding key
    probing_table.insert('silent', 200)

    # Check the new and old keys
    print("\nChecking for a new and old keys, \n", probing_table.find('listen') == 99 and probing_table.find('silent') == 200)

    # Update a key
    probing_table.insert('listen', 101)

    # Check the value
    print("\nFind a value, ", probing_table.find('listen') == 101)

    print("\nChecking all values, ", probing_table.list_all() == ['listen', 'silent'])

